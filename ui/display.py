"""Colored output utilities using colorama."""

import os
import sys
from typing import Optional

try:
    from colorama import Fore, Back, Style, init
except ImportError:
    # Graceful degradation if colorama not available
    class Fore:  # type: ignore
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        CYAN = ""
        WHITE = ""

    class Back:  # type: ignore
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""

    class Style:  # type: ignore
        BRIGHT = ""
        RESET_ALL = ""

    def init(*args, **kwargs):  # type: ignore
        pass


init(autoreset=True)


def supports_color() -> bool:
    """Check if terminal supports color.

    Returns:
        True if color is supported
    """
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    # Check for common terminals that don't support color
    if os.environ.get("TERM") == "dumb":
        return False
    return True


def print_header(text: str) -> None:
    """Print a header message with styling.

    Args:
        text: Header text to print
    """
    print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.CYAN}{text.center(50)}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")


def print_success(text: str) -> None:
    """Print a success message.

    Args:
        text: Success message to print
    """
    print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")


def print_error(text: str) -> None:
    """Print an error message.

    Args:
        text: Error message to print
    """
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")


def print_warning(text: str) -> None:
    """Print a warning message.

    Args:
        text: Warning message to print
    """
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")


def print_info(text: str) -> None:
    """Print an info message.

    Args:
        text: Info message to print
    """
    print(f"{Fore.BLUE}ℹ {text}{Style.RESET_ALL}")


def print_question(question: str, question_number: int, total_questions: int) -> None:
    """Print a formatted question.

    Args:
        question: The question string
        question_number: Current question number
        total_questions: Total questions in game
    """
    progress = f"[{question_number}/{total_questions}]"
    print(f"\n{Fore.YELLOW}{progress} {Style.BRIGHT}{question}{Style.RESET_ALL}")


def print_score(score: int, message: str = "") -> None:
    """Print the current score.

    Args:
        score: Current score
        message: Optional message to append
    """
    text = f"Score: {score}"
    if message:
        text += f" - {message}"
    print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")


def print_leaderboard(rows: list[dict]) -> None:
    """Print leaderboard in formatted table.

    Args:
        rows: List of leaderboard entries with rank, name, best_score, etc.
    """
    print_header("LEADERBOARD")

    # Print table header
    header = f"{'Rank':<6} {'Name':<20} {'Best Score':<12} {'Avg Score':<12} {'Games':<8}"
    print(f"{Fore.CYAN}{Style.BRIGHT}{header}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")

    # Print rows
    for row in rows:
        rank_str = f"#{row['rank']:<4}"
        name_str = row["name"][:19].ljust(20)
        best_score = str(row["best_score"] or 0).ljust(12)
        avg_score = f"{(row['avg_score'] or 0):.1f}".ljust(12)
        games = str(row["games_played"] or 0).ljust(8)

        line = f"{rank_str} {name_str} {best_score} {avg_score} {games}"
        print(line)

    print()


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")
