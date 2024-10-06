import PyPDF2
import streamlit as st
from typing import IO

def extract_text_from_pdf(file: IO) -> str:
    reader = PyPDF2.PdfFileReader(file)
    text = ""
    for page_num in range(reader.getNumPages()):
        text += reader.getPage(page_num).extract_text()
    return text
