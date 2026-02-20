"""Question generation and representation."""

import random
from dataclasses import dataclass

from config import OPERATORS, MIN_NUMBER, MAX_NUMBER


@dataclass
class Question:
    """Represents a single true/false question."""

    left: int
    operator: str
    right: int

    def __str__(self) -> str:
        """Return the question as a string."""
        return f"{self.left}{self.operator}{self.right}"

    def is_correct(self, answer: bool) -> bool:
        """Check if the given answer is correct.

        Args:
            answer: True or False

        Returns:
            True if answer is correct, False otherwise
        """
        if self.operator == "<":
            return (self.left < self.right) == answer
        elif self.operator == "=":
            return (self.left == self.right) == answer
        elif self.operator == ">":
            return (self.left > self.right) == answer
        return False


def generate_question() -> Question:
    """Generate a random true/false question.

    Returns:
        A Question instance with random values
    """
    left = random.randint(MIN_NUMBER, MAX_NUMBER)
    operator = random.choice(OPERATORS)
    right = random.randint(MIN_NUMBER, MAX_NUMBER)

    return Question(left, operator, right)
