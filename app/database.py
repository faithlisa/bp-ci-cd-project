import sqlite3

def get_connection():
    conn = sqlite3.connect("bp.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blood_pressure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            systolic INTEGER NOT NULL,
            diastolic INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
