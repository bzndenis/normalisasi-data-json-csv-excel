"""
Database Routes
===============
API endpoints for database connection operations.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import DatabaseConnectionSchema, UploadResponse
from app.services.database_connector import DatabaseConnector
from app.services.upload_handler import UploadHandler
from app.utils.logger import app_logger


router = APIRouter(prefix="/api/database", tags=["Database"])


@router.post("/connect", response_model=UploadResponse)
async def connect_database(config: DatabaseConnectionSchema):
    """
    Connect to database and read table data
    
    Args:
        config: Database connection configuration
    
    Returns:
        Upload response with file ID and basic info
    """
    try:
        # Build connection string
        connection_string = DatabaseConnector.build_connection_string(config)
        
        # Test connection
        DatabaseConnector.test_connection(connection_string)
        
        # Read table
        df = DatabaseConnector.read_table(connection_string, config.table)
        
        # Generate file ID and store data
        file_id = UploadHandler.generate_file_id()
        UploadHandler.store_data(file_id, df)
        
        app_logger.info(
            f"Database connected successfully: {config.db_type}://{config.host}/{config.database}.{config.table}"
        )
        
        return UploadResponse(
            success=True,
            message="Database connected successfully",
            file_id=file_id,
            filename=f"{config.database}.{config.table}",
            rows=len(df),
            columns=df.columns.tolist()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Unexpected error in database connection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test_connection(config: DatabaseConnectionSchema):
    """
    Test database connection
    
    Args:
        config: Database connection configuration
    
    Returns:
        Success message
    """
    try:
        connection_string = DatabaseConnector.build_connection_string(config)
        DatabaseConnector.test_connection(connection_string)
        
        return {
            "success": True,
            "message": "Database connection successful"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Database connection test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
