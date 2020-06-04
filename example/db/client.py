import os
import sqlite3

import aiosql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

conn = sqlite3.connect("db.db")
queries = aiosql.from_path(os.path.join(BASE_DIR, "queries.sql"), "sqlite3")
