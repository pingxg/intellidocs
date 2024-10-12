"""
This module provides functions for user management in a Streamlit application, 
including creating, fetching, updating, and deleting user records in the database.
"""

from typing import List, Optional
from database.models import User
from database.session import get_db
import streamlit_authenticator as stauth
from uuid import UUID

class UserService:
    @staticmethod
    def create_user(
        username: str, 
        email: str, 
        password: str, 
        user_group_id: Optional[UUID] = None) -> User:
        """
        Creates a new user in the database.

        Parameters:
        username (str): The username of the new user.
        email (str): The email address of the new user.
        password (str): The password for the new user.
        user_group_id (Optional[UUID]): The ID of the user group to assign the user to.

        Returns:
        User: The created User object.
        """
        with get_db() as db:
            hashed_password = stauth.Hasher([password]).generate()[0]
            new_user = User(
                username=username,
                email=email, 
                password=hashed_password, 
                user_group_id=user_group_id
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

    @staticmethod
    def fetch_all_users() -> List[User]:
        """
        Retrieves all users from the database.

        Returns:
        List[User]: A list of User objects.
        """
        with get_db() as db:
            return db.query(User).order_by(User.username).all()

    @staticmethod
    def get_user_by_id(user_id: UUID) -> Optional[User]:
        """
        Retrieves a user by their ID.

        Parameters:
        user_id (UUID): The ID of the user to retrieve.

        Returns:
        Optional[User]: The User object if found, otherwise None.
        """
        with get_db() as db:
            return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def update_user(
        user_id: UUID,
        username: Optional[str] = None, 
        email: Optional[str] = None, 
        password: Optional[str] = None, 
        user_group_id: Optional[UUID] = None) -> Optional[User]:
        """
        Updates an existing user's information.

        Parameters:
        user_id (UUID): The ID of the user to update.
        username (Optional[str]): The new username for the user (if provided).
        email (Optional[str]): The new email for the user (if provided).
        password (Optional[str]): The new password for the user (if provided).
        user_group_id (Optional[UUID]): The new user group ID for the user (if provided).

        Returns:
        Optional[User]: The updated User object if the user was found and updated, otherwise None.
        """
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                if username:
                    user.username = username
                if email:
                    user.email = email
                if password:
                    hashed_password = stauth.Hasher([password]).generate()[0]
                    user.password = hashed_password
                if user_group_id is not None:
                    user.user_group_id = user_group_id
                db.commit()
                db.refresh(user)
            return user

    @staticmethod
    def delete_user(user_id: UUID) -> bool:
        """
        Deletes a user from the database.

        Parameters:
        user_id (UUID): The ID of the user to delete.

        Returns:
        bool: True if the user was deleted, otherwise False.
        """
        with get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                db.delete(user)
                db.commit()
                return True
            return False

    @staticmethod
    def fetch_users_by_group(user_group_id: UUID) -> List[User]:
        """
        Retrieves all users belonging to a specific user group.

        Parameters:
        user_group_id (UUID): The ID of the user group.

        Returns:
        List[User]: A list of User objects belonging to the specified group.
        """
        with get_db() as db:
            return db.query(User).filter(User.user_group_id == user_group_id).all()
