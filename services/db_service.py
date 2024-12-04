# services/db_service.py
from langchain_chroma import Chroma
from services.llm_service import get_embeddings
from config.settings import settings
from utils import process_documents
import os

def get_db():
    embedding = get_embeddings()
    # Configure the retriever with specific parameters
    return Chroma(
        persist_directory=settings.db_dir,
        embedding_function=embedding,
    ).as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": 3,  # Number of documents to retrieve
            "score_threshold": 0.5,  # Minimum similarity score
        }
    )

def initialize_database():
    """Initialize the vector database with documents from the documents directory"""
    try:
        # Process all PDF files in the documents directory
        docs = process_documents(settings.docs_dir)
        if not docs:
            print("No documents found to process")
            return False
            
        # Create or update the vector database
        embedding = get_embeddings()
        db = Chroma.from_documents(
            persist_directory=settings.db_dir,
            documents=docs,
            embedding=embedding
        )
        print(f"Database initialized successfully with {len(docs)} chunks")
        return True
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        return False