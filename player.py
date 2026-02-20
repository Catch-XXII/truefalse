"""Player model and validation."""

import datetime
import re
from typing import Optional

from const import RE_EMAIL, RE_PHONE


class Player:
    """Represents a game player with profile information."""

    def __init__(
        self,
        name: str,
        email: str,
        age: int | str,
        phone: str,
        score: int = 0,
        date: Optional[datetime.datetime] = None,
    ) -> None:
        """Initialize a Player.

        Args:
            name: Player's name
            email: Player's email
            age: Player's age (int or string that converts to int)
            phone: Player's phone number
            score: Player's current score (default 0)
            date: Registration date (default now)

        Raises:
            ValueError: If any validation fails
        """
        self.name = name
        self.email = email
        self.age = age
        self.phone = phone
        self.score = score
        self.date = date if date else datetime.datetime.now()

    @property
    def name(self) -> str:
        """Get player name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set player name with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Name cannot be empty and must be a string.")
        self._name = value.strip()

    @property
    def email(self) -> str:
        """Get player email."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Set player email with validation."""
        if not value:
            raise ValueError("Email cannot be empty.")
        if not re.match(RE_EMAIL, value):
            raise ValueError("Invalid email format.")
        self._email = value.lower()

    @property
    def age(self) -> int:
        """Get player age."""
        return self._age

    @age.setter
    def age(self, value: int | str) -> None:
        """Set player age with validation."""
        try:
            age_int = int(value) if isinstance(value, str) else value
        except (ValueError, TypeError):
            raise ValueError("Age must be a number.")

        if age_int <= 0 or age_int > 150:
            raise ValueError("Age must be between 1 and 150.")
        self._age = age_int

    @property
    def phone(self) -> str:
        """Get player phone."""
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """Set player phone with validation."""
        if not value:
            raise ValueError("Phone number cannot be empty.")
        if not re.match(RE_PHONE, value):
            raise ValueError("Invalid phone number format.")
        self._phone = value

    @property
    def score(self) -> int:
        """Get player score."""
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        """Set player score with validation."""
        if not isinstance(value, int):
            raise ValueError("Score must be an integer.")
        if value < 0:
            raise ValueError("Score cannot be negative.")
        self._score = value

    @property
    def date(self) -> datetime.datetime:
        """Get player registration date."""
        return self._date

    @date.setter
    def date(self, value: datetime.datetime) -> None:
        """Set player registration date with validation."""
        if not isinstance(value, datetime.datetime):
            raise ValueError("Date must be a datetime object.")
        self._date = value

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Player(name={self.name!r}, email={self.email!r}, age={self.age}, score={self.score})"
