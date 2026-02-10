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
# TODO: fix all
class DB:
  def __init__(self):
    try:
      self.conn = psycopg2.connect(**readConfig(DBINIT_PATH, DBINIT_SEC))
      self.cur = self.conn.cursor()
    except psycopg2.Error as e:
      print("DB connection failed:", e)
      self.conn=None
      self.cur=None
    self._create_table()
    if isDevMode():
      print("dev: DB connection succeeded")
  
  def _ensure_db(self):
    if self.conn is None or self.cur is None:
      raise RuntimeError("Database is not connected")
  
  def _safe_exec(self, query):
    try:
      self.cur.execute(query)
      self.conn.commit()
      return True
    except Exception as e:
      self.conn.rollback()
      print("DB error:", e)
      return False

  def close(self):
    if self.cur:
      self.cur.close()
    if self.conn:
      self.conn.close()
    self.cur=None
    self.conn=None

  # Scheme "player ID - codename - team ID - score"
  def _create_table(self):
    self._ensure_db()

    self._safe_exec(sql.SQL(
      '''
      CREATE TABLE IF NOT EXISTS players (
        player_id SERIAL PRIMARY KEY,
        team_id INTEGER DEFAULT -1,
        codename TEXT,
        score NUMERIC DEFAULT 0,
        is_registered BOOLEAN DEFAULT FALSE
      )
      WITH (fillfactor = {});
     '''
    ).format(
      sql.Literal(MAX_NUM_PLAYER*NUM_TEAM) 
    ))
  
  # assign a codename to a specific player id row
  def set_player(self, player_id: int, team_id: int, codename: str):
    self._ensure_db()
    if not validIndex(team_id, NUM_TEAM):
      return False
    
    # disable the row if the codename is at size 0
    registered = "TRUE" if len(codename)>0 else "FALSE"

    self._safe_exec(sql.SQL(
      '''
      UPDATE players
      SET codename = '{}',
        team_id = {},
        is_registered = {},
        score = 0
      WHERE player_id = {};
      '''
    ).format(
      sql.Identifier(codename),
      sql.Literal(team_id),
      sql.Identifier(registered),
      sql.Literal(player_id)
    ))

  # update the player score by a difference to the previous score
  def update_score(self, diff:int, player_id:int, team_id:int):
    self._ensure_db()
    if not validIndex(player_id, MAX_NUM_PLAYER) or not validIndex(team_id, NUM_TEAM):
      return False
    
    idx=self._get_index(player_id, team_id)

    # 1. get the current score
    self._safe_exec(sql.SQL(
      '''
      SELECT score
      FROM players
      WHERE player_id = {}
        AND is_registered=TRUE;
      '''
    ).format(
      sql.Literal(idx)
    ))

    row=self.cur.fetchone()
    if row is None:
      return False

    # 2. apply the change
    new_score=row[0]+diff

    self._safe_exec(sql.SQL(
      '''
      UPDATE players
      SET score = {}
      WHERE player_id = {}
        AND is_registered=TRUE;
      '''
    ).format(
      sql.Literal(new_score),
      sql.Literal(idx)
    ))

  # returns a tuple of {rank, codename, score} in non-decreasing order
  def get_leaderboard(self, team_id:int):
    self._ensure_db()
    if not validIndex(team_id, NUM_TEAM):
      return False
    
    # 1. get an array (player_id is a dummy slot replaced with a rank)
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

    # 2. write a rank and return the set of tuples
    res=[list(r) for r in rows]

    res[0][0]= 1
    for i in range(1, len(res)):
      res[i][0]= res[i-1][0] if res[i][2]==res[i-1][2] else i+1
    
    return [tuple(r) for r in res]
  
  # returns a pair of {team_id, player_id} 
  def get_player_info(self, equip_id: int):
    self._ensure_db()

    self._safe_exec(sql.SQL(
      '''
      SELECT player_id
      FROM equips
      WHERE equip_id={}
      '''
    ).format(
      sql.Literal(equip_id)
    ))

    idx=self.cur.fetchone()
    if idx is None or not validIndex(idx, NUM_TEAM*MAX_NUM_PLAYER):
      return False

    return [idx/MAX_NUM_PLAYER, idx%MAX_NUM_PLAYER]
  
  def assign_equipment(self, player_id:int, team_id:int, equip_id:int):
    self._ensure_db()

    if not validIndex(player_id, MAX_NUM_PLAYER) or not validIndex(team_id, NUM_TEAM):
      return False

    # INSERT iff equip_id is yet to be registered
    self._safe_exec(sql.SQL(
      '''
      INSERT INTO equips (equip_id, player_id)
      SELECT {}, {}
      WHERE NOT EXISTS (
        SELECT 1
        FROM equips
        WHERE equip_id = {}
      );
      '''
    ).format(
      sql.Literal(equip_id),
      sql.Literal(self._get_index(player_id, team_id)),
      sql.Literal(equip_id)
    ))

    return self.cur.rowcount==1

  # remove specific equipment
  def free_equipment(self, equip_id:int):
    self._ensure_db()

    self._safe_exec(sql.SQL(
      '''
      DELETE FROM equips
      WHERE equip_id = {};
      '''
    ).format(
      sql.Literal(equip_id)
    ))

    return self.cur.rowcount==1

  # remove all rows
  def clear_equips(self):
    self._ensure_db()

    self._safe_exec(sql.SQL(
      '''
      TRUNCATE TABLE equips;
      '''
    ))
    return self.cur.rowcount==1
  
  # set every row invalid
  def clear_players(self):
    self._ensure_db()

    self._safe_exec(sql.SQL(
      '''
      UPDATE players
      SET is_registered = FALSE
      '''
    ))
    return self.cur.rowcount==1