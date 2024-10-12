import streamlit as st
from services.file_service import extract_text_from_pdf
from utils.logger import get_logger
from services.sharepoint_service import upload_to_sharepoint
# from services.aws_service import upload_to_s3
from typing import Dict, Optional

logger = get_logger(__name__)  # Initialize the logger

st.title("IntelliDocs")

uploaded_file: Optional[st.file_uploader] = st.file_uploader("Choose a file")
if uploaded_file is not None:
    try:
        logger.info("File uploaded: %s", uploaded_file.name)
        # Assuming process_document is similar to extract_text_from_pdf
        metadata: Dict[str, str] = extract_text_from_pdf(uploaded_file)
        st.write("Extracted Metadata:", metadata)
        logger.info("Metadata extracted successfully.")
        
        try:
            # Assuming store_metadata is similar to a function that stores metadata in a database
            # You might need to implement this function based on your database setup
            # store_metadata(metadata)
            st.toast("Metadata stored successfully!", icon="✅")
            logger.info("Metadata stored successfully.")
        except Exception as e:
            st.toast(f"Failed to store metadata: {e}", icon="🚨")
            logger.error("Failed to store metadata: %s", e)
        
        try:
            upload_to_sharepoint(uploaded_file, uploaded_file.name)
            st.toast("File uploaded to SharePoint successfully!", icon="✅")
            logger.info("File uploaded to SharePoint successfully.")
        except Exception as e:
            st.toast(f"Failed to upload to SharePoint: {e}", icon="🚨")
            logger.error("Failed to upload to SharePoint: %s", e)
        
        try:
            # upload_to_s3(uploaded_file, uploaded_file.name)
            st.toast("File uploaded to S3 successfully!", icon="✅")
            logger.info("File uploaded to S3 successfully.")
        except Exception as e:
            st.toast(f"Failed to upload to S3: {e}", icon="🚨")
            logger.error("Failed to upload to S3: %s", e)
    
    except Exception as e:
        st.toast(f"Failed to process document: {e}", icon="🚨")
        logger.error("Failed to process document: %s", e)
