#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt
from db import DB, User
from bcrypt import hashpw, gensalt, checkpw
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password as bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def _generate_uuid(self) -> str:
        """Generate a new UUID."""
        return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize an Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user in the authentication system.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User doesn't exist; proceed with registration
            hashed_password = _hash_password(password)
            user = self._db.add_user(
                email=email, hashed_password=hashed_password.decode('utf-8'))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's login by checking their email and password.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the user exists and the password matches,
                  otherwise False.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
            # Check if the password matches the hashed password stored in the DB
            if checkpw(password.encode(
                    'utf-8'), user.hashed_password.encode('utf-8')):
                return True
            else:
                return False
        except NoResultFound:
            # If the user does not exist, return False
            return False
