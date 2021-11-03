# CircleTable — Christopher Liu, Yusuf Elsharawy, Deven Maheshwari, Naomi Naranjo
# SoftDev
# P00: CircleStories

"""Authentication

Handles all of the login/registration functionality for CircleStories
including input validation.
"""

import re
import sqlite3

DB_FILE = "circlestories.db"


def validate_user(
    username: str, email: str, password: str, password_check: str
) -> list:
    """Validates input for new user creation."""

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    errors = []
    if len(username) == 0:
        errors.append("Username is required")
    if (
        c.execute(
            "SELECT * FROM users WHERE username=:username", {"username": username}
        ).fetchone()
        is not None
    ):
        errors.append("Username already in use")

    if len(email) == 0:
        errors.append("Email is required")
    if (
        c.execute("SELECT * FROM users WHERE email=:email", {"email": email}).fetchone()
        is not None
    ):
        errors.append("Email already in use")

    if len(password) == 0:
        errors.append("Password is required")
    if len(password_check) == 0:
        errors.append("Repeat password is required")

    # Makes sure email is in the form something@something.something
    if not re.fullmatch(r"\S+@\S+\.\S+", email):
        errors.append("A valid email address is required")

    if password != password_check:
        errors.append("Passwords must match")

    return errors


def create_user(username: str, email: str, password: str, password_check: str) -> list:
    """Validates inputs and creates a new user if all inputs are valid."""

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            user_id     TEXT PRIMARY KEY DEFAULT (hex(randomblob(8))),
            username    TEXT,
            email       TEXT,
            password    TEXT
        )
    """
    )

    errors = validate_user(username, email, password, password_check)
    if not errors:
        c.execute(
            "INSERT INTO users(username, email, password) VALUES (?, ?, ?)",
            (username, email, password),
        )

    db.commit()
    db.close()

    return errors


def authenticate_user(username: str, password: str) -> bool:
    """Authenticates a user using the given credentials."""

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if not c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users';"
    ).fetchone():
        return False

    user_pw = c.execute(
        "SELECT password FROM users WHERE username=:username", {"username": username}
    ).fetchone()
    if user_pw is not None and user_pw[0] == password:
        return True

    return False
