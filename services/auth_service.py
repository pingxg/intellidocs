"""
This module handles user authentication for a Streamlit dashboard using 
streamlit_authenticator. It includes functions to authenticate users, 
manage the authentication flow, and interact with a custom database query.
"""

import streamlit as st
import streamlit_authenticator as stauth
from config.config import ST_SECRET_KEY
from services.user_service import UserService


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
        user_list = UserService.fetch_all_users()

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

