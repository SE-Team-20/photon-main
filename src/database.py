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

# TODO: change a scheme and add "game session ID" to keep track of the player pool for the specific match
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
  # TODO: make it register to the buffer on memory instead
  def set_player(self, row_index: int, team_id: int, codename: str):
    self._ensure_db()
    if not validIndex(team_id, NUM_TEAM):
      return False
  
  # TODO: 
  def assign_equip(self, row_index: int, team_id: int, equip_id: int):
    self._ensure_db()
    if not validIndex(team_id, NUM_TEAM):
      return False
    return False

  # update the player score by a difference to the previous score
  def update_score(self, diff:int, player_id:int):
    self._ensure_db()
    return False

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
  
  # TODO: returns a player ID
  def get_player_info(self, equip_id: int):
    return False
  
  # TODO: 
  def free_equipment(self, equip_id:int):
    return False

  # TODO: 
  def free_equips(self):
    return False
  
  # TODO: 
  def clear_buffer(self):
    return False
