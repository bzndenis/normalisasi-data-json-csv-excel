"""
Configuration Management
========================
Manages application configuration from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Data Normalization App"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: str = "json,csv,xls,xlsx"
    UPLOAD_DIR: str = "uploads"
    EXPORT_DIR: str = "exports"
    
    # Database
    DB_TYPE: str = "postgresql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_NAME: str = "gokendali_dev"
    
    # Logging
    LOG_DIR: str = "logs"
    LOG_FILE_MAX_BYTES: int = 10485760
    LOG_FILE_BACKUP_COUNT: int = 5
    
    # Normalization Defaults
    DEFAULT_TEXT_CASE: str = "title"
    DEFAULT_EMAIL_DOMAIN_VALIDATION: bool = False
    DEFAULT_SK_FORMAT: str = "slash"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get list of allowed file extensions"""
        return self.ALLOWED_EXTENSIONS.split(",")
    
    @property
    def database_url(self) -> str:
        """Get database URL for SQLAlchemy"""
        if self.DB_TYPE == "postgresql":
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:  # mysql
            return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.UPLOAD_DIR,
            self.EXPORT_DIR,
            self.LOG_DIR,
            "data"
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Ensure directories exist
settings.ensure_directories()
