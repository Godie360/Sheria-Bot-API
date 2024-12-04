from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # OpenAI Settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY")
    
    # Directory Settings
    docs_dir: str = "documents"
    db_dir: str = "db"
    
    # LLM Settings
    llm_name: str = "gpt-4o-mini"           # Changed from model_name
    llm_temperature: float = 0.6            # Changed from model_temperature
    embedding_name: str = "text-embedding-3-large"
    embedding_dimensions: int = 1536
    
    # Document Processing
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # CORS Settings
    allowed_origins: list = ["*"]
    allowed_methods: list = ["*"]
    allowed_headers: list = ["*"]
    
    model_config = {
        'protected_namespaces': ('settings_',),  # Add this to fix namespace warning
        'extra': 'ignore'  # Allow extra fields in environment variables
    }

settings = Settings()