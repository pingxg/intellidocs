import streamlit as st
from services.user_service import UserService
from services.user_group_service import UserGroupService
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

st.title("User Management")

# Add tabs for user management tasks
tab1, tab2, tab3 = st.tabs(["Add User", "Update User", "Delete User"])

# Fetch user groups
user_groups = UserGroupService.fetch_all_user_groups()
user_group_options = {group.group_name: group.id for group in user_groups}

# Add a new user
with tab1:
    st.subheader("Add New User")
    with st.form(key='add_user_form', clear_on_submit=True, border=False):
        username = st.text_input("Username", key='add_user_username')
        email = st.text_input("Email", key='add_user_email')
        password = st.text_input("Password", type="password", key='add_user_password')
        user_group = st.selectbox("User Group", options=list(user_group_options.keys()), index=None, key='add_user_group')
        submit_button = st.form_submit_button(label='Add User')
        if submit_button:
            if not username or not email or not password:
                st.toast("All fields are required!", icon="🚨")
                logger.warning("Attempted to add user with missing fields.")
            else:
                try:
                    password_hash = password
                    UserService.create_user(username, email, password_hash, user_group_options.get(user_group))
                    st.toast("User added successfully!", icon="✅")
                    logger.info(f"User '{username}' added successfully.")
                    st.rerun()
                except Exception as e:
                    st.toast(f"Failed to add user '{username}'. Please check the details and try again. Error: {e}", icon="🚨")
                    logger.error(f"Error adding user '{username}': {e}")

with tab2:
    st.subheader("Update User")
    users = UserService.fetch_all_users()
    user_options = {user.username: user.id for user in users}
    
    # Fetch all users and create a selection box outside the form
    selected_username = st.selectbox("Select User", options=list(user_options.keys()), index=None, key='update_user_selector')
    selected_user_id = user_options.get(selected_username, None)

    # Check if a user is selected and fetch their data
    if selected_user_id is not None:
        selected_user = UserService.get_user_by_id(selected_user_id)
        default_username = selected_user.username
        default_email = selected_user.email
        # Update user group index based on the selected user
        st.session_state.default_user_group_index = list(user_group_options.values()).index(selected_user.user_group_id) if selected_user.user_group_id in user_group_options.values() else None
    else:
        default_username = ""
        default_email = ""
        st.session_state.default_user_group_index = None

    # Create the form with pre-filled values
    with st.form(key='update_user_form', clear_on_submit=True, border=False):
        username = st.text_input("New Username", value=default_username, key='update_user_username')
        email = st.text_input("New Email", value=default_email, key='update_user_email')
        password = st.text_input("New Password", type="password", key='update_user_password')
        user_group = st.selectbox("New User Group", options=list(user_group_options.keys()), index=st.session_state.default_user_group_index if st.session_state.default_user_group_index is not None else 0, key='update_user_group')
        
        submit_button = st.form_submit_button(label='Update User')
        
        if submit_button:
            if selected_user_id is None:
                st.toast("Please select a valid user!", icon="🚨")
                logger.warning("Attempted to update user without a valid selection.")
            elif not (username or email or password):
                st.toast("At least one field is required!", icon="🚨")
                logger.warning("Attempted to update user with no fields provided.")
            else:
                try:
                    UserService.update_user(selected_user_id, username, email, password, user_group_options[user_group])
                    st.toast("User updated successfully!", icon="✅")
                    logger.info(f"User '{selected_username}' updated successfully.")
                    st.rerun()
                except Exception as e:
                    st.toast(f"Failed to update user '{selected_username}'. Please ensure the details are correct and try again. Error: {e}", icon="🚨")
                    logger.error(f"Error updating user '{selected_username}': {e}")

with tab3:
    st.subheader("Delete User")
    users = UserService.fetch_all_users()
    user_options = {user.username: user.id for user in users}
    selected_username = st.selectbox("Select User", options=list(user_options.keys()), index=None, key='delete_user_selector')
    
    if selected_username:
        @st.dialog("Confirm Deletion")
        def confirm_deletion():
            st.write(f"Are you sure you want to delete the user '{selected_username}'?")
            if st.button("Confirm Delete"):
                try:
                    selected_user_id = user_options[selected_username]
                    UserService.delete_user(selected_user_id)
                    st.toast("User deleted successfully!", icon="✅")
                    logger.info(f"User '{selected_username}' deleted successfully.")
                    st.session_state.pop('delete_user_selector', None)
                    st.rerun()  # Refresh the page
                except Exception as e:
                    st.toast(f"Failed to delete user '{selected_username}'. Please ensure the details are correct and try again. Error: {e}", icon="🚨")
                    logger.error(f"Error deleting user '{selected_username}': {e}")
            if st.button("Cancel"):
                st.toast("User deletion cancelled.", icon="ℹ️")
                logger.info(f"User deletion for '{selected_username}' was cancelled.")
                st.session_state.pop('delete_user_selector', None)
                st.rerun()

    with st.form(key='delete_user_form', clear_on_submit=True, border=False):
        submit_button = st.form_submit_button(label='Delete User')
        if submit_button and selected_username:
            confirm_deletion()
