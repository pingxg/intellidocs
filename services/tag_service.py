from typing import List, Optional
from uuid import UUID
from database.models import Tag
from database.session import get_db

class TagService:
    @staticmethod
    def create_tag(tag_name: str) -> Tag:
        """
        Create a new tag in the database.

        Args:
            tag_name (str): The name of the tag to be created.

        Returns:
            Tag: The newly created Tag object.
        """
        with get_db() as db:
            new_tag = Tag(tag_name=tag_name)
            db.add(new_tag)
            db.commit()
            db.refresh(new_tag)
            return new_tag

    @staticmethod
    def get_all_tags() -> List[Tag]:
        """
        Retrieve all tags from the database.

        Returns:
            List[Tag]: A list of all Tag objects.
        """
        with get_db() as db:
            return db.query(Tag).order_by(Tag.tag_name).all()

    @staticmethod
    def get_tag_by_id(tag_id: UUID) -> Optional[Tag]:
        """
        Retrieve a tag by its ID.

        Args:
            tag_id (UUID): The ID of the tag to retrieve.

        Returns:
            Optional[Tag]: The Tag object if found, otherwise None.
        """
        with get_db() as db:
            return db.query(Tag).filter(Tag.id == tag_id).first()

    @staticmethod
    def delete_tag(tag_id: UUID) -> bool:
        """
        Delete a tag from the database if it is not associated with any documents.

        Args:
            tag_id (UUID): The ID of the tag to delete.

        Returns:
            bool: True if the tag was deleted, False otherwise.
        """
        with get_db() as db:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag and not tag.documents:
                db.delete(tag)
                db.commit()
                return True
            return False

    @staticmethod
    def can_be_deleted(tag: Tag) -> bool:
        """
        Check if a tag can be deleted (i.e., no documents are associated with it).

        Args:
            tag (Tag): The Tag object to check.

        Returns:
            bool: True if the tag can be deleted, False otherwise.
        """
        return len(tag.documents) == 0

    @staticmethod
    def update_tag(tag_id: UUID, new_name: str) -> Optional[Tag]:
        """
        Update the name and user group of an existing tag.

        Args:
            tag_id (UUID): The ID of the tag to update.
            new_name (str): The new name for the tag.

        Returns:
            Optional[Tag]: The updated Tag object if successful, otherwise None.
        """
        with get_db() as db:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                tag.tag_name = new_name
                db.commit()
                db.refresh(tag)
                return tag
            return None
