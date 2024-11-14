#!/usr/bin/env python3
"""
SessionAuth module for handling session-based authentication
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """ Session authentication class that inherits from Aut
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for a user_id
           stores it in user_id_by_session_id.
        Args:
            user_id (str): The ID of the user to create a session for.
        Returns:
            str: The generated session ID, None if user_id is None or not str
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # generate a unique session id
        session_id = str(uuid.uuid4())

        # Store the session ID with the corresponding user_id
        self.user_id_by_session_id[session_id] = user_id

        return session_id
