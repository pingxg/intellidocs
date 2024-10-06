import streamlit as st
from services.file_service import extract_text_from_pdf
from services.logger import get_logger
from services.sharepoint_service import upload_to_sharepoint
from services.aws_service import upload_to_s3
from typing import Dict, Optional

st.title("IntelliDocs")

uploaded_file: Optional[st.UploadedFile] = st.file_uploader("Choose a file")
if uploaded_file is not None:
    try:
        # Assuming process_document is similar to extract_text_from_pdf
        metadata: Dict[str, str] = extract_text_from_pdf(uploaded_file)
        st.write("Extracted Metadata:", metadata)
        
        try:
            # Assuming store_metadata is similar to a function that stores metadata in a database
            # You might need to implement this function based on your database setup
            store_metadata(metadata)
            st.toast("Metadata stored successfully!", icon="✅")
        except Exception as e:
            st.toast(f"Failed to store metadata: {e}", icon="🚨")
        
        try:
            upload_to_sharepoint(uploaded_file, uploaded_file.name)
            st.toast("File uploaded to SharePoint successfully!", icon="✅")
        except Exception as e:
            st.toast(f"Failed to upload to SharePoint: {e}", icon="🚨")
        
        try:
            upload_to_s3(uploaded_file, uploaded_file.name)
            st.toast("File uploaded to S3 successfully!", icon="✅")
        except Exception as e:
            st.toast(f"Failed to upload to S3: {e}", icon="🚨")
    
    except Exception as e:
        st.toast(f"Failed to process document: {e}", icon="🚨")
