import time
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from database.models import engine
from utils.logger import get_logger

logger = get_logger(__name__)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db(**session_options):
    db = SessionLocal(**session_options)
    logger.info("Database session created.")
    try:
        yield db
        logger.info("Database session yielded successfully.")
    finally:
        db.close()
        logger.info("Database session closed.")

def get_db_with_retries(retries=10, delay=0.2, **session_options):
    attempt = 0
    while attempt < retries:
        try:
            with get_db(**session_options) as db:
                yield db
            return
        except OperationalError as e:
            logger.warning(f"OperationalError encountered: {e}. Retrying {attempt + 1}/{retries}...")
            if attempt < retries - 1:
                time.sleep(delay)
                attempt += 1
            else:
                logger.error("Max retries reached. Raising exception.")
                raise e