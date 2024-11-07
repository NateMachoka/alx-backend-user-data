#!/usr/bin/env python3

"""Contains excrypting functions"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a randomly generated salt.
    Args:
        password (str): The password to hash.
    Returns:
        bytes: The salted, hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.
    Args:
        hashed_password (bytes): The previously hashed password.
        password (str): The plain-text password to validate.
    Returns:
        bool: True if the password is valid, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
