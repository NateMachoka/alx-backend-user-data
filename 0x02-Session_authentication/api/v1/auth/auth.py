#!/usr/bin/env python3
""" Auth class for managing API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A template class for authentication management"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Returns:
        - True if path is None
        - True if excluded_paths is None or empty
        - False if path is in excluded_paths (slash tolerant)
        """
        if path is None:
            return True

        if not excluded_paths:
            return True

        # Normalize path to be slash tolerant
        normalized_path = path if path.endswith('/') else f"{path}/"

        for excluded_path in excluded_paths:
            # Normalize excluded_path
            normalized_excluded = excluded_path if excluded_path.endswith(
                '/') else f"{excluded_path}/"

            # Handle wildcard '*' at the end of excluded_path
            if normalized_excluded.endswith("*/"):
                # Match if path starts with the prefix before '*'
                prefix = normalized_excluded[:-2]
                if normalized_path.startswith(prefix):
                    return False
            elif normalized_path == normalized_excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the Authorization header from the request if present """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user associated with the request """
        return None
