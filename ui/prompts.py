"""User prompts and input handling."""

import re
from typing import Optional

from const import RE_EMAIL, RE_PHONE
from ui.display import print_error, print_info


def get_player_name() -> str:
    """Prompt for and get player name.

    Returns:
        Validated player name
    """
    while True:
        name = input("Enter your name: ").strip()
        if not name:
            print_error("Name cannot be empty")
            continue
        if len(name) > 50:
            print_error("Name must be 50 characters or less")
            continue
        return name


def get_player_email() -> str:
    """Prompt for and get player email.

    Returns:
        Validated email address
    """
    while True:
        email = input("Enter your email: ").strip().lower()
        if not re.match(RE_EMAIL, email):
            print_error("Not a valid email address")
            continue
        return email


def get_player_age() -> int:
    """Prompt for and get player age.

    Returns:
        Validated age as integer
    """
    while True:
        try:
            age_str = input("Enter your age: ").strip()
            age = int(age_str)
            if age <= 0 or age > 150:
                print_error("Age must be between 1 and 150")
                continue
            return age
        except ValueError:
            print_error("Age must be a valid number")
            continue


def get_player_phone() -> str:
    """Prompt for and get player phone number.

    Returns:
        Validated phone number
    """
    while True:
        phone = input("Enter your phone number: ").strip()
        if not re.match(RE_PHONE, phone):
            print_error("Not a valid phone number")
            continue
        return phone


def get_true_false_answer() -> bool:
    """Prompt for and get True/False answer.

    Returns:
        True or False based on user input

    Raises:
        ValueError: If input is invalid after max retries
    """
    max_retries = 3
    for attempt in range(max_retries):
        answer = input("Your answer (T/F): ").strip().upper()

        if answer in ("T", "TRUE"):
            return True
        elif answer in ("F", "FALSE"):
            return False
        else:
            if attempt < max_retries - 1:
                print_error(f"Invalid answer. Please enter T or F (Retry {attempt + 1}/{max_retries})")
            else:
                raise ValueError(f"Invalid answer after {max_retries} attempts")

    raise ValueError("Could not get valid answer")


def select_menu_option(options: list[str]) -> int:
    """Prompt user to select from a menu.

    Args:
        options: List of menu options

    Returns:
        Index of selected option (0-based)
    """
    while True:
        print("\n" + "-" * 40)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("-" * 40)

        choice = input("Select option: ").strip()

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num - 1
            else:
                print_error(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print_error("Please enter a valid number")


def confirm_action(message: str) -> bool:
    """Prompt user to confirm an action.

    Args:
        message: Confirmation message

    Returns:
        True if user confirms, False otherwise
    """
    while True:
        response = input(f"{message} (Y/N): ").strip().upper()
        if response in ("Y", "YES"):
            return True
        elif response in ("N", "NO"):
            return False
        else:
            print_error("Please enter Y or N")


def select_difficulty() -> str:
    """Prompt user to select game difficulty.

    Returns:
        Difficulty name: "easy", "medium", or "hard"
    """
    options = ["Easy (5 questions)", "Medium (9 questions)", "Hard (15 questions)"]
    index = select_menu_option(options)
    difficulties = ["easy", "medium", "hard"]
    return difficulties[index]
