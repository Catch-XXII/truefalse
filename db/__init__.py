"""Database initialization module with auto-setup."""

import sqlite3
from typing import Optional


DB_SCHEMA_VERSION = 1


def create_sqlite_database(filename: str) -> sqlite3.Connection:
    """Create a database connection to a SQLite database.

    Args:
        filename: Path to the database file

    Returns:
        Database connection object

    Raises:
        sqlite3.Error: If connection fails
    """
    try:
        conn = sqlite3.connect(
            filename, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        return conn
    except sqlite3.Error as error:
        raise sqlite3.Error(f"SQLite DB Connection Error: {error}") from error


def setup_database(conn: sqlite3.Connection) -> None:
    """Create all necessary tables if they don't exist.

    This is idempotent and safe to call multiple times.

    Args:
        conn: Database connection

    Raises:
        sqlite3.Error: If table creation fails
    """
    try:
        cursor = conn.cursor()

        # Create player table
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS player(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            score INTEGER NOT NULL,
            duration REAL NOT NULL,
            date TIMESTAMP NOT NULL
        )"""
        )

        # Create game_session table for tracking individual games
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS game_session(
            id INTEGER PRIMARY KEY,
            player_id INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            score INTEGER NOT NULL,
            max_score INTEGER NOT NULL,
            duration REAL NOT NULL,
            created_at TIMESTAMP NOT NULL,
            FOREIGN KEY(player_id) REFERENCES player(id)
        )"""
        )

        conn.commit()
    except sqlite3.Error as error:
        conn.rollback()
        raise sqlite3.Error(f"Error creating tables: {error}") from error
    finally:
        cursor.close()


def close_connection(conn: sqlite3.Connection) -> None:
    """Close database connection safely.

    Args:
        conn: Database connection to close
    """
    if conn:
        try:
            conn.close()
        except sqlite3.Error as error:
            print(f"Warning: Error closing database: {error}")
