import sqlite3
import os

DB_NAME = os.getenv("DB_NAME", "urls.db")

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT,
            response_time REAL
        )
    """)
    conn.commit()
    conn.close()

