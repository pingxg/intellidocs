import uuid
from sqlalchemy import Column, String, ForeignKey, Table, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.base import Base
from pgvector.sqlalchemy import Vector
from typing import Optional, List

# Many-to-Many association table between documents and tags
document_tags = Table(
    'document_tags', Base.metadata,
    Column('document_id', UUID(as_uuid=True), ForeignKey('documents.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)
)

# Many-to-Many association table between user groups and tags
usergroup_tags = Table(
    'usergroup_tags', Base.metadata,
    Column('usergroup_id', UUID(as_uuid=True), ForeignKey('user_groups.id'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id'), primary_key=True)
)

class User(Base):
    """
    Model representing a user.
    
    Attributes:
        - id: Primary key of the user (UUID).
        - username: Unique username for the user.
        - email: Email address for the user.
        - password: Password for the user (hashed).
        - user_group_id: Foreign key referencing the user's group.
    """
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('user_groups.id'))

    user_group: Mapped['UserGroup'] = relationship('UserGroup', back_populates='users')

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"

class UserGroup(Base):
    """
    Model representing a user group.
    
    Attributes:
        - id: Primary key of the user group.
        - group_name: Name of the user group.
        - tags: Many-to-many relationship with tags.
    """
    __tablename__ = 'user_groups'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    group_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Relationship to users
    users: Mapped[List[User]] = relationship('User', back_populates='user_group')

    # Relationship to tags (many-to-many)
    tags: Mapped[List['Tag']] = relationship('Tag', secondary=usergroup_tags, back_populates='user_groups')

    def __repr__(self) -> str:
        return f"<UserGroup(id={self.id}, group_name={self.group_name})>"

class Document(Base):
    """
    Model representing a document.
    
    Attributes:
        - id: Primary key of the document (UUID).
        - file_name: Name of the file uploaded.
        - description: Description of the document.
        - description_vector: Vector representation of the document description.
        - file_path: Path of the file uploaded.
        - document_metadata: Additional document_metadata in JSONB format (e.g., date, author).
        - tags: Many-to-many relationship with tags.
    """
    __tablename__ = 'documents'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    description_vector: Mapped[Vector] = mapped_column(Vector(1536))
    document_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    created_at: Mapped[Optional[str]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[str]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to tags (many-to-many)
    tags: Mapped[List['Tag']] = relationship('Tag', secondary=document_tags, back_populates='documents')

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, file_name={self.file_name}, document_type={self.document_type})>"

class DocumentContent(Base):
    """
    Model representing the raw content and vector store of a document.
    
    Attributes:
        - id: Primary key (UUID).
        - document_id: Foreign key referencing the document's UUID.
        - raw_content: The raw document content as a string.
        - vector: The corresponding vector representation of the document.
    """
    __tablename__ = 'document_contents'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('documents.id'), nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    vector: Mapped[Vector] = mapped_column(Vector(1536))
    
    # Timestamps
    created_at: Mapped[Optional[str]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[str]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<DocumentContent(id={self.id}, document_id={self.document_id})>"

class Tag(Base):
    """
    Model representing a tag for categorizing documents.
    
    Attributes:
        - id: Primary key of the tag.
        - tag_name: Name of the tag (e.g., 'contract', 'rental-related').
        - documents: Many-to-many relationship with documents.
    """
    __tablename__ = 'tags'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    # Timestamps
    created_at: Mapped[Optional[str]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[str]] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationship to documents (many-to-many)
    documents: Mapped[List[Document]] = relationship('Document', secondary=document_tags, back_populates='tags')

    # Relationship to user groups (many-to-many)
    user_groups: Mapped[List[UserGroup]] = relationship('UserGroup', secondary=usergroup_tags, back_populates='tags')

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, tag_name={self.tag_name})>"
