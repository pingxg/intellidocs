import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Table, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from pgvector.sqlalchemy import Vector
import config.config as cfg

# SQLAlchemy Base class for model inheritance
Base = declarative_base()

# Create a database engine using the DATABASE_URL from config.py
engine = create_engine(cfg.DATABASE_URL, echo=True, pool_pre_ping=True, pool_recycle=3600, future=True, connect_args={"connect_timeout": 10})

# Many-to-Many association table between documents and tags
document_tags = Table(
    'document_tags', Base.metadata,
    Column('document_id', UUID(as_uuid=True), ForeignKey('documents.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

# Many-to-Many association table between user groups and tags
user_group_tags = Table(
    'user_group_tags', Base.metadata,
    Column('user_group_id', UUID(as_uuid=True), ForeignKey('user_groups.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
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
    user_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('user_groups.id'), nullable=False)

    user_group: Mapped['UserGroup'] = relationship('UserGroup', back_populates='users')

    # Timestamps in UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class UserGroup(Base):
    """
    Model representing a user group.
    
    Attributes:
        - id: Primary key of the user group.
        - group_name: Name of the user group.
        - tags: One-to-many relationship with tags.
    """
    __tablename__ = 'user_groups'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    group_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Relationship to users (one-to-many)
    users: Mapped[List[User]] = relationship('User', back_populates='user_group')

    # Relationship to tags (many-to-many)
    tags: Mapped[List['Tag']] = relationship('Tag', secondary=user_group_tags, back_populates='user_groups')

    # Timestamps in UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def can_be_deleted(self) -> bool:
        """Check if the user group can be deleted (i.e., no users are associated with it)."""
        return len(self.users) == 0

    def __repr__(self) -> str:
        return f"<UserGroup(id={self.id}, group_name={self.group_name})>"

class Document(Base):
    """
    Model representing a document.
    
    Attributes:
        - id: Primary key of the document (UUID).
        - file_name: Name of the file uploaded.
        - start_date: Start date of the document.
        - end_date: End date of the document.
        - description: Description of the document.
        - description_vector: Vector representation of the document description.
        - file_path: Path of the file uploaded.
        - document_metadata: Additional document_metadata in JSONB format (e.g., date, author).
        - tags: Many-to-many relationship with tags.
    """
    __tablename__ = 'documents'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    description_vector: Mapped[Vector] = mapped_column(Vector(1536))
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    document_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    content_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    
    # Timestamps in UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship to tags (many-to-many)
    tags: Mapped[List['Tag']] = relationship('Tag', secondary=document_tags, back_populates='documents')

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, file_name={self.file_name})>"

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
    file_extension: Mapped[str] = mapped_column(String(15), nullable=False)
    # Timestamps in UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<DocumentContent(id={self.id}, document_id={self.document_id})>"

class Tag(Base):
    """
    Model representing a tag for categorizing documents.
    
    Attributes:
        - id: Primary key of the tag.
        - tag_name: Name of the tag (e.g., 'contract', 'rental-related').
        - user_group_id: Foreign key referencing the user group.
        - documents: Many-to-many relationship with documents.
        - notify: Boolean indicating if notifications are needed.
        - notification_days_before_expiry: Days before document expiry to start notifications.
        - notification_frequency: Frequency of notifications in days.
    """
    __tablename__ = 'tags'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tag_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # New columns for notification settings
    notify: Mapped[bool] = mapped_column(default=False, nullable=False)
    notification_days_before_expiry: Mapped[int] = mapped_column(default=30, nullable=False)
    notification_frequency: Mapped[int] = mapped_column(default=7, nullable=False)

    # Timestamps in UTC
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationship to documents (many-to-many)
    documents: Mapped[List[Document]] = relationship('Document', secondary=document_tags, back_populates='tags')

    # Relationship to user groups (many-to-many)
    user_groups: Mapped[List[UserGroup]] = relationship('UserGroup', secondary=user_group_tags, back_populates='tags')

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, tag_name={self.tag_name})>"

# Create all tables in the database
# Base.metadata.create_all(engine)
