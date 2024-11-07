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
