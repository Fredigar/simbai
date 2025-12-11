"""
SIMBA Backend - Configuration

Configuration management using Pydantic Settings.
Loads from environment variables with .env file support.
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings"""

    # Application
    APP_NAME: str = "SIMBA"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./simba.db"

    # ChromaDB
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_data"

    # Redis (optional)
    REDIS_URL: str | None = None

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_ORG_ID: str | None = None

    # Anthropic
    ANTHROPIC_API_KEY: str | None = None

    # Other LLM Providers
    MISTRAL_API_KEY: str | None = None
    COHERE_API_KEY: str | None = None

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: List[str] = [
        "pdf", "docx", "xlsx", "pptx",
        "png", "jpg", "jpeg", "gif",
        "txt", "md", "csv"
    ]

    # RAG Settings
    RAG_TOP_K: int = 10
    RAG_CHUNK_SIZE: int = 1000
    RAG_CHUNK_OVERLAP: int = 200
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Tools Settings
    TOOLS_CONFIG_PATH: str = "./config/tools.yaml"
    TOOLS_TIMEOUT: int = 30

    # Confluence (example)
    CONFLUENCE_URL: str | None = None
    CONFLUENCE_USER: str | None = None
    CONFLUENCE_API_TOKEN: str | None = None

    # Jira (example)
    JIRA_URL: str | None = None
    JIRA_USER: str | None = None
    JIRA_API_TOKEN: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def max_upload_size_bytes(self) -> int:
        """Convert MB to bytes"""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    @property
    def chroma_url(self) -> str:
        """ChromaDB full URL"""
        return f"http://{self.CHROMA_HOST}:{self.CHROMA_PORT}"

    def get_llm_api_key(self, provider: str) -> str | None:
        """Get API key for specific LLM provider"""
        return getattr(self, f"{provider.upper()}_API_KEY", None)


# Singleton instance
settings = Settings()
