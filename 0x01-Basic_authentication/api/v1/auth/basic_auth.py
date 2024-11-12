#!/usr/bin/env python3
"""Basic Authentication class"""

import base64
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class for basic authentication """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header fo
        Basic Authentication.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        # Return the part after "Basic "
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a Base64 string (base64_authorization_header) to UTF-8 string.
        Return None if base64_authorization_header is None, not a string, or
        if it is not a valid Base64 encoding.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to a UTF-8 string
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            # Return None if decoding fails
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 authorization header.
        Returns:
            tuple: (user_email, user_password) if successful,
        otherwise (None, None).
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        # Split on the first occurrence of ':'
        user_email, user_password = decoded_base64_authorization_header.split(
            ":", 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on email and password.
         Args:
            user_email (str): The email of the user.
            user_pwd (str): The user's password.
        Returns:
            User instance if email and password are valid, else None.
        """
        # Check if user_email and user_pwd are valid
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        users = User.search({'email': user_email})
        if not users:
            return None  # No user with given email found

        user = users[0]  # Assume only one user with the given email

        # Validate password
        if not user.is_valid_password(user_pwd):
            return None

        # Return the user instance if credentials are valid
        return user
