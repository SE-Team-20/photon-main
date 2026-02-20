import psycopg2
from psycopg2 import sql
from util import validIndex, isDevMode
from constants import MAX_NUM_PLAYER, NUM_TEAM

# Connection parameters
connection_params = {
    "dbname": "photon",
    # "user": "student",
    # "password": "student",
    # "host": "localhost",
    # "port": "5432"
}

# Helper class for managing player ID allocation
class UnionFind:
    def __init__(self, registered):
        self.root = {}
        for x in registered:
            self.root[x] = x
        for x in registered:
            self.root[x] = self.find(x + 1)

    def find(self, x=0) -> int:
        if x not in self.root:
            return x
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
        return self.root[x]

    def use(self, x: int) -> bool:
        if x in self.root:
            return False
        self.root[x] = self.find(x + 1)
        return True

# Helper class for managing game state
class GameManager:
    def __init__(self):
        self.equips = {}
        self.players = {}

    def add_player(self, playerID: int, teamID: int, equipID: int) -> bool:
        if equipID in self.equips or playerID in self.players:
            return False
        self.equips[equipID] = playerID
        self.players[playerID] = teamID
        return True

class DB:
    def __init__(self):
        if isDevMode():
            print("warning: database connection is temporarily disabled")
            self.conn = None
            self.cur = None
            self.uf = None
            self.gm = None
            return

        try:
            self.conn = psycopg2.connect(**connection_params)
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print("DB connection failed:", e)
            self.conn = None
            self.cur = None
            self.uf = None
            self.gm = None
            return

        self.create_table()
        self.uf = UnionFind(self.get_all_ids())
        self.gm = GameManager()
        if isDevMode():
            print("dev: DB connection succeeded")

    # Internal helpers
    def ensure_db(self):
        if self.conn is None or self.cur is None:
            raise RuntimeError("Database is not connected")

    def safe_exec(self, query):
        try:
            self.ensure_db()
            self.cur.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("DB error:", e)
            return False

    def create_table(self):
        """Create the players table with only id and codename."""
        self.safe_exec(sql.SQL(
            '''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                codename TEXT
            );
            '''
        ))

    def get_all_ids(self):
        self.ensure_db()
        try:
            self.cur.execute("SELECT id FROM players;")
            return [row[0] for row in self.cur.fetchall()]
        except Exception as e:
            print("DB error in get_all_ids:", e)
            return []

    def get_player_info(self, playerID: int):
        self.ensure_db()
        try:
            self.cur.execute(
                sql.SQL(
                    "SELECT id, codename FROM players WHERE id = {};"
                ).format(sql.Literal(playerID))
            )
            row = self.cur.fetchone()
            if row is None:
                return False
            return [row[0], row[1] if row[1] is not None else ""]
        except Exception as e:
            print("DB error in get_player_info:", e)
            return False

    def add_player(self, codename):
        # Insert a new player with auto‑generated ID. Returns the new id.
        if self.conn is None:
            self.connect()
        try:
            self.ensure_db()
            self.cur.execute(
                "INSERT INTO players (codename) VALUES (%s) RETURNING id;",
                (codename,)
            )
            new_id = self.cur.fetchone()[0]
            self.conn.commit()
            if self.uf:
                self.uf.use(new_id)
            # Show the updated table after insertion
            self.show_table()
            return new_id
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print("Error adding player:", e)
            return None

    def query_id(self, id):
        if self.conn is None:
            self.connect()
        try:
            self.ensure_db()
            self.cur.execute("SELECT * FROM players WHERE id = %s;", (id,))
            return self.cur.fetchone()
        except Exception as e:
            print("Error querying player:", e)
            return None

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        self.cur = None
        self.conn = None

    def is_registered(self, playerID: int) -> bool:
        # Return True if a player with the given ID exists.
        self.ensure_db()
        try:
            self.cur.execute(
                sql.SQL("SELECT EXISTS (SELECT 1 FROM players WHERE id = {});").format(sql.Literal(playerID))
            )
            return self.cur.fetchone()[0]
        except Exception as e:
            print("DB error in is_registered:", e)
            return False

    def update_codename(self, playerID: int, codename: str) -> bool:
        if self.uf is None:
            return False
        if not self.uf.use(playerID):
            return False
        success = self.safe_exec(sql.SQL(
            "INSERT INTO players (id, codename) VALUES ({}, {});"
        ).format(sql.Literal(playerID), sql.Literal(codename)))
        if success:
            # Show the updated table after insertion
            self.show_table()
        return success

    def queue_player(self, playerID: int, teamID: int, equipID: int) -> bool:
        if self.gm is None or not self.is_registered(playerID):
            return False
        return self.gm.add_player(playerID, teamID, equipID)

    def show_table(self) -> bool:
        # show all players in the database
        print("--- all players in the database ---")
        self.ensure_db()
        try:
            self.cur.execute("SELECT id, codename FROM players ORDER BY id;")
            rows = self.cur.fetchall()
            for pid, name in rows:
                print(f"ID: {pid}, codename: {name if name else ''}")
        except Exception as e:
            print("DB error in show_table:", e)
            return False
        print("---------")
        return True

    def update_codename(self, playerID: int, codename: str) -> bool:
        result = self.safe_exec(sql.SQL(
            "UPDATE players SET codename = {} WHERE id = {};"
        ).format(sql.Literal(codename), sql.Literal(playerID)))
        if result and self.cur.rowcount == 0:
            return False   # No player with that ID
        if result:
            # Show the updated table after successful update
            self.show_table()
        return result

    def get_leaderboard(self, team_id: int):
        self.ensure_db()
        if not validIndex(team_id, NUM_TEAM):
            return False
        lb = team_id * MAX_NUM_PLAYER
        ub = lb + MAX_NUM_PLAYER
        try:
            self.cur.execute(
                sql.SQL(
                    "SELECT id, codename FROM players "
                    "WHERE {} <= id AND id < {} "
                    "ORDER BY codename;"
                ).format(sql.Literal(lb), sql.Literal(ub))
            )
            rows = self.cur.fetchall()
            if not rows:
                return []
            # Build result with ranks (ties if codenames duplicate)
            res = []
            prev_name = None
            for i, (pid, name) in enumerate(rows):
                if i == 0 or name != prev_name:
                    rank = i + 1
                else:
                    rank = res[-1][0]
                res.append((rank, name, 0))   # score always 0
                prev_name = name
            return res
        except Exception as e:
            print("DB error in get_leaderboard:", e)
            return False

    def connect(self):
        try:
            self.conn = psycopg2.connect(**connection_params)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"Connection error: {e}")
            self.conn = None
            self.cur = None

    def query_codename(self, id: int):
        # return codename if exitst, false otherwise
        info = self.get_player_info(id)
        if info is False:
            return False
        return info[1]  # codename


#global methods for simplified access to the DB class
_db_instance = None
_last_checked_registered = False   # state for is_registered()

def _get_db():
    global _db_instance
    if _db_instance is None:
        _db_instance = DB()
    return _db_instance

def _query_codename(id):
    global _last_checked_registered
    db = _get_db()
    codename = db.query_codename(id)
    _last_checked_registered = (codename is not False)
    return codename

def _is_registered():
    return _last_checked_registered

def _update_codename(id, codename):
    db = _get_db()
    return db.update_codename(id, codename)

def _update_codename(id, codename):
    db = _get_db()
    return db.update_codename(id, codename)

def _queue_player(id, team_id, equip_id):
    db = _get_db()
    return db.queue_player(id, team_id, equip_id)

def close():
    db = _get_db()
    db.close()