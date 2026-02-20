"""Test configuration and fixtures."""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from db import create_sqlite_database, setup_database


@pytest.fixture
def temp_db():
    """Create a temporary test database.

    Yields:
        Database connection to temporary test DB
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        conn = create_sqlite_database(db_path)
        setup_database(conn)
        yield conn
    finally:
        if conn:
            conn.close()
        Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def sample_player():
    """Create a sample player object.

    Returns:
        Player instance for testing
    """
    from models.player import Player
    from datetime import datetime

    return Player(
        name="Test Player",
        email="test@example.com",
        age=25,
        phone="555-123-4567",
        date=datetime.now(),
    )
