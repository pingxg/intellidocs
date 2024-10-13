"""
This module provides functionality for sending emails using Office365 SMTP
within a Streamlit application. It includes functions to fetch secrets from
environment variables, create email content, and send emails. Logging is used 
to track the success or failure of email transmissions.

Functions:
- fetch_secret: Retrieves secret values from environment variables.
- create_email_body: Constructs the body of the email based on the subject and data.
- send_email: Sends an email to a specified receiver with a given subject and data.
"""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Setting up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_secret(key):
    """
    Fetch a secret value from the environment variables.

    Parameters:
    - key (str): The key for the secret value.

    Returns:
    - str: The secret value associated with the key, or None if the key does not exist.
    """
    return os.getenv(key)


def create_email_body(subject, data):
    """
    Create the body of an email based on the subject and data provided.

    Parameters:
    - subject (str): The subject of the email.
    - data (str or pandas.DataFrame): The content of the email.
        If data is a string or if the subject starts with "Error" or "SMP",
        the data is returned as a string. Otherwise, it is formatted as an HTML table.

    Returns:
    - str: The formatted HTML content for the email body.
    """
    if subject.startswith(("Error", "SMP")) or isinstance(data, str):
        return str(data)

    return f"""
        <html>
        <head>
            Please find {subject}.
        </head>
        <body>
            {data.to_html()}
        </body>
        </html>
    """


def send_email(receiver, subject, data) -> None:
    """
    Send an email to the specified receiver with the given subject and data.

    Parameters:
    - receiver (str): The email address of the receiver.
    - subject (str): The subject of the email.
    - data (str or pandas.DataFrame): The content of the email.
        This will be formatted into the email body.

    Logs:
    - Logs an info message if the email is sent successfully.
    - Logs an error message if sending the email fails.
    """
    # Create email message
    mimemsg = MIMEMultipart()
    mimemsg["From"] = fetch_secret("OFFICE_USN")
    mimemsg["To"] = receiver
    mimemsg["Subject"] = subject

    # Attach the body
    body = create_email_body(subject, data)
    mimemsg.attach(MIMEText(body, "html"))

    # Establish connection and send the email
    try:
        connection = smtplib.SMTP(host="smtp.office365.com", port=587)
        connection.starttls()
        connection.login(fetch_secret("OFFICE_USN"), fetch_secret("OFFICE_PSW"))
        connection.send_message(mimemsg)
        connection.quit()
        logging.info(
            "Email sent successfully to %s with subject: %s", receiver, subject
        )
    except smtplib.SMTPAuthenticationError as e:
        logging.error(
            "SMTP authentication failed for user %s. Error: %s",
            fetch_secret("OFFICE_USN"),
            e,
        )
    except smtplib.SMTPRecipientsRefused as e:
        logging.error(
            "The server refused the email recipients %s. Error: %s", receiver, e
        )
    except smtplib.SMTPException as e:
        logging.error("Failed to send email due to an SMTP error. Error: %s", e)
    except Exception as e:
        logging.error("An unexpected error occurred. Error: %s", e)