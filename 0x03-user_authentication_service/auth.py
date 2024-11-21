#!/usr/bin/env python3
"""
Authentication module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password string using bcrypt and return the salted hash.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password as a byte string.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    # Generate a salted hash using bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
