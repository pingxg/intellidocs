from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import config.config as cfg

# SQLAlchemy Base class for model inheritance
Base = declarative_base()

# Create a database engine using the DATABASE_URL from config.py
engine = create_engine(cfg.DATABASE_URL, echo=True)
