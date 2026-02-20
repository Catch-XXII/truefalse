"""Game result tracking and statistics."""

import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.player import Player


@dataclass
class GameResult:
    """Represents the result of a single game session."""

    player_id: int
    difficulty: str
    score: int
    max_score: int
    duration: float
    created_at: datetime.datetime

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage.

        Returns:
            Accuracy as a percentage (0-100)
        """
        if self.max_score == 0:
            return 0.0
        return (self.score / self.max_score) * 100

    def __str__(self) -> str:
        """Return formatted game result."""
        return (
            f"GameResult(difficulty={self.difficulty}, "
            f"score={self.score}/{self.max_score}, "
            f"accuracy={self.accuracy:.1f}%, "
            f"duration={self.duration:.2f}s)"
        )
