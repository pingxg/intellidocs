"""
This module provides functions for user group management in a Streamlit application,
including creating, fetching, updating, and deleting user group records in the database.
"""

from typing import List, Optional
from database.models import UserGroup, Tag
from database.session import get_db
from uuid import UUID

class UserGroupService:
    @staticmethod
    def create_user_group(group_name: str, tag_ids: Optional[List[UUID]] = None) -> UserGroup:
        """
        Creates a new user group in the database and associates it with tags.

        Parameters:
        group_name (str): The name of the new user group.
        tag_ids (Optional[List[UUID]]): A list of tag UUIDs to associate with the user group.

        Returns:
        UserGroup: The created UserGroup object.
        """
        with get_db() as db:
            new_group = UserGroup(group_name=group_name)
            # update the usergroup_tags association table
            if tag_ids:
                # Fetch the tags by their UUIDs
                tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
                # Associate the tags with the new group
                new_group.tags = tags
            db.add(new_group)
            db.commit()
            db.refresh(new_group)
            return new_group

    @staticmethod
    def fetch_all_user_groups() -> List[UserGroup]:
        """
        Retrieves all user groups from the database.

        Returns:
        List[UserGroup]: A list of UserGroup objects.
        """
        with get_db() as db:
            return db.query(UserGroup).order_by(UserGroup.group_name).all()

    @staticmethod
    def get_user_group_by_id(group_id: UUID) -> Optional[UserGroup]:
        """
        Retrieves a user group by its ID.

        Parameters:
        group_id (UUID): The ID of the user group to retrieve.

        Returns:
        Optional[UserGroup]: The UserGroup object if found, otherwise None.
        """
        with get_db() as db:
            return db.query(UserGroup).filter(UserGroup.id == group_id).first()

    @staticmethod
    def get_tags_for_group(group_id: UUID) -> List[Tag]:
        """
        Retrieves the tags associated with a user group by its ID from the association table.

        Parameters:
        group_id (UUID): The ID of the user group to retrieve tags for.

        Returns:
        List[Tag]: A list of Tag objects associated with the user group.
        """
        with get_db() as db:
            return db.query(Tag).join(UserGroup.tags).filter(UserGroup.id == group_id).all()

    @staticmethod
    def update_user_group(group_id: UUID, group_name: Optional[str] = None, tag_ids: Optional[List[UUID]] = None) -> Optional[UserGroup]:
        """
        Updates an existing user group's information.

        Parameters:
        group_id (UUID): The ID of the user group to update.
        group_name (Optional[str]): The new name for the user group (if provided).
        tag_ids (Optional[List[UUID]]): A list of tag UUIDs to associate with the user group.

        Returns:
        Optional[UserGroup]: The updated UserGroup object if the group was found and updated, otherwise None.
        """
        with get_db() as db:
            group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
            if group:
                if group_name:
                    group.group_name = group_name
                if tag_ids is not None:
                    if tag_ids:
                        # Fetch the tags by their UUIDs
                        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
                        group.tags = tags
                    else:
                        # Remove all tag associations if tag_ids is an empty list
                        group.tags = []
                db.commit()
                db.refresh(group)
            return group

    @staticmethod
    def delete_user_group(group_id: UUID) -> bool:
        """
        Deletes a user group from the database if no users are associated with it.

        Parameters:
        group_id (UUID): The ID of the user group to delete.

        Returns:
        bool: True if the user group was deleted, otherwise False.
        """
        with get_db() as db:
            group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
            if group:
                if group.can_be_deleted():
                    db.delete(group)
                    db.commit()
                    return True
                else:
                    # Log or handle the case where the group cannot be deleted
                    print(f"Cannot delete UserGroup '{group.group_name}' because it has associated users.")
            return False

    @staticmethod
    def update_user_group_tags(group_id: UUID, tag_ids: List[UUID]) -> Optional[UserGroup]:
        """
        Updates the tags associated with a user group.

        Parameters:
        group_id (UUID): The ID of the user group to update.
        tag_ids (List[UUID]): A list of tag UUIDs to associate with the user group.

        Returns:
        Optional[UserGroup]: The updated UserGroup object if the group was found and updated, otherwise None.
        """
        with get_db() as db:
            group = db.query(UserGroup).filter(UserGroup.id == group_id).first()
            if group:
                # Fetch the tags by their UUIDs
                tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
                # Update the group's tags
                group.tags = tags
                db.commit()
                db.refresh(group)
            return group
