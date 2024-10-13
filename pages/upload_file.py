import streamlit as st
from utils.file_utils import extract_text_from_pdf
from utils.logger import get_logger
from services.document_service import DocumentService
from services.openai_service import OpenAIClient
from services.tag_service import TagService
from datetime import datetime
from utils.file_utils import generate_hash_from_bytes
import json

logger = get_logger(__name__)

st.title("IntelliDocs - Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'], accept_multiple_files=False)
if uploaded_file is not None:
    try:
        logger.info("File uploaded: %s", uploaded_file.name)
        
        # Check if the document already exists
        content_hash = generate_hash_from_bytes(uploaded_file)

        existing_document = DocumentService.document_exists_by_hash(content_hash)
        if existing_document is True:
            st.toast(f"This document already exists in the database.", icon="🔍")
            logger.info(f"Document {uploaded_file.name} already exists in the database.")
            st.stop()

        extracted_text = extract_text_from_pdf(uploaded_file)
        logger.info("Text extracted successfully.")
        parsed_data = OpenAIClient().extract_document_metadata(input_data=extracted_text)
        parsed_data = json.loads(parsed_data)

        col1, col2 = st.columns(2)

        with col1:
            st.expander("Extracted Text", expanded=False).code(extracted_text, language="text")

        with col2:
            st.expander("Parsed Data", expanded=False).code(json.dumps(parsed_data, indent=2), language="json")

        file_name = parsed_data.get("filename", "")
        parsed_data.pop("filename", None)
        start_date = datetime.strptime(parsed_data.get("start_date", ""), "%Y.%m.%d") if parsed_data.get("start_date", "") else None
        parsed_data.pop("start_date", None)
        end_date = datetime.strptime(parsed_data.get("end_date", ""), "%Y.%m.%d") if parsed_data.get("end_date", "") else None
        parsed_data.pop("end_date", None)
        description = parsed_data.get("description", "")
        parsed_data.pop("description", None)


        col1, col2 = st.columns(2)

        with col1:
            file_name = st.text_input("File Name", value=file_name)
            start_date = st.date_input("Start Date", value=start_date)
            description = st.text_area("Description", value=description, height=250)
        with col2:
            file_extension = st.text_input("File Extension", value=uploaded_file.type.split('/')[1])
            end_date = st.date_input("End Date", value=end_date)
            document_metadata = st.text_area("Document Metadata", value=json.dumps(parsed_data, indent=2), height=250)


        # Fetch tags for multiselect
        all_tags = TagService.get_all_tags()
        tag_options = {tag.tag_name: tag.id for tag in all_tags}
        selected_tags = st.multiselect("Tags", options=list(tag_options.keys()), default=parsed_data.get("tags", []))
        
        if st.button("Save Document"):
            try:
                # Save the document using the DocumentService
                DocumentService.create_document(
                    file_name=file_name,
                    start_date=start_date,
                    end_date=end_date,
                    description=description,
                    file_extension=file_extension,
                    document_metadata=document_metadata,
                    tag_ids=[tag_options[tag] for tag in selected_tags]
                )
                st.toast("Document saved successfully!", icon="✅")
                logger.info("Document saved successfully.")
            except Exception as e:
                st.toast(f"Failed to save document: {e}", icon="🚨")
                logger.error("Failed to save document: %s", e)
    
    except Exception as e:
        st.toast(f"Failed to process document: {e}", icon="🚨")
        logger.error("Failed to process document: %s", e)
