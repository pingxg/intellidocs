from typing import Optional, List
from database.session import get_db
from database.models import Document, Tag

def create_document(file_name: str, document_type: str, content: str, metadata: Optional[dict] = None) -> Document:
    with get_db() as db:  # Get a session from session.py
        new_document = Document(file_name=file_name, document_type=document_type, content=content, metadata=metadata)
        db.add(new_document)
        db.commit()  # Commit the transaction to the database
        db.refresh(new_document)  # Refresh the instance with the new state from the database
        return new_document

def get_all_documents() -> List[Document]:
    with get_db() as db:
        return db.query(Document).all()
