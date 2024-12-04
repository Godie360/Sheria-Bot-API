from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from config.prompts import get_contextualize_prompt, get_qa_prompt
from config.settings import settings
import os

def process_documents(docs_dir: str) -> List:
    """Process all PDF files in the specified directory"""
    all_docs = []
    
    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )
    
    # Process each PDF file in the directory
    for filename in os.listdir(docs_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(docs_dir, filename)
            try:
                loader = PyPDFLoader(file_path)
                docs = loader.load_and_split(text_splitter)
                all_docs.extend(docs)
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
                continue
    
    return all_docs

def build_history_aware_retriever(llm, retriever):
    contextualize_q_prompt = get_contextualize_prompt()
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    return history_aware_retriever

def build_qa_chain(llm):
    qa_prompt = get_qa_prompt()
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)
    return qa_chain