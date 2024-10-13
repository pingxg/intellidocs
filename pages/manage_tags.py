import streamlit as st
from services.tag_service import TagService
from utils.logger import get_logger

logger = get_logger(__name__)

st.title("Tag Management")

tab1, tab2, tab3 = st.tabs(["Add Tag", "Update Tag", "Delete Tag"])

with tab1:
    st.subheader("Add New Tag")
    with st.form(key='add_tag_form', clear_on_submit=True, border=False):
        tag_name = st.text_input("Tag Name", key='add_tag_name').lower().replace(" ", "-")
        notify = st.checkbox("Notify", key='add_notify', value=False)
        notification_days_before_expiry = st.number_input("Days Before Expiry", min_value=0, value=30, key='add_notification_days')
        notification_frequency = st.number_input("Notification Frequency", min_value=0, value=7, key='add_notification_frequency')
        submit_button = st.form_submit_button(label='Add Tag')
        if submit_button:
            if not tag_name:
                st.toast("Tag name is required!", icon="🚨")
                logger.warning("Attempted to add tag with missing name.")
            else:
                try:
                    TagService.create_tag(tag_name, notify, notification_days_before_expiry, notification_frequency)
                    st.toast("Tag added successfully!", icon="✅")
                    logger.info(f"Tag '{tag_name}' added successfully.")
                    st.rerun()
                except Exception as e:
                    st.toast(f"Failed to add tag '{tag_name}'. Please check the details and try again. Error: {e}", icon="🚨")
                    logger.error(f"Error adding tag '{tag_name}': {e}")

with tab2:
    st.subheader("Update Tag")
    tags = TagService.get_all_tags()
    tag_options = {tag.tag_name.lower().replace(" ", "-"): tag.id for tag in tags}
    
    selected_tag_name = st.selectbox("Select Tag", options=list(tag_options.keys()), index=None, key='update_tag_selector')
    
    # Fetch the selected tag details
    if selected_tag_name:
        selected_tag_id = tag_options[selected_tag_name]
        selected_tag = TagService.get_tag_by_id(selected_tag_id)

    with st.form(key='update_tag_form', clear_on_submit=True, border=False):
        tag_name = st.text_input("New Tag Name", value=selected_tag.tag_name if selected_tag_name else "", key='update_tag_name').lower().replace(" ", "-")
        notify = st.checkbox("Notify", value=selected_tag.notify if selected_tag_name else False, key='update_notify')
        notification_days_before_expiry = st.number_input("Days Before Expiry", min_value=0, value=selected_tag.notification_days_before_expiry if selected_tag_name else 0, key='update_notification_days')
        notification_frequency = st.number_input("Notification Frequency", min_value=0, value=selected_tag.notification_frequency if selected_tag_name else 0, key='update_notification_frequency')
        submit_button = st.form_submit_button(label='Update Tag')
        if submit_button:
            if not tag_name:
                st.toast("Tag name is required!", icon="🚨")
                logger.warning("Attempted to update tag with no name provided.")
            else:
                try:
                    TagService.update_tag(selected_tag_id, tag_name, notify, notification_days_before_expiry, notification_frequency)
                    st.toast("Tag updated successfully!", icon="✅")
                    logger.info(f"Tag '{selected_tag_name}' updated successfully.")
                    st.rerun()
                except Exception as e:
                    st.toast(f"Failed to update tag '{selected_tag_name}'. Please ensure the details are correct and try again. Error: {e}", icon="🚨")
                    logger.error(f"Error updating tag '{selected_tag_name}': {e}")

with tab3:
    st.subheader("Delete Tag")
    tags = TagService.get_all_tags()
    tag_options = {tag.tag_name.lower().replace(" ", "-"): tag.id for tag in tags}
    
    selected_tag_name = st.selectbox("Select Tag", options=list(tag_options.keys()), index=None, key='delete_tag_selector')
    
    if selected_tag_name:
        @st.dialog("Confirm Deletion")
        def confirm_deletion():
            st.write(f"Are you sure you want to delete the tag '{selected_tag_name}'?")
            if st.button("Confirm Delete"):
                try:
                    selected_tag_id = tag_options[selected_tag_name]
                    if TagService.delete_tag(selected_tag_id):
                        st.toast("Tag deleted successfully!", icon="✅")
                        logger.info(f"Tag '{selected_tag_name}' deleted successfully.")
                        st.session_state.pop('delete_tag_selector', None)
                        st.rerun()
                    else:
                        st.toast(f"Cannot delete tag '{selected_tag_name}' because it is associated with documents.", icon="🚨")
                        logger.warning(f"Attempted to delete tag '{selected_tag_name}' that cannot be deleted.")
                except Exception as e:
                    st.toast(f"Failed to delete tag '{selected_tag_name}'. Please ensure the details are correct and try again. Error: {e}", icon="🚨")
                    logger.error(f"Error deleting tag '{selected_tag_name}': {e}")
            if st.button("Cancel"):
                st.toast("Tag deletion cancelled.", icon="ℹ️")
                logger.info(f"Tag deletion for '{selected_tag_name}' was cancelled.")
                st.session_state.pop('delete_tag_selector', None)
                st.rerun()

    with st.form(key='delete_tag_form', clear_on_submit=True, border=False):
        submit_button = st.form_submit_button(label='Delete Tag')
        if submit_button and selected_tag_name:
            confirm_deletion()
