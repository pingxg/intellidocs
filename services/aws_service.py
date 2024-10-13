# from typing import Union, Optional
# import boto3
# import config.config as cfg
# import streamlit as st

# # AWS credentials and S3 configuration
# AWS_ACCESS_KEY = cfg.AWS_ACCESS_KEY
# AWS_SECRET_KEY = cfg.AWS_SECRET_KEY
# S3_BUCKET_NAME = cfg.S3_BUCKET_NAME

# def upload_to_s3(file: Union[bytes, 'file-like object'], file_name: str) -> Optional[str]:
#     """
#     Uploads a file to an S3 bucket.
    
#     :param file: The file to upload (bytes or file-like object).
#     :param file_name: The name of the file to be saved as in S3.
#     :return: The URL of the uploaded file.
#     """
#     s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    
#     try:
#         s3_client.upload_fileobj(file, S3_BUCKET_NAME, file_name)
#         s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{file_name}"
#         return s3_url
#     except Exception as e:
#         st.error(f"Failed to upload file to S3: {e}")
#         return None
