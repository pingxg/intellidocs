"""
This module handles user authentication for a Streamlit dashboard using 
streamlit_authenticator. It includes functions to authenticate users, 
manage the authentication flow, and interact with a custom database query.
"""

from typing import List, Optional
import streamlit as st
import streamlit_authenticator as stauth
from config.config import ST_SECRET_KEY
from database.models import User
from database.session import get_db


def create_user(username: str, email: str, password: str) -> User:
    """
    Creates a new user in the database.

    Parameters:
    username (str): The username of the new user.
    email (str): The email address of the new user.
    password (str): The password for the new user.

    Returns:
    User: The created User object.
    """
    with get_db() as db:
        new_user = User(username=username, email=email, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


def get_all_users() -> List[User]:
    """
    Retrieves all users from the database.

    Returns:
    List[User]: A list of User objects.
    """
    with get_db() as db:
        return db.query(User).all()


def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Retrieves a user by their ID.

    Parameters:
    user_id (int): The ID of the user to retrieve.

    Returns:
    Optional[User]: The User object if found, otherwise None.
    """
    with get_db() as db:
        return db.query(User).filter(User.id == user_id).first()


def update_user(user_id: int, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
    """
    Updates an existing user's information.

    Parameters:
    user_id (int): The ID of the user to update.
    username (Optional[str]): The new username for the user (if provided).
    email (Optional[str]): The new email for the user (if provided).
    password (Optional[str]): The new password for the user (if provided).

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
                user.password = password
            db.commit()
            db.refresh(user)
        return user


def delete_user(user_id: int) -> bool:
    """
    Deletes a user from the database.

    Parameters:
    user_id (int): The ID of the user to delete.

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


def user_authentication(user_list=None):
    """
    Handles user authentication using streamlit_authenticator.

    Parameters:
    user_list (DataFrame, optional): DataFrame containing user credentials.
    Defaults to querying the database.

    Returns:
    tuple: Contains the authenticated user's name,
        authentication status, username, and authenticator object.
    """
    if user_list is None:
        user_list = get_all_users()

    usernames = []
    names = []
    hashed_passwords = []

    for user in user_list:
        usernames.append(user.email)
        names.append(user.username)
        hashed_passwords.append(user.password)

    authenticator = stauth.Authenticate(
        names,
        usernames,
        hashed_passwords,
        ST_SECRET_KEY,
        ST_SECRET_KEY,
        cookie_expiry_days=30,
    )

    name, authentication_status, username = authenticator.login("Login", "main")
    return name, authentication_status, username, authenticator


def handle_authentication():
    """
    Manages the authentication flow, stopping the app if the user is not authenticated.

    Returns:
    str: The authenticated user's name.
    """
    name, authentication_status, _, authenticator = user_authentication()
    if not authentication_status:
        st.stop()

    st.sidebar.write(f"Welcome *{name}*!")
    authenticator.logout("Logout", "sidebar")

    return name

