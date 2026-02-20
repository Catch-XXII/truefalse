"""Integration tests for the complete game flow."""

import pytest
from datetime import datetime

from models.player import Player
from config import EASY
from game.engine import GameEngine
from db.operations import PlayerRepository, GameResultRepository
from models.game_result import GameResult


class TestIntegration:
    """Integration tests for game components."""

    def test_full_player_creation_workflow(self, temp_db):
        """Test complete player creation workflow."""
        repo = PlayerRepository(temp_db)

        # Create player
        player_id = repo.insert_player(
            name="Integration Test Player",
            email="integration@test.com",
            age=30,
            phone="555-555-5555",
            date=datetime.now(),
        )

        # Verify player was created
        player = repo.find_player_by_id(player_id)
        assert player is not None
        assert player["email"] == "integration@test.com"

        # Verify can find by email
        player_by_email = repo.find_player_by_email("integration@test.com")
        assert player_by_email["id"] == player_id

    def test_game_creation_and_scoring(self):
        """Test game creation and basic scoring logic."""
        player = Player(
            name="Test Player",
            email="test@example.com",
            age=25,
            phone="555-123-4567",
            date=datetime.now(),
        )

        engine = GameEngine(player, EASY)

        # Game should start with score 0
        assert engine.get_score() == 0
        assert not engine.is_game_finished()

        # Game state tracking
        assert engine.get_max_possible_score() == 50

    def test_game_result_persistence(self, temp_db):
        """Test saving and retrieving game results."""
        result_repo = GameResultRepository(temp_db)

        # Create and save game result
        result = GameResult(
            player_id=1,
            difficulty="easy",
            score=45,
            max_score=50,
            duration=125.5,
            created_at=datetime.now(),
        )

        result_id = result_repo.insert_game_result(result)
        assert result_id > 0

        # Retrieve and verify
        history = result_repo.get_player_game_history(player_id=1)
        assert len(history) == 1
        assert history[0]["score"] == 45
        assert history[0]["max_score"] == 50

    def test_multiple_players_and_leaderboard(self, temp_db):
        """Test multiple players and leaderboard functionality."""
        player_repo = PlayerRepository(temp_db)
        result_repo = GameResultRepository(temp_db)

        # Create multiple players
        players = []
        for i in range(3):
            player_id = player_repo.insert_player(
                name=f"Player {i+1}",
                email=f"player{i+1}@test.com",
                age=20 + i,
                phone=f"555-111-{1000+i}",
                date=datetime.now(),
            )
            players.append(player_id)

        # Add game results for each player
        for i, player_id in enumerate(players):
            result = GameResult(
                player_id=player_id,
                difficulty="easy",
                score=30 + i * 5,
                max_score=50,
                duration=120.0,
                created_at=datetime.now(),
            )
            result_repo.insert_game_result(result)

        # Get leaderboard
        leaderboard = result_repo.get_leaderboard(limit=10)
        assert len(leaderboard) >= 3
        # Should be sorted by best score descending
        for i in range(len(leaderboard) - 1):
            assert leaderboard[i]["best_score"] >= leaderboard[i + 1]["best_score"]

    def test_player_model_validation(self):
        """Test Player model comprehensive validation."""
        # Valid player
        player = Player(
            name="Valid Player",
            email="valid@example.com",
            age="25",  # String should be converted
            phone="555-123-4567",
        )

        assert player.age == 25
        assert isinstance(player.age, int)

        # Invalid age should raise error
        with pytest.raises(ValueError):
            Player(
                name="Invalid Age",
                email="test@example.com",
                age="not_a_number",
                phone="555-123-4567",
            )

        # Invalid email should raise error
        with pytest.raises(ValueError):
            Player(
                name="Invalid Email",
                email="not_an_email",
                age=25,
                phone="555-123-4567",
            )

    def test_game_answer_validation(self):
        """Test game answer validation and parsing."""
        player = Player(
            name="Test",
            email="test@example.com",
            age=25,
            phone="555-123-4567",
        )

        engine = GameEngine(player, EASY)

        # Valid answers
        assert engine._parse_answer("T") is True
        assert engine._parse_answer("F") is False
        assert engine._parse_answer("TRUE") is True
        assert engine._parse_answer("FALSE") is False

        # Invalid answers
        with pytest.raises(ValueError):
            engine._parse_answer("MAYBE")

        with pytest.raises(ValueError):
            engine._parse_answer("1")

    def test_game_progress_accuracy(self):
        """Test game result accuracy calculation."""
        # Perfect score
        result_perfect = GameResult(
            player_id=1,
            difficulty="easy",
            score=50,
            max_score=50,
            duration=100.0,
            created_at=datetime.now(),
        )
        assert result_perfect.accuracy == 100.0

        # Half score
        result_half = GameResult(
            player_id=1,
            difficulty="easy",
            score=25,
            max_score=50,
            duration=100.0,
            created_at=datetime.now(),
        )
        assert result_half.accuracy == 50.0

        # Zero score
        result_zero = GameResult(
            player_id=1,
            difficulty="easy",
            score=0,
            max_score=50,
            duration=100.0,
            created_at=datetime.now(),
        )
        assert result_zero.accuracy == 0.0
