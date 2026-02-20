"""Test suite for game/__init__.py."""

import pytest

from game.question import Question, generate_question


class TestQuestion:
    """Test Question class."""

    def test_question_string_representation(self):
        """Test question string format."""
        q = Question(45, "<", 67)
        assert str(q) == "45<67"

    def test_less_than_correct(self):
        """Test < operator with correct answer."""
        q = Question(45, "<", 67)
        assert q.is_correct(True) is True
        assert q.is_correct(False) is False

    def test_less_than_incorrect(self):
        """Test < operator with incorrect answer."""
        q = Question(67, "<", 45)
        assert q.is_correct(True) is False
        assert q.is_correct(False) is True

    def test_equals_correct(self):
        """Test = operator with correct answer."""
        q = Question(42, "=", 42)
        assert q.is_correct(True) is True
        assert q.is_correct(False) is False

    def test_equals_incorrect(self):
        """Test = operator with incorrect answer."""
        q = Question(42, "=", 43)
        assert q.is_correct(True) is False
        assert q.is_correct(False) is True

    def test_greater_than_correct(self):
        """Test > operator with correct answer."""
        q = Question(100, ">", 50)
        assert q.is_correct(True) is True
        assert q.is_correct(False) is False

    def test_greater_than_incorrect(self):
        """Test > operator with incorrect answer."""
        q = Question(50, ">", 100)
        assert q.is_correct(True) is False
        assert q.is_correct(False) is True


class TestQuestionGeneration:
    """Test question generation."""

    def test_generate_question(self):
        """Test that generate_question creates valid questions."""
        q = generate_question()
        assert isinstance(q, Question)
        assert 1 <= q.left <= 100
        assert 1 <= q.right <= 100
        assert q.operator in ("<", "=", ">")

    def test_generate_multiple_questions(self):
        """Test generating multiple questions."""
        questions = [generate_question() for _ in range(100)]
        assert len(questions) == 100
        assert all(isinstance(q, Question) for q in questions)

        # Check distribution of operators
        operators = [q.operator for q in questions]
        assert "<" in operators
        assert "=" in operators
        assert ">" in operators
