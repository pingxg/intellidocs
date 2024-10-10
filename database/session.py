from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from database.base import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()