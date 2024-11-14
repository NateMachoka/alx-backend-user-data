#!/usr/bin/env python3
"""Session class"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class to add expiration to session IDs."""

    def __init__(self):
        """Initialize session expiration with a duration."""
        super().__init__()

        # Set session duration from environment variable
        try:
            self.session_duration = int(
                os.getenv("SESSION_DURATION", "0"))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with an expiration timestamp."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store session information with creation time
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user_id based on session ID and check if it is expired."""
        if session_id is None:
            return None

        # Check if session exists
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        # No expiration if session_duration is 0 or less
        if self.session_duration <= 0:
            return session_dict.get("user_id")

        # Validate session expiration
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        # Calculate expiration time
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            # Session expired, remove it
            del self.user_id_by_session_id[session_id]
            return None

        return session_dict.get("user_id")
