from PyPDF2 import PdfReader
from typing import IO
import base64
import hashlib
from utils.logger import get_logger

logger = get_logger(__name__)

def encode_image(image_path):
    """
    Encodes an image to a base64 string.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        logger.error(f"Error encoding image: {e}")
        return None

def extract_text_from_pdf(file: IO) -> str:
    """
    Extracts text from a PDF file using PyMuPDF.
    """
    text_data = ""
    try:
        if file is not None:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text_data += page.extract_text()
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
    return text_data

def generate_hash_from_bytes(fileobj: IO) -> str:
    """
    Generates a SHA-256 hash from the given file-like object.

    :param fileobj: A file-like object opened for reading in binary mode.
    :return: A SHA-256 hash string.
    """
    digest = hashlib.file_digest(fileobj, "sha256")
    return digest.hexdigest()
