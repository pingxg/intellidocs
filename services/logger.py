# services/logger.py
import logging
import os

# Log Level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()

def get_logger(name):
    """
    Returns a logger with a given name, configured for the app.
    
    :param name: Logger name, typically the module's __name__
    :return: Configured logger
    """
    logger = logging.getLogger(name)
    
    if not logger.hasHandlers():
        logger.setLevel(LOG_LEVEL)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LOG_LEVEL)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        
        # Optional: File handler (for file-based logging)
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(LOG_LEVEL)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Adding both handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger
