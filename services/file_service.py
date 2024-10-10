import PyPDF2
import streamlit as st
from typing import IO
import config.config as cfg
from typing import List
import pymupdf
import base64
import pandas as pd
import requests
from database.models import Document, Tag, User
from typing import Optional
from database.session import get_db

def encode_image(image_path):
    """
    Encodes an image to a base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    text = ""
    try:
        with pymupdf.open(pdf_path) as pdf_document:
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text("text")
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def create_document(file_name: str, document_type: str, content: str, metadata: Optional[dict] = None) -> Document:
    with get_db() as db:  # Get a session from session.py
        new_document = Document(file_name=file_name, document_type=document_type, content=content, metadata=metadata)
        db.add(new_document)
        db.commit()  # Commit the transaction to the database
        db.refresh(new_document)  # Refresh the instance with the new state from the database
        return new_document

def get_all_documents() -> List[Document]:
    with get_db() as db:
        return db.query(Document).all()

