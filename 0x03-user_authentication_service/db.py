#!/usr/bin/env python3
"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class to manage database interactions"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine(
            "sqlite:///a.db",
            echo=False,
            connect_args={"check_same_thread": False}
        )
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            User: The User object that was added to the database.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The first user found matching the criteria.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If the query arguments are invalid.
        """
        # Define valid keys corresponding to User model attributes
        valid_keys = (
            'id', 'email', 'hashed_password', 'session_id', 'reset_token')
        for key in kwargs.keys():
            if key not in valid_keys:
                raise InvalidRequestError

        # Perform the query and handle no result scenario
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes in the database.
        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the
            attributes to update.
        Returns:
            None
        Raises:
            ValueError: If an attribute in kwargs does not exist
        """
        # Use find_user_by to locate the user by their ID
        user = self.find_user_by(id=user_id)

        # Iterate over the kwargs and update the user's attributes
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
