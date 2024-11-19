#!/usr/bin/env python3
"""
SQLAlchemy model definition for the `users` table.
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    User model for the `users` table.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        email (str): Non-nullable string for the user's email.
        hashed_password (str): Non-nullable str for the user's hashed pswrd.
        session_id (str): Nullable string for the user's session ID.
        reset_token (str): Nullable str for the user's pswrd reset token.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    session_id = Column(String(255), nullable=True)
    reset_token = Column(String(255), nullable=True)
