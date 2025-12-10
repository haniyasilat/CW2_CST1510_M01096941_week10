import sqlite3
from pathlib import Path

def connect_database():
    """Connect to SQLite database"""
    # FIX: Use the actual database file you have
    db_path = Path(__file__).parent / "intelligence_platform.db"
    
    # Debug: uncomment next line to see the path
    # print(f"Database path: {db_path}")
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn