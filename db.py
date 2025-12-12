import sqlite3
from datetime import datetime, timedelta

DB_PATH = "database.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            telegram_id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            bio TEXT,
            profile_photo_id TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_user(phone):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
    row = cursor.fetchone()
    conn.close()
    return row

def is_outdated(user_row):
    if not user_row:
        return True
    last = datetime.fromisoformat(user_row["updated_at"])
    return last < datetime.now() - timedelta(days=30)

def save_user(phone, telegram_id, username, first_name, last_name, bio, profile_photo_id):
    conn = get_connection()
    cursor = conn.cursor()
    current_time = datetime.now().isoformat(timespec="seconds")

    cursor.execute("""
        INSERT INTO users (phone, telegram_id, username, first_name, last_name, bio, profile_photo_id, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(phone) DO UPDATE SET
            telegram_id=excluded.telegram_id,
            username=excluded.username,
            first_name=excluded.first_name,
            last_name=excluded.last_name,
            bio=excluded.bio,
            profile_photo_id=excluded.profile_photo_id,
            updated_at=excluded.updated_at
    """, (phone, telegram_id, username, first_name, last_name, bio, profile_photo_id, current_time))

    conn.commit()
    conn.close()
