import os
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, exc, text
import config.config as cfg
from utils.logger import get_logger

logger = get_logger(__name__)

def create_db_if_not_exists():
    # create database if not exists
    db_uri = cfg.DATABASE_URL
    database = db_uri.rsplit('/', 1)[-1]
    db_postgres = db_uri.rsplit('/', 1)[0] + "/postgres"
    try:
        engine = create_engine(db_uri)
        # Attempt to connect to the database
        with engine.connect() as conn:
            logger.info(f'Database {database} already exists.')
    except exc.OperationalError:
        logger.info(f'Database {database} does not exist. Creating now.')
        engine = create_engine(db_postgres)
        try:
            # Attempt to connect to the database
            with engine.connect() as conn:
                conn.execute(text("commit"))
                conn.execute(text(f'CREATE DATABASE {database};'))
                logger.info(f'Database {database} created successfully.')
        except exc.SQLAlchemyError as e:
            logger.error(f'Error creating database {database}: {e}')

def run_migrations():
    # Point to the alembic.ini file
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '..', 'alembic.ini'))
    command.revision(alembic_cfg, autogenerate=True, message="Auto-generated migration")
    command.upgrade(alembic_cfg, 'head')

if __name__ == '__main__':
    create_db_if_not_exists()
    run_migrations()
