import streamlit as st
import config.config as cfg
from services.auth_service import handle_authentication

cfg.config_page()

handle_authentication()

pages = {
    "Document Management": [
        st.Page("pages/upload_file.py", title="Upload File", icon="📤"),
        st.Page("pages/search_file.py", title="Search File", icon="🔍"),
        st.Page("pages/edit_file.py", title="Edit File", icon="✏️"),
        st.Page("pages/delete_file.py", title="Delete File", icon="🗑️"),
    ],

    "User & Tag Management": [
        st.Page("pages/manage_users.py", title="User Management", icon="👤"),
        st.Page("pages/manage_user_groups.py", title="User Group Management", icon="👥"),
        st.Page("pages/manage_tags.py", title="Tag Management", icon="🏷️"),
    ],

    "Chat & Support": [
        st.Page("pages/chatbot.py", title="Chat with File", icon="💬"),
    ],
}

pg = st.navigation(pages)
pg.run()