import psycopg2
from contextlib import closing

from util import isDevMode

class DB:
    def __init__(self):
        # Store connection parameters for later use
        self.connection_params = {
            'dbname': 'photon',
            'user': 'student',
            'password': 'student',
            'host': 'localhost',
            'port': '5432'
        }
        # Optionally, establish a persistent connection
        self.conn = None
        if not isDevMode():
            self._connect()
            self._init_db()
        else:
            print("warning: database connection is temporarily disabled")

    def _connect(self):
        """Create and store a connection."""
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Connection error: {e}")
            self.conn = None

    def _init_db(self):
        """Create tables if they don't exist and perform any initial setup."""
        if not self.conn:
            return
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    codename VARCHAR(20)
                );
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Error initializing database: {e}")

    def add_player(self, codename):
        """Insert a new player and return the generated id."""
        if not self.conn:
            # Option A: reopen connection if closed
            self._connect()
        try:
            self.cursor.execute(
                "INSERT INTO players (codename) VALUES (%s) RETURNING id;",
                (codename,)
            )
            new_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return new_id
        except Exception as e:
            self.conn.rollback()
            print(f"Error adding player: {e}")
            return None

    def query_id(self, player_id):
        """Retrieve a player by id."""
        if not self.conn:
            self._connect()
        try:
            self.cursor.execute(
                "SELECT * FROM players WHERE id = %s;",
                (player_id,)
            )
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error querying player: {e}")
            return None

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            self.conn = None