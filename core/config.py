
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    """
    Application settings loaded from the environment.
    """
    # Database settings
    DATABASE_URL: str = f"sqlite:///{os.path.join(PROJECT_ROOT, 'db.sqlite3')}"

    # RAG pipeline settings
    KNOWLEDGE_BASE_DIR: str = os.path.join(PROJECT_ROOT, "knowledge_base")
    VECTOR_STORE_DIR: str = os.path.join(PROJECT_ROOT, "vector_store")
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    
    # Text splitting
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 100

    # LLM settings (placeholder)
    LLM_API_KEY: str = "YOUR_API_KEY_HERE"

    # Email notification settings
    SMTP_SERVER: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your-email@example.com"
    SMTP_PASSWORD: str = "your-password"
    NOTIFICATION_EMAIL_TO: str = "human-agent@example.com"

    # Specify the .env file to load
    model_config = SettingsConfigDict(env_file=os.path.join(PROJECT_ROOT, ".env"), extra="ignore")

# Instantiate the settings
settings = Settings()
