import sqlite3
from pathlib import Path

DB_PATH = Path("data/screener.db")

def get_connection():
    conn = sqlite3.connect(
        DB_PATH,
        timeout=30,              # <-- VERY important
        check_same_thread=False  # <-- FastAPI requirement
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = sqlite3.Row
    return conn
