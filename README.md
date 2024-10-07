# Smart Document Management System

This project is a smart document management system that uses AI to process, categorize, and store documents intelligently.

## Features

- Streamlit-based user interface for easy interaction
- PostgreSQL database for storing metadata and vector representations
- OpenAI integration for intelligent document processing
- Automatic metadata extraction from various file formats
- AI-driven file naming and folder structure organization
- SharePoint integration for document storage
- Support for user authentication and group management
- Many-to-many relationships between documents, tags, and user groups

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your environment variables in `.env`
4. Run the application: `streamlit run app.py`

## Project Structure

- `src/`: Contains the main application code
  - `app.py`: Streamlit application for user interaction
  - `Dockerfile`: Docker configuration for containerization
  - `database.py`: Database operations using SQLAlchemy
  - `document_processor.py`: AI-powered document processing
  - `sharepoint_manager.py`: SharePoint integration
- `alembic/`: Database migration scripts
  - `versions/`: Contains migration version files
- `database/`: Contains database models and session management
  - `models.py`: SQLAlchemy models for documents, users, tags, and user groups
  - `session.py`: Database session management
- `tests/`: Unit tests for the application
- `config/`: Configuration files
- `.devcontainer/`: Development container configuration for VSCode

## Database Schema

The database schema includes the following tables:

- **documents**: Stores document metadata and content
- **tags**: Categorizes documents with tags
- **user_groups**: Manages user groups for access control
- **users**: Stores user information and authentication details
- **document_contents**: Contains raw content and vector representations of documents
- **document_tags**: Many-to-many relationship between documents and tags
- **usergroup_tags**: Many-to-many relationship between user groups and tags

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
