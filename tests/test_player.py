"""Unit tests for game engine logic."""

import pytest
from datetime import datetime

from config import EASY, MEDIUM, HARD
from game.engine import GameEngine
from models.player import Player


class TestGameEngine:
    """Test GameEngine class."""

    @pytest.fixture
    def player(self):
        """Create a test player."""
        return Player(
            name="Test Player",
            email="test@example.com",
            age=25,
            phone="555-123-4567",
            date=datetime.now(),
        )

    def test_engine_initialization(self, player):
        """Test GameEngine initialization."""
        engine = GameEngine(player, EASY)

        assert engine.player == player
        assert engine.difficulty == EASY
        assert engine.score == 0
        assert engine.current_question_index == 0
        assert engine.total_questions == 5

    def test_game_not_finished_initially(self, player):
        """Test that game is not finished initially."""
        engine = GameEngine(player, EASY)
        assert engine.is_game_finished() is False

    def test_progress_tracking(self, player):
        """Test progress tracking."""
        engine = GameEngine(player, EASY)
        assert engine.get_progress() == (0, 5)

    def test_max_possible_score(self, player):
        """Test max possible score calculation."""
        engine_easy = GameEngine(player, EASY)
        assert engine_easy.get_max_possible_score() == 50  # 5 * 10

        engine_medium = GameEngine(player, MEDIUM)
        assert engine_medium.get_max_possible_score() == 45  # 9 * 5

        engine_hard = GameEngine(player, HARD)
        assert engine_hard.get_max_possible_score() == 45  # 15 * 3

    def test_parse_answer_valid(self, player):
        """Test parsing valid answers."""
        engine = GameEngine(player, EASY)

        assert engine._parse_answer("T") is True
        assert engine._parse_answer("t") is True
        assert engine._parse_answer("TRUE") is True
        assert engine._parse_answer("true") is True
        assert engine._parse_answer("True") is True

        assert engine._parse_answer("F") is False
        assert engine._parse_answer("f") is False
        assert engine._parse_answer("FALSE") is False
        assert engine._parse_answer("false") is False
        assert engine._parse_answer("False") is False

    def test_parse_answer_with_whitespace(self, player):
        """Test parsing answers with whitespace."""
        engine = GameEngine(player, EASY)

        assert engine._parse_answer("  T  ") is True
        assert engine._parse_answer("  F  ") is False

    def test_parse_answer_invalid(self, player):
        """Test parsing invalid answers raises error."""
        engine = GameEngine(player, EASY)

        with pytest.raises(ValueError):
            engine._parse_answer("X")

        with pytest.raises(ValueError):
            engine._parse_answer("maybe")

        with pytest.raises(ValueError):
            engine._parse_answer("1")

    def test_get_score(self, player):
        """Test score getter."""
        engine = GameEngine(player, EASY)
        assert engine.get_score() == 0

    def test_difficulty_levels(self, player):
        """Test different difficulty levels."""
        engine_easy = GameEngine(player, EASY)
        assert engine_easy.difficulty.score_per_correct == 10
        assert engine_easy.difficulty.score_penalty == 5

        engine_medium = GameEngine(player, MEDIUM)
        assert engine_medium.difficulty.score_per_correct == 5
        assert engine_medium.difficulty.score_penalty == 5

        engine_hard = GameEngine(player, HARD)
        assert engine_hard.difficulty.score_per_correct == 3
        assert engine_hard.difficulty.score_penalty == 2
