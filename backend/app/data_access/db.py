import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'techvault.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

    from .seed import seed_data
    seed_data()

def ensure_default_users():
    """Create default accounts on every startup if they don't already exist."""
    conn = get_db()
    cursor = conn.cursor()
    defaults = [
        ('admin',    'admin@techvault.com',    'admin123',    'admin'),
        ('customer', 'customer@techvault.com', 'customer123', 'customer'),
    ]
    cursor.executemany(
        'INSERT OR IGNORE INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
        defaults
    )
    conn.commit()
    conn.close()
