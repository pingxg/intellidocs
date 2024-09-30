import streamlit as st
from src.document_processor import process_document
from src.database import store_metadata
from src.sharepoint_manager import upload_to_sharepoint

st.title("Smart Document Management System")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    metadata = process_document(uploaded_file)
    st.write("Extracted Metadata:", metadata)
    store_metadata(metadata)
    upload_to_sharepoint(uploaded_file, metadata)
