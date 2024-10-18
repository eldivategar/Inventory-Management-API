import sqlite3
from app.config.config import Config

def get_db_connection():
    if Config.DATABASE_PATH is None:
        raise Exception("Database path not set. Please set the DATABASE_PATH in .env file.")
    else:
        conn = sqlite3.connect(f"app/{Config.DATABASE_PATH}")
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    conn = get_db_connection()
    try:
        with open('app/database/schema.sql') as f:
            conn.executescript(f.read())
        conn.commit()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def close_db(conn):
    if conn is not None:
        conn.close()