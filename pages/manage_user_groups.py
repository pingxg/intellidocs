import streamlit as st
from services.user_group_service import UserGroupService
from services.tag_service import TagService
from utils.logger import get_logger

logger = get_logger(__name__)

st.title("User Group Management")

tab1, tab2, tab3 = st.tabs(["Add User Group", "Update User Group", "Delete User Group"])

with tab1:
    st.subheader("Add New User Group")
    
    all_tags = TagService.get_all_tags()

    with st.form(key='add_user_group_form', clear_on_submit=True, border=False):
        group_name = st.text_input("Group Name", key='add_user_group_name').lower().replace(" ", "-")
        # Use all possible tags as options
        tags = st.multiselect("Tags", options=[tag.tag_name for tag in all_tags], key='add_user_group_tags')  
        submit_button = st.form_submit_button(label='Add User Group')
        if submit_button:
            if not group_name:
                st.toast("Group name is required!", icon="🚨")
                logger.warning("Attempted to add user group with missing name.")
            else:
                try:
                    # pass the tag ids
                    tag_ids = [tag.id for tag in all_tags if tag.tag_name in tags]
                    UserGroupService.create_user_group(group_name, tag_ids)
                    st.toast("User group added successfully!", icon="✅")
                    logger.info(f"User group '{group_name}' added successfully.")
                except Exception as e:
                    st.toast(f"Failed to add user group '{group_name}'. Please check the details and try again. Error: {e}", icon="🚨")
                    logger.error(f"Error adding user group '{group_name}': {e}")

with tab2:
    st.subheader("Update User Group")
    user_groups = UserGroupService.fetch_all_user_groups()
    group_options = {group.group_name.lower().replace(" ", "-"): group.id for group in user_groups}

    selected_group_name = st.selectbox(
        "Select User Group", 
        options=list(group_options.keys()), 
        index=0,
        key='update_user_group_selector'
    )
    selected_group_id = group_options[selected_group_name]
    current_tags = UserGroupService.get_tags_for_group(selected_group_id)
    current_tag_names = [tag.tag_name for tag in current_tags]

    all_tags = TagService.get_all_tags()

    with st.form(key='update_user_group_form', clear_on_submit=True, border=False):
        group_name = st.text_input("New Group Name", key='update_user_group_name').lower().replace(" ", "-")
        # Pre-populate the multiselect with current tags
        tags = st.multiselect(
            "New Tags", 
            options=[tag.tag_name for tag in all_tags], 
            default=current_tag_names,  # Set current tags as default
            key='update_user_group_tags'
        )
        submit_button = st.form_submit_button(label='Update User Group')
        if submit_button:
            try:
                # Use the existing group name if the new one is empty
                final_group_name = group_name if group_name else selected_group_name
                # If no tags are provided, set tag_ids to an empty list to remove all tags
                tag_ids = [tag.id for tag in all_tags if tag.tag_name in tags]
                UserGroupService.update_user_group(selected_group_id, final_group_name, tag_ids)

                st.toast("User group updated successfully!", icon="✅")
                logger.info(f"User group '{final_group_name}' updated successfully.")
                st.rerun()
            except Exception as e:
                st.toast(f"Failed to update user group '{selected_group_name}'. Please ensure the details are correct and try again. Error: {e}", icon="🚨")
                logger.error(f"Error updating user group '{selected_group_name}': {e}")

with tab3:
    st.subheader("Delete User Group")
    user_groups = UserGroupService.fetch_all_user_groups()
    group_options = {group.group_name.lower().replace(" ", "-"): group.id for group in user_groups}
    
    selected_group_name = st.selectbox("Select User Group", options=list(group_options.keys()), index=None, key='delete_user_group_selector')
    
    if selected_group_name:
        @st.dialog("Confirm Deletion")
        def confirm_deletion():
            st.write(f"Are you sure you want to delete the user group '{selected_group_name}'?")
            if st.button("Confirm Delete"):
                try:
                    selected_group_id = group_options[selected_group_name]
                    if UserGroupService.delete_user_group(selected_group_id):
                        st.toast("User group deleted successfully!", icon="✅")
                        logger.info(f"User group '{selected_group_name}' deleted successfully.")
                        st.session_state.pop('delete_user_group_selector', None)
                        st.rerun()
                    else:
                        st.toast(f"Cannot delete user group '{selected_group_name}' because it has associated users.", icon="🚨")
                        logger.warning(f"Attempted to delete user group '{selected_group_name}' that cannot be deleted.")
                except Exception as e:
                    st.toast(f"Failed to delete user group '{selected_group_name}'. Please ensure the details are correct and try again. Error: {e}", icon="🚨")
                    logger.error(f"Error deleting user group '{selected_group_name}': {e}")
            if st.button("Cancel"):
                st.toast("User group deletion cancelled.", icon="ℹ️")
                logger.info(f"User group deletion for '{selected_group_name}' was cancelled.")
                st.session_state.pop('delete_user_group_selector', None)
                st.rerun()

    with st.form(key='delete_user_group_form', clear_on_submit=True, border=False):
        submit_button = st.form_submit_button(label='Delete User Group')
        if submit_button and selected_group_name:
            confirm_deletion()
