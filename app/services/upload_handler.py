"""
Upload Handler Service
======================
Handles file upload operations and data reading from various sources.
"""

import os
import uuid
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List, Tuple
from fastapi import UploadFile, HTTPException
from app.config import settings
from app.utils.logger import app_logger


class UploadHandler:
    """
    Service for handling file uploads and initial data reading.
    """
    
    # In-memory storage for uploaded data (for demo purposes)
    # In production, consider using Redis or database
    _data_store: Dict[str, pd.DataFrame] = {}
    
    @staticmethod
    def generate_file_id() -> str:
        """Generate unique file ID"""
        return str(uuid.uuid4())
    
    @classmethod
    async def handle_file_upload(
        cls,
        file: UploadFile
    ) -> Tuple[str, pd.DataFrame, str]:
        """
        Handle file upload and read data
        
        Args:
            file: Uploaded file object
        
        Returns:
            Tuple of (file_id, dataframe, original_filename)
        
        Raises:
            HTTPException: If file is invalid or cannot be read
        """
        # Validate file
        cls._validate_file(file)
        
        # Generate file ID
        file_id = cls.generate_file_id()
        
        # Save file temporarily
        file_path = cls._save_uploaded_file(file, file_id)
        
        try:
            # Read file into DataFrame
            df = cls._read_file_to_dataframe(file_path, file.filename)
            
            # Store in memory
            cls._data_store[file_id] = df
            
            app_logger.info(
                f"File uploaded successfully: {file.filename} "
                f"(ID: {file_id}, Rows: {len(df)}, Columns: {len(df.columns)})"
            )
            
            return file_id, df, file.filename
            
        except Exception as e:
            # Clean up file if reading failed
            if os.path.exists(file_path):
                os.remove(file_path)
            app_logger.error(f"Error reading file {file.filename}: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error reading file: {str(e)}"
            )
    
    @classmethod
    def read_from_database(
        cls,
        connection_string: str,
        table: str
    ) -> Tuple[str, pd.DataFrame]:
        """
        Read data from database
        
        Args:
            connection_string: Database connection string
            table: Table name
        
        Returns:
            Tuple of (file_id, dataframe)
        
        Raises:
            HTTPException: If database connection fails
        """
        from sqlalchemy import create_engine
        
        try:
            # Create database engine
            engine = create_engine(connection_string)
            
            # Read table into DataFrame
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, engine)
            
            # Generate file ID
            file_id = cls.generate_file_id()
            
            # Store in memory
            cls._data_store[file_id] = df
            
            app_logger.info(
                f"Data read from database successfully: {table} "
                f"(ID: {file_id}, Rows: {len(df)}, Columns: {len(df.columns)})"
            )
            
            return file_id, df
            
        except Exception as e:
            app_logger.error(f"Error reading from database: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error reading from database: {str(e)}"
            )
    
    @classmethod
    def get_data(cls, file_id: str) -> pd.DataFrame:
        """
        Get data by file ID
        
        Args:
            file_id: File ID
        
        Returns:
            DataFrame
        
        Raises:
            HTTPException: If file_id not found
        """
        if file_id not in cls._data_store:
            raise HTTPException(
                status_code=404,
                detail=f"File ID not found: {file_id}"
            )
        return cls._data_store[file_id].copy()
    
    @classmethod
    def store_data(cls, file_id: str, df: pd.DataFrame) -> None:
        """
        Store data with file ID
        
        Args:
            file_id: File ID
            df: DataFrame to store
        """
        cls._data_store[file_id] = df.copy()
    
    @staticmethod
    def _validate_file(file: UploadFile) -> None:
        """
        Validate uploaded file
        
        Args:
            file: Uploaded file object
        
        Raises:
            HTTPException: If file is invalid
        """
        # Check file extension
        extension = Path(file.filename).suffix.lower().lstrip('.')
        if extension not in settings.allowed_extensions_list:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(settings.allowed_extensions_list)}"
            )
    
    @staticmethod
    def _save_uploaded_file(file: UploadFile, file_id: str) -> str:
        """
        Save uploaded file to disk
        
        Args:
            file: Uploaded file object
            file_id: Generated file ID
        
        Returns:
            Path to saved file
        """
        # Get file extension
        extension = Path(file.filename).suffix
        
        # Create filename with file_id
        filename = f"{file_id}{extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        return file_path
    
    @staticmethod
    def _read_file_to_dataframe(file_path: str, original_filename: str) -> pd.DataFrame:
        """
        Read file into pandas DataFrame
        
        Args:
            file_path: Path to file
            original_filename: Original filename (to determine type)
        
        Returns:
            DataFrame
        
        Raises:
            ValueError: If file type is unsupported or file cannot be read
        """
        extension = Path(original_filename).suffix.lower()
        
        if extension == '.csv':
            return pd.read_csv(file_path)
        elif extension == '.json':
            return pd.read_json(file_path)
        elif extension in ['.xls', '.xlsx']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
