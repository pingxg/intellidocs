from typing import List, Optional
from database.models import Document, DocumentContent, Tag
from database.session import get_db
from uuid import UUID

class DocumentService:
    @staticmethod
    def create_document(title: str, content: str, file_extension: str, tags: Optional[List[UUID]] = None, document_metadata: Optional[str] = None) -> Document:
        """
        Creates a new document in the database and associates it with tags.

        Parameters:
        title (str): The title of the new document.
        content (str): The content of the new document.
        tags (Optional[List[UUID]]): A list of tag UUIDs to associate with the document.

        Returns:
        Document: The created Document object.
        """
        with get_db() as db:
            new_document = Document(title=title, file_extension=file_extension)
            new_content = DocumentContent(content=content, document=new_document)
            if tags:
                # Fetch the tags by their UUIDs
                tag_objects = db.query(Tag).filter(Tag.id.in_(tags)).all()
                # Associate the tags with the new document
                new_document.tags = tag_objects
            db.add(new_document)
            db.add(new_content)
            db.commit()
            db.refresh(new_document)
            return new_document

    @staticmethod
    def fetch_all_documents() -> List[Document]:
        """
        Retrieves all documents from the database.

        Returns:
        List[Document]: A list of Document objects.
        """
        with get_db() as db:
            return db.query(Document).order_by(Document.title).all()

    @staticmethod
    def get_document_by_id(document_id: UUID) -> Optional[Document]:
        """
        Retrieves a document by its ID.

        Parameters:
        document_id (UUID): The ID of the document to retrieve.

        Returns:
        Optional[Document]: The Document object if found, otherwise None.
        """
        with get_db() as db:
            return db.query(Document).filter(Document.id == document_id).first()

    @staticmethod
    def update_document(document_id: UUID, title: Optional[str] = None, content: Optional[str] = None, tags: Optional[List[UUID]] = None) -> Optional[Document]:
        """
        Updates an existing document's information.

        Parameters:
        document_id (UUID): The ID of the document to update.
        title (Optional[str]): The new title for the document (if provided).
        content (Optional[str]): The new content for the document (if provided).
        tags (Optional[List[UUID]]): A list of tag UUIDs to associate with the document.

        Returns:
        Optional[Document]: The updated Document object if the document was found and updated, otherwise None.
        """
        with get_db() as db:
            document = db.query(Document).filter(Document.id == document_id).first()
            if document:
                if title:
                    document.title = title
                if content:
                    document_content = db.query(DocumentContent).filter(DocumentContent.document_id == document_id).first()
                    if document_content:
                        document_content.content = content
                    else:
                        new_content = DocumentContent(content=content, document=document)
                        db.add(new_content)
                if tags is not None:
                    if tags:
                        # Fetch the tags by their UUIDs
                        tag_objects = db.query(Tag).filter(Tag.id.in_(tags)).all()
                        document.tags = tag_objects
                    else:
                        # Remove all tag associations if tags is an empty list
                        document.tags = []
                db.commit()
                db.refresh(document)
            return document

    @staticmethod
    def delete_document(document_id: UUID) -> bool:
        """
        Deletes a document from the database.

        Parameters:
        document_id (UUID): The ID of the document to delete.

        Returns:
        bool: True if the document was deleted, otherwise False.
        """
        with get_db() as db:
            document = db.query(Document).filter(Document.id == document_id).first()
            if document:
                # Delete associated content
                db.query(DocumentContent).filter(DocumentContent.document_id == document_id).delete()
                db.delete(document)
                db.commit()
                return True
            return False

    @staticmethod
    def get_document_by_hash(content_hash: str) -> Optional[Document]:
        with get_db() as db:
            return db.query(Document).filter(Document.content_hash == content_hash).first()

    @staticmethod
    def document_exists_by_hash(content_hash: str) -> bool:
        with get_db() as db:
            document = db.query(Document).filter(Document.content_hash == content_hash).first()
            return document is not None
