import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/mydatabase')

# AWS Configuration (for S3)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', 'your-aws-access-key')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', 'your-aws-secret-key')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'your-s3-bucket-name')

# Email Configuration (for notifications)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'your_email@gmail.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your_email_password')
EMAIL_FROM = os.getenv('EMAIL_FROM', SMTP_USERNAME)
EMAIL_TO = os.getenv('EMAIL_TO', 'admin@example.com')
EMAIL_SUBJECT = os.getenv('EMAIL_SUBJECT', 'Critical Error in Streamlit App')

# OpenAI API Configuration (for embeddings or generation tasks)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()

# Debug Mode
DEBUG_MODE = os.getenv('DEBUG_MODE', True)

# Streamlit Specific Configuration (optional)
ST_SECRET_KEY = os.getenv('ST_SECRET_KEY', 'your-streamlit-secret-key')

# SharePoint Configuration
SHAREPOINT_SITE_URL = os.getenv('SHAREPOINT_SITE_URL', 'your-sharepoint-site-url')
SHAREPOINT_USERNAME = os.getenv('SHAREPOINT_USERNAME', 'your-sharepoint-username')
SHAREPOINT_PASSWORD = os.getenv('SHAREPOINT_PASSWORD', 'your-sharepoint-password')

def config_page():
    """
    Configures the Streamlit application's page settings.

    This function sets up the initial configuration for the Streamlit page, including
    the page icon, layout, and sidebar state. It also loads and applies custom CSS
    styles from an external file to ensure consistent styling across the application.
    """
    st.set_page_config(
        page_icon="assets/logo.png",
        layout="wide",
        initial_sidebar_state="auto",
    )
    st.logo("assets/logo-sidebar.png")