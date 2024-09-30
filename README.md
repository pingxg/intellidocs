# Smart Document Management System

This project is a smart document management system that uses AI to process, categorize, and store documents intelligently.

## Features

- Streamlit-based user interface for easy interaction
- PostgreSQL database for storing metadata and vector representations
- OpenAI integration for intelligent document processing
- Automatic metadata extraction from various file formats
- AI-driven file naming and folder structure organization
- SharePoint integration for document storage

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your environment variables in `.env`
4. Run the application: `streamlit run src/app.py`

## Project Structure

- `src/`: Contains the main application code
  - `app.py`: Streamlit application
  - `database.py`: Database operations using SQLAlchemy
  - `document_processor.py`: AI-powered document processing
  - `sharepoint_manager.py`: SharePoint integration
- `tests/`: Unit tests
- `config/`: Configuration files

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
