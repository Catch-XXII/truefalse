"""Game configuration and difficulty levels."""

from dataclasses import dataclass
from typing import Final


@dataclass
class DifficultyLevel:
    """Defines a difficulty level for the game."""

    name: str
    num_questions: int
    score_per_correct: int
    score_penalty: int


# Difficulty level definitions
EASY: Final[DifficultyLevel] = DifficultyLevel(
    name="Easy",
    num_questions=5,
    score_per_correct=10,
    score_penalty=5,
)

MEDIUM: Final[DifficultyLevel] = DifficultyLevel(
    name="Medium",
    num_questions=9,
    score_per_correct=5,
    score_penalty=5,
)

HARD: Final[DifficultyLevel] = DifficultyLevel(
    name="Hard",
    num_questions=15,
    score_per_correct=3,
    score_penalty=2,
)

DIFFICULTY_LEVELS: Final[dict[str, DifficultyLevel]] = {
    "easy": EASY,
    "medium": MEDIUM,
    "hard": HARD,
}

# Game constants
MIN_NUMBER: Final[int] = 1
MAX_NUMBER: Final[int] = 100
OPERATORS: Final[list[str]] = ["<", "=", ">"]
