import PyPDF2
import streamlit as st
from typing import IO
import config.config as cfg
from typing import List
import fitz
import base64
import pandas as pd
import requests

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
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text("text")
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text