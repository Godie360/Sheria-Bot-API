# services/llm_service.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from config.settings import settings

def get_llm():
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.llm_name,             
        temperature=settings.llm_temperature   
    )

def get_embeddings():
    return OpenAIEmbeddings(
        api_key=settings.openai_api_key,
        model=settings.embedding_name,         
        dimensions=settings.embedding_dimensions
    )
