"""Test database operations."""

import pytest
import sqlite3
from datetime import datetime

from db.operations import PlayerRepository, GameResultRepository
from models.game_result import GameResult


class TestPlayerRepository:
    """Test PlayerRepository class."""

    @pytest.fixture
    def repo(self, temp_db):
        """Create a PlayerRepository with test database.

        Args:
            temp_db: Temporary database fixture

        Returns:
            PlayerRepository instance
        """
        return PlayerRepository(temp_db)

    def test_insert_player(self, repo):
        """Test inserting a player."""
        player_id = repo.insert_player(
            name="John Doe",
            email="john@example.com",
            age=30,
            phone="555-123-4567",
            date=datetime.now(),
        )

        assert player_id > 0

    def test_find_player_by_email(self, repo):
        """Test finding player by email."""
        repo.insert_player(
            name="Jane Doe",
            email="jane@example.com",
            age=28,
            phone="555-987-6543",
            date=datetime.now(),
        )

        player = repo.find_player_by_email("jane@example.com")
        assert player is not None
        assert player["name"] == "Jane Doe"
        assert player["age"] == 28

    def test_find_player_by_email_not_found(self, repo):
        """Test finding non-existent player."""
        player = repo.find_player_by_email("nonexistent@example.com")
        assert player is None

    def test_find_player_by_id(self, repo):
        """Test finding player by ID."""
        player_id = repo.insert_player(
            name="Test Player",
            email="test@example.com",
            age=25,
            phone="555-111-2222",
            date=datetime.now(),
        )

        player = repo.find_player_by_id(player_id)
        assert player is not None
        assert player["name"] == "Test Player"
        assert player["id"] == player_id

    def test_duplicate_email_raises_error(self, repo):
        """Test that duplicate email raises error."""
        repo.insert_player(
            name="Player 1",
            email="duplicate@example.com",
            age=25,
            phone="555-111-1111",
            date=datetime.now(),
        )

        with pytest.raises(sqlite3.IntegrityError):
            repo.insert_player(
                name="Player 2",
                email="duplicate@example.com",
                age=30,
                phone="555-222-2222",
                date=datetime.now(),
            )

    def test_duplicate_phone_raises_error(self, repo):
        """Test that duplicate phone raises error."""
        repo.insert_player(
            name="Player 1",
            email="player1@example.com",
            age=25,
            phone="555-123-4567",
            date=datetime.now(),
        )

        with pytest.raises(sqlite3.IntegrityError):
            repo.insert_player(
                name="Player 2",
                email="player2@example.com",
                age=30,
                phone="555-123-4567",
                date=datetime.now(),
            )


class TestGameResultRepository:
    """Test GameResultRepository class."""

    @pytest.fixture
    def repo(self, temp_db):
        """Create a GameResultRepository with test database.

        Args:
            temp_db: Temporary database fixture

        Returns:
            GameResultRepository instance
        """
        return GameResultRepository(temp_db)

    def test_insert_game_result(self, repo):
        """Test inserting a game result."""
        result = GameResult(
            player_id=1,
            difficulty="easy",
            score=45,
            max_score=50,
            duration=120.5,
            created_at=datetime.now(),
        )

        result_id = repo.insert_game_result(result)
        assert result_id > 0

    def test_get_leaderboard_empty(self, repo):
        """Test getting leaderboard when empty."""
        leaderboard = repo.get_leaderboard()
        assert leaderboard == []

    def test_get_player_game_history_empty(self, repo):
        """Test getting game history when empty."""
        history = repo.get_player_game_history(player_id=999)
        assert history == []

    def test_insert_multiple_results(self, repo):
        """Test inserting multiple game results."""
        for i in range(5):
            result = GameResult(
                player_id=i,
                difficulty="easy",
                score=40 + i,
                max_score=50,
                duration=100.0 + i,
                created_at=datetime.now(),
            )
            repo.insert_game_result(result)

        # Get a specific player's history
        history = repo.get_player_game_history(player_id=1)
        assert len(history) >= 1
