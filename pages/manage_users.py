import streamlit as st
from database.session import get_db
from services.auth_service import get_all_users, create_user, update_user, delete_user
import uuid
# from werkzeug.security import generate_password_hash


st.title("User Management")

# Add tabs for user management tasks
tab1, tab2, tab3 = st.tabs(["Add User", "Update User", "Delete User"])

# Add a new user
with tab1:
    st.subheader("Add New User")
    with st.form(key='add_user_form'):
        username = st.text_input("Username", key='add_user_username')
        email = st.text_input("Email", key='add_user_email')
        password = st.text_input("Password", type="password", key='add_user_password')
        submit_button = st.form_submit_button(label='Add User')
        if submit_button:
            if not username or not email or not password:
                st.toast("All fields are required!", icon="🚨")
            else:
                try:
                    password_hash = password
                    create_user(username, email, password_hash)
                    st.toast("User added successfully!", icon="✅")
                except Exception as e:
                    st.toast(f"Failed to add user '{username}'. Please check the details and try again. Error: {e}", icon="🚨")

# Update user
with tab2:
    st.subheader("Update User")
    users = get_all_users()
    user_options = {user.username: user.id for user in users}
    selected_username = st.selectbox("Select User", options=list(user_options.keys()), key='update_user_selector')
    selected_user_id = user_options[selected_username]
    
    with st.form(key='update_user_form'):
        username = st.text_input("Username", key='update_user_username')
        email = st.text_input("Email", key='update_user_email')
        password = st.text_input("Password", type="password", key='update_user_password')
        submit_button = st.form_submit_button(label='Update User')
        if submit_button:
            if not username or not email or not password:
                st.toast("All fields are required!", icon="🚨")
            else:
                try:
                    update_user(selected_user_id, username, email, password)
                    st.toast("User updated successfully!", icon="✅")
                except Exception as e:
                    st.toast(f"Failed to update user '{selected_username}'. Please ensure the details are correct and try again. Error: {e}", icon="🚨")

# Delete user
with tab3:
    st.subheader("Delete User")
    users = get_all_users()
    user_options = {user.username: user.id for user in users}
    selected_username = st.selectbox("Select User", options=list(user_options.keys()), key='delete_user_selector')
    selected_user_id = user_options[selected_username]
    
    with st.form(key='delete_user_form'):
        submit_button = st.form_submit_button(label='Delete User')
        if submit_button:
            if not selected_username:
                st.toast("Please select a user to delete!", icon="🚨")
            else:
                try:
                    delete_user(selected_user_id)
                    st.toast("User deleted successfully!", icon="✅")
                except Exception as e:
                    st.toast(f"Failed to delete user '{selected_username}'. Please ensure the details are correct and try again. Error: {e}", icon="🚨")
