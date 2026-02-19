# This file is temporary for an assignment

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR/"src"

sys.path.insert(0, str(SRC_DIR))

from database import DB

if __name__ == "__main__":
  database = DB()
  print("--- calling showTable() ---")
  database.showTable()
  print("--- called showTable() ---")