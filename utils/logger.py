import logging
from logging.handlers import SMTPHandler
import config.config as cfg

# Email settings
SMTP_SERVER = cfg.SMTP_SERVER
SMTP_PORT = cfg.SMTP_PORT
SMTP_USERNAME = cfg.SMTP_USERNAME
SMTP_PASSWORD = cfg.SMTP_PASSWORD
EMAIL_FROM = cfg.EMAIL_FROM
EMAIL_TO = cfg.EMAIL_TO
EMAIL_SUBJECT = cfg.EMAIL_SUBJECT

# Log level
LOG_LEVEL = cfg.LOG_LEVEL.upper()

def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger configured with console output and email notification on critical errors.
    
    :param name: The name of the logger.
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(LOG_LEVEL)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Email handler for critical errors
        if LOG_LEVEL == 'ERROR' or LOG_LEVEL == 'CRITICAL':
            email_handler = SMTPHandler(
                mailhost=(SMTP_SERVER, SMTP_PORT),
                fromaddr=EMAIL_FROM,
                toaddrs=EMAIL_TO.split(','),
                subject=EMAIL_SUBJECT,
                credentials=(SMTP_USERNAME, SMTP_PASSWORD),
                secure=()
            )
            email_handler.setLevel(logging.CRITICAL)
            email_formatter = logging.Formatter(
                'Timestamp: %(asctime)s\nLogger: %(name)s\nLevel: %(levelname)s\n\nMessage:\n%(message)s'
            )
            email_handler.setFormatter(email_formatter)
            logger.addHandler(email_handler)

    return logger
