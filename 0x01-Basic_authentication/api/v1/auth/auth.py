#!/usr/bin/env python3
""" Auth class for managing API authentication
"""
from flask import request
from typing import List, TypeVar

class Auth:
    """A template class for authentication management"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if the path requires authentication """
        return False

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header from the request """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user associated with the request """
        return None
