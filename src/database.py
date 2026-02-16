import psycopg2
from psycopg2 import sql
from util import (
  validIndex,
  readConfig,
  isDevMode,
)

from constants import (
  DBINIT_PATH,
  DBINIT_SEC,
  MAX_NUM_PLAYER,
  NUM_TEAM
)

class UnionFind:
  def __init__(self, registered):
    self.root = {}
    for x in registered:
      self.root[x]=x
    for x in registered:
      self.root[x]=self.find(x+1)

  def find(self, x=0) -> int:
    if x not in self.root:
      return x
    if self.root[x]!=x:
      self.root[x]=self.find(self.root[x])
    return self.root[x]
  
  def use(self, x: int) -> bool:
    if x in self.root:
      return False
    self.root[x]=self.find(x+1)
    return True

# 1. holds equip-player and player-team relationship
# 2. detects equip duplication
# 3. validates the team state
class GameManager:
  def __init__(self):
    self.equips={}
    self.players={}
  def addPlayer(self, playerID:int, teamID:int, equipID:int):
    # duplicated equipment ID
    if equipID in self.equips:
      return False
    # duplicated player
    if playerID in self.players:
      return False
    
    self.equips[equipID]=playerID
    self.players[playerID]=teamID

    return True
  

class DB:
  def __init__(self):
    if isDevMode():
      print("warning: database connection is temporarily disabled")
      return

    try:
      self.conn = psycopg2.connect(**readConfig(DBINIT_PATH, DBINIT_SEC))
      self.cur = self.conn.cursor()
    except psycopg2.Error as e:
      print("DB connection failed:", e)
      self.conn=None
      self.cur=None
    self._create_table()
    self.uf = UnionFind(self.getAllPlayerID())
    self.gm = GameManager()
    if isDevMode():
      print("dev: DB connection succeeded")
  
  def _ensure_db(self):
    if self.conn is None or self.cur is None:
      raise RuntimeError("Database is not connected")
  
  def _safe_exec(self, query):
    try:
      self._ensure_db()
      self.cur.execute(query)
      self.conn.commit()
      return True
    except Exception as e:
      self.conn.rollback()
      print("DB error:", e)
      return False

  def _create_table(self):
    self._safe_exec(sql.SQL(
      '''
      CREATE TABLE IF NOT EXISTS players (
        player_id SERIAL PRIMARY KEY,
        codename TEXT,
        highscore NUMERIC DEFAULT 0,
        playcnt NUMERIC DEFAULT 0,
        is_registered BOOLEAN DEFAULT FALSE
      );
     '''
    ))
  
  def _getAllPlayerID(self):
    self._safe_exec(
    '''
    SELECT player_id
    from players
    WHERE is_registered;
    '''
    )
    return [row[0] for row in self.cur.fetchall()]

  def _getBasicPlayerInfo(self, playerID: int):
    self._safe_exec(sql.SQL(
      '''
      SELECT player_id, codename, highscore
      from players
      WHERE player_id = {};
      '''
    ).format(
      sql.Literal(playerID)
    ))
    
    row=self.cur.fetchone()

    if row is None:
      return False
    
    return [row[0], row[1] if row[1] is not None else "", row[2] if row[2] is not None else 0]

  def close(self):
    if self.cur:
      self.cur.close()
    if self.conn:
      self.conn.close()
    self.cur=None
    self.conn=None

  def isRegistered(self, playerID: int) :
    self._safe_exec(sql.SQL(
      '''
      SELECT EXISTS (
        SELECT 1
        from players
        WHERE codename = {};
      )
      '''      
    ).format(
      sql.Literal(playerID)
    ))

    return self.cur.rowcount==1

  def findNewPlayerID(self, playerID: int):
    if self.uf is None: 
      return False
    return self.uf.find()
  
  def usePlayerID(self, playerID: int, codename: str):
    if self.uf is None:
      return False
    res = self.uf.use(playerID)

    if not res:
      return False
    
    self._safe_exec(sql.SQL(
    '''
    INSERT INTO players (
      plaer_id,
      codename,
      highscore,
      playcnt,
      is_registered
    )
    VALUES ({}, {}, 0, 0, TRUE);
    '''
    ).format(
      sql.Literal(playerID),
      sql.Literal(codename)
    ))

    return True

  def addPlayerNextGame(self, playerID: int, teamID: int, equipID: int):
    if self.gm is None or not self.isRegistered(playerID):
      return False
    return self.gm.addPlayer(playerID, teamID, equipID)
  
  def showTable(self):
    print("--- all players registered in the database ---")
    for pid in self._getAllPlayerID():
      info = self._getBasicPlayerInfo(pid)

      if not info:
        print(f"Failed _getBasicPlayerInfo({info})")
        return False
      print(
        f"ID: {info[0]},"
        f"codename: {info[1]}"
        f"highscore: {info[2]}"
      )
    print("---------")
    return True

  def updateCodename(self, playerID: int, codename: str):
    self._safe_exec(sql.SQL(
      '''
      UPDATE players
      SET codename = {}
      WHERE player_id = {}
        AND is_registered;
      '''
    ).format(
      sql.Literal(codename),
      sql.Literal(playerID)
    ))

    if self.cur.rowcount==0:
      return False

    return True

  # returns a tuple of {rank, codename, score} in non-decreasing order
  def get_leaderboard(self, team_id:int):
    self._ensure_db()
    if not validIndex(team_id, NUM_TEAM):
      return False
    lb=team_id*MAX_NUM_PLAYER
    ub=lb+MAX_NUM_PLAYER
    self._safe_exec(sql.SQL(
      '''
      SELECT player_id, codename, score
      FROM players
      WHERE {} <= player_id 
        AND player_id < {} 
        AND is_registered=TRUE
      ORDER BY score, codename;
      '''
    ).format(
      sql.Literal(lb),
      sql.Literal(ub)
    ))
    rows=self.cur.fetchall()
    if not rows:
      return []
    res=[list(r) for r in rows]
    res[0][0]= 1
    for i in range(1, len(res)):
      res[i][0]= res[i-1][0] if res[i][2]==res[i-1][2] else i+1
    return [tuple(r) for r in res]

