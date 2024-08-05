from const import RE_EMAIL, RE_PHONE
import datetime
import re


class Player:
    def __init__(self, name, email, age, phone, score, date) -> None:
        self._name = name
        self._email = email
        self._age = age
        self._phone = phone
        self._score = score
        self._date = date

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value:
            raise ValueError("Email cannot be empty.")
        if not re.match(RE_EMAIL, value):
            raise ValueError("Invalid email format.")
        self._email = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Age must be a positive integer.")
        self._age = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if not value:
            raise ValueError("Phone number cannot be empty.")
        if not re.match(RE_PHONE, value):
            raise ValueError("Invalid phone number format.")
        self._phone = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError("Score must be an integer.")
        self._score = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, datetime.datetime):
            raise ValueError("Date must be a datetime object.")
        self._date = value
