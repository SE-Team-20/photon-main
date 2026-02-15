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

  def close(self):
    if self.cur:
      self.cur.close()
    if self.conn:
      self.conn.close()
    self.cur=None
    self.conn=None


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

