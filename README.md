# Enterprise-Knowledge-Hub

The Enterprise Knowledge Hub is a full-stack AI-powered document management and search platform designed to help organizations efficiently store, semantically retrieve, and analyze unstructured document data. It leverages FAISS-based semantic search, named entity recognition, and keyword extraction to enhance information discovery. This project is built built with MLOps for scalability and production-readiness, making it suitable for enterprise environments.

## Features
- Upload and store multiple PDFs for streamlined access.
- Uses FAISS-based vector search with Transformers to retrieve the most relevant documents based on meaning, not just keywords.
- Extracts text from PDF files, indexes them, and allows real-time searching.
- Intuitive Streamlit interface with a sidebar for document management and a centered search workflow.
- View search trends and insights after performing multiple queries.
- Previous search results clear automatically, and analytics are enabled only after historical searches.

## Directory Structure
    Enterprise-Knowledge-Hub/
    ├── app/
    │   ├── __init__.py
    │   ├── analytics.py
    │   ├── main.py
    │   ├── ml_pipeline.py
    │   ├── search.py
    ├── requirements.txt
    └── Dockerfile

## Technologies Used
- Python (Core Language)
- Streamlit (Frontend UI)
- FAISS (Fast document retrieval)
- Sentence Transformers (Semantic search with all-MiniLM-L6-v2)
- Spacy & KeyBERT (Entity recognition & keyword extraction)
- PyPDF2 (Document processing)
- Docker (For containerized deployment)

## Installation & Setup
### Prerequisites
- Python 3.8+
- Pip & Virtual Environment
- Docker (Optional for deployment)
#### 1. Clone the Repository
```
$ git clone https://github.com/your-repo/enterprise-knowledge-hub.git
$ cd enterprise-knowledge-hub
```
#### 2. Install Dependencies
```
$ pip install -r requirements.txt
```
#### 3. Run the Application
```
$ streamlit run app/main.py
```
#### Deployment
To deploy using Docker:
```
$ docker build -t knowledge-hub .
$ docker run -p 8501:8501 knowledge-hub
```

## Usage Guide
- Upload Documents: Use the upload button in the center to add PDFs.
- Manage Documents: Uploaded documents appear in the sidebar, where you can hover to download.
- Search: Enter a query in the search bar to find relevant documents.
- Analyze Trends: The analytics button becomes active after multiple searches, allowing data insights.
