"""
Database connection and configuration.
Manages SQLite database connection lifecycle.
"""
import sqlite3
import os
from pathlib import Path
from contextlib import contextmanager


# Database path configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_DIR = BASE_DIR / "data"
DB_PATH = DB_DIR / "campus.db"


def get_db_path() -> Path:
    """Get the database file path"""
    # Create data directory if it doesn't exist
    DB_DIR.mkdir(exist_ok=True)
    return DB_PATH


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Ensures proper connection cleanup.
    
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM events")
    """
    conn = sqlite3.connect(str(get_db_path()))
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def init_database():
    """
    Initialize database schema.
    Creates tables if they don't exist.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create Events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL CHECK(category IN ('cultural', 'technical')),
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                venue TEXT NOT NULL,
                organizer TEXT NOT NULL,
                description TEXT
            )
        """)
        
        # Create Exams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exam_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                department TEXT NOT NULL CHECK(department IN ('CSE', 'ECE', 'ME', 'CE', 'IT', 'EEE')),
                semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 8),
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                venue TEXT NOT NULL
            )
        """)
        
        # Create Placements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS placements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                role TEXT NOT NULL,
                department TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                venue TEXT NOT NULL
            )
        """)
        
        conn.commit()
        print(f"✅ Database initialized at: {get_db_path()}")