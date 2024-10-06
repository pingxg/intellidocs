from office365.sharepoint.client_context import ClientContext
import config.config as cfg
import streamlit as st
from typing import Union, Optional, IO

# SharePoint configuration
SHAREPOINT_SITE_URL: str = cfg.SHAREPOINT_SITE_URL
SHAREPOINT_USERNAME: str = cfg.SHAREPOINT_USERNAME
SHAREPOINT_PASSWORD: str = cfg.SHAREPOINT_PASSWORD

def upload_to_sharepoint(file: Union[bytes, IO], file_name: str) -> Optional[str]:
    """
    Uploads a file to SharePoint.
    
    :param file: The file to upload (bytes or file-like object).
    :param file_name: The name of the file to be saved as in SharePoint.
    :return: The URL of the uploaded file.
    """
    ctx: ClientContext = ClientContext(SHAREPOINT_SITE_URL).with_credentials(SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD)

    try:
        target_folder = ctx.web.get_folder_by_server_relative_url("/sites/yoursite/Documents")
        target_folder.upload_file(file_name, file.read()).execute_query()
        file_url: str = f"{SHAREPOINT_SITE_URL}/sites/yoursite/Documents/{file_name}"
        return file_url
    except Exception as e:
        st.error(f"Failed to upload file to SharePoint: {e}")
        return None
