#!/usr/bin/env python3
"""Session Authenticatioon with persistence"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session-based authentication with database persistence."""

    def create_session(self, user_id=None):
        """Create a session and save it to the database."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create a new UserSession instance and save it
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve the user_id based on session_id from the database."""
        if session_id is None:
            return None

        # Retrieve UserSession from database by session_id
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None

        # Check expiration (using the superclass method)
        session = sessions[0]
        if self.session_duration <= 0:
            return session.user_id

        if session.created_at is None:
            return None

        # Check if session expired
        from datetime import datetime, timedelta
        expiration_time = session.created_at + timedelta(
            seconds=self.session_duration)
        if datetime.now() > expiration_time:
            session.remove()  # Remove expired session
            return None

        return session.user_id

    def destroy_session(self, request=None):
        """Destroy the session from the database."""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Find and delete session from the database
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False

        # Remove the session from the file-based database
        session = sessions[0]
        session.remove()
        return True
