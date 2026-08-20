"""Application Settings using Pydantic Settings."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Uniplexity Migration Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # GCP Configuration
    GCP_PROJECT_ID: str = "uniplexity-migration-dev"
    GCS_BUCKET_NAME: str = "uniplexity-migration-uploads"
    PUB_SUB_TOPIC: str = "document-migration-queue"
    FIRESTORE_DATABASE: str = "(default)"
    
    # Gemini AI Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "mock-gemini-key")
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # Feature Flags / Mocks
    MOCK_GCP: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
