import psycopg2
from psycopg2 import sql
from util import (
  validIndex
)

from constants import (
  DB_NAME,
  DB_USERNAME,
  DB_PASSWORD,
  DB_HOST,
  DB_PORT,
  DB_TABLE_PLAYERS,
  DB_TABLE_EQUIPS,
  MAX_NUM_PLAYER,
  NUM_TEAM
)

class DB:
  # TODO: return false if failed to make one
  def __init__(self):
    self.conn = psycopg2.connect(**connection_params)
    self.cur = self.conn.cursor()
    self.create_tables()
  
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
      CREATE TABLE IF NOT EXISTS {} (
        player_id SERIAL PRIMARY KEY,
        codename TEXT,
        score NUMERIC DEFAULT 0,
        is_registered BOOLEAN DEFAULT FALSE
      )
      WITH (fillfactor = {});
     '''
    ).format(
      sql.Identifier(DB_TABLE_PLAYERS),
      sql.Literal(MAX_NUM_PLAYER*NUM_TEAM) 
    ))

    # Scheme "player ID - equipment ID"
    self.cur.execute(sql.SQL(
      '''
      CREATE TABLE IF NOT EXISTS {} (
        player_id INTEGER 
          REFERENCES {}(player_id) 
          ON DELETE CASCADE,
        equip_id INTEGER,
        PRIMARY KEY (player_id, equip_id)
      );
     '''
    ).format(
      sql.Identifier(DB_TABLE_EQUIPS),
      sql.Identifier(DB_TABLE_PLAYERS)
    ))
  
  def getIndex(player_id: int, team_id: int):
    return player_id+team_id*MAX_NUM_PLAYER
  
  def set_player(self, player_id: int, codename: str, team_id: int):
    if not validIndex(player_id, MAX_NUM_PLAYER) or not validIndex(team_id, NUM_TEAM):
      return False
    
    # disable the row if player_id is at size 0
    registered = "TRUE" if len(player_id)>0 else "FALSE"

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

  # TODO: Update score (change, playerID, teamID)

  # TODO: Get ranking (teamID)
  

connection_params = {
  "dbname": f"{DB_NAME}",
  "user": f"{DB_USERNAME}",
  'password': f"{DB_PASSWORD}",
  'host': f"{DB_HOST}",
  'port': f"{DB_PORT}",
}

# wrapper/validator (do we need it?????)
def run_query(sql_text, params=None, fetch=False):
  with psycopg2.connect(**connection_params) as conn:
     with conn.cursor() as cur:
        cur.execute(sql_text, params)
        if fetch:
           return cur.fetchall()

# hints
  # conn.commit()
  # rows = cursor.fetchall()
  # for row in rows:
  #   print(row)