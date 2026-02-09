import psycopg2
from psycopg2 import sql
from util import (
  validIndex,
  readConfig,
)

from constants import (
  DBINIT_PATH,
  DBINIT_SEC,
  MAX_NUM_PLAYER,
  NUM_TEAM
)

class DB:
  # TODO: return false if failed to connect to the database
  # TODO: check if the method should self.conn.commit() every time
  def __init__(self):
    self.conn = psycopg2.connect(**readConfig(DBINIT_PATH, DBINIT_SEC))
    self.cur = self.conn.cursor()
    self.create_tables()
    print("successfully created a table")
  
  def close(self):
    if self.cur:
      self.cur.close()
    if self.conn:
      self.conn.close()

  def create_tables(self):
    # Scheme "player ID - codename - team ID - score"
    # (team ID is ommited to take advantage of modulo property)
    self.cur.execute(sql.SQL(
      '''
      CREATE TABLE IF NOT EXISTS players (
        player_id SERIAL PRIMARY KEY,
        codename TEXT,
        score NUMERIC DEFAULT 0,
        is_registered BOOLEAN DEFAULT FALSE
      )
      WITH (fillfactor = {});
     '''
    ).format(
      sql.Literal(MAX_NUM_PLAYER*NUM_TEAM) 
    ))

    # Scheme "player ID - equipment ID"
    self.cur.execute(sql.SQL(
      '''
      CREATE TABLE IF NOT EXISTS equips (
        player_id INTEGER 
          REFERENCES players(player_id) 
          ON DELETE CASCADE,
        equip_id INTEGER,
        PRIMARY KEY (player_id, equip_id)
      );
     '''
    ))
  
  def getIndex(player_id: int, team_id: int):
    return player_id+team_id*MAX_NUM_PLAYER
  
  def set_player(self, player_id: int, codename: str, team_id: int):
    if not validIndex(player_id, MAX_NUM_PLAYER) or not validIndex(team_id, NUM_TEAM):
      return False
    
    # disable the row if the codename is at size 0
    registered = "TRUE" if len(codename)>0 else "FALSE"

    self.cur.execute(sql.SQL(
      '''
      UPDATE players
      SET codename = '{}',
        is_registered = {}
      WHERE player_id = {};
      '''
    ).format(
      sql.Identifier(codename),
      sql.Identifier(registered),
      sql.Literal(self.getIndex(player_id, team_id))
    ))

  def update_score(self, diff:int, player_id:int, team_id:int):
    if not validIndex(player_id, MAX_NUM_PLAYER) or not validIndex(team_id, NUM_TEAM):
      return False
    
    idx=self.getIndex(player_id, team_id)

    # 1. get the current score
    self.cur.execute(sql.SQL(
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

    self.cur.execute(sql.SQL(
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
    if not validIndex(team_id, NUM_TEAM):
      return False
    
    # 1. get an array (player_id is a dummy slot replaced with a rank)
    lb=team_id*MAX_NUM_PLAYER
    ub=lb+MAX_NUM_PLAYER

    self.cur.execute(sql.SQL(
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

    self.cur.execute(sql.SQL(
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
    if not validIndex(player_id, MAX_NUM_PLAYER) or not validIndex(team_id, NUM_TEAM):
      return False

    # INSERT iff equip_id is yet to be registered
    self.cur.execute(sql.SQL(
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
      sql.Literal(self.getIndex(player_id, team_id)),
      sql.Literal(equip_id)
    ))

    return self.cur.rowcount==1


  # TODO: Assign equipment

  # TODO: Collect equipment


  # TODO: clear equips
  # TODO: clear players