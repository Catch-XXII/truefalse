"""Core game engine for managing game flow and scoring."""

from typing import TYPE_CHECKING

from config import DifficultyLevel
from game.question import generate_question

if TYPE_CHECKING:
    from models.player import Player


class GameEngine:
    """Manages a single game session and scoring logic."""

    def __init__(self, player: "Player", difficulty: DifficultyLevel) -> None:
        """Initialize the game engine.

        Args:
            player: The Player instance playing the game
            difficulty: The DifficultyLevel for this game
        """
        self.player = player
        self.difficulty = difficulty
        self.score = 0
        self.current_question_index = 0
        self.total_questions = difficulty.num_questions

    def play_round(self, user_answer: str) -> bool:
        """Play a single round of the game.

        Args:
            user_answer: "T" or "F" or "True" or "False"

        Returns:
            True if the answer was correct, False otherwise

        Raises:
            ValueError: If user_answer is not valid
        """
        if self.current_question_index >= self.total_questions:
            raise RuntimeError("Game already finished")

        question = generate_question()
        answer_bool = self._parse_answer(user_answer)

        is_correct = question.is_correct(answer_bool)

        if is_correct:
            self.score += self.difficulty.score_per_correct
        else:
            self.score = max(0, self.score - self.difficulty.score_penalty)

        self.current_question_index += 1
        return is_correct

    def get_current_question(self) -> str:
        """Get the current question as a string.

        Returns:
            The question string (e.g., "45<67")
        """
        return str(generate_question())

    def get_score(self) -> int:
        """Get the current score.

        Returns:
            Current score
        """
        return self.score

    def get_max_possible_score(self) -> int:
        """Get the maximum possible score for this game.

        Returns:
            Maximum possible score based on getting all questions correct
        """
        return self.total_questions * self.difficulty.score_per_correct

    def is_game_finished(self) -> bool:
        """Check if the game is finished.

        Returns:
            True if all questions have been asked
        """
        return self.current_question_index >= self.total_questions

    def get_progress(self) -> tuple[int, int]:
        """Get game progress.

        Returns:
            Tuple of (current_question_index, total_questions)
        """
        return (self.current_question_index, self.total_questions)

    @staticmethod
    def _parse_answer(answer: str) -> bool:
        """Parse user answer into boolean.

        Args:
            answer: User input (T, F, True, False, etc.)

        Returns:
            True or False

        Raises:
            ValueError: If answer is not recognized
        """
        normalized = answer.strip().upper()

        if normalized in ("T", "TRUE"):
            return True
        elif normalized in ("F", "FALSE"):
            return False
        else:
            raise ValueError(f"Invalid answer: {answer}. Please enter T/F or True/False")
