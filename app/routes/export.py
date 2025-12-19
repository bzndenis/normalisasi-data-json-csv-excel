"""
Export Routes
=============
API endpoints for exporting data.
"""

import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.schemas import ExportToFileRequest, ExportToDatabaseRequest, ExportResponse
from app.services.upload_handler import UploadHandler
from app.services.export_service import ExportService
from app.services.database_connector import DatabaseConnector
from app.config import settings
from app.utils.logger import app_logger


router = APIRouter(prefix="/api/export", tags=["Export"])


@router.post("/file", response_model=ExportResponse)
async def export_to_file(request: ExportToFileRequest):
    """
    Export data to file (CSV, Excel, or JSON)
    
    Args:
        request: Export request with file_id and format
    
    Returns:
        Export response with download URL
    """
    try:
        # Get data
        df = UploadHandler.get_data(request.file_id)
        
        # Export based on format
        if request.format == 'csv':
            file_path = ExportService.export_to_csv(df, request.filename)
        elif request.format == 'excel':
            file_path = ExportService.export_to_excel(df, request.filename)
        elif request.format == 'json':
            file_path = ExportService.export_to_json(df, request.filename)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {request.format}")
        
        download_url = ExportService.get_download_url(file_path)
        
        return ExportResponse(
            success=True,
            message=f"Data exported to {request.format.upper()} successfully",
            file_path=file_path,
            download_url=download_url
        )
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error exporting to file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/database", response_model=ExportResponse)
async def export_to_database(request: ExportToDatabaseRequest):
    """
    Export data to database table
    
    Args:
        request: Export request with file_id and database config
    
    Returns:
        Export response
    """
    try:
        # Get data
        df = UploadHandler.get_data(request.file_id)
        
        # Build connection string
        connection_string = DatabaseConnector.build_connection_string(request.connection)
        
        # Write to database
        rows_written = DatabaseConnector.write_table(
            df,
            connection_string,
            request.table_name,
            request.if_exists
        )
        
        return ExportResponse(
            success=True,
            message=f"{rows_written} rows saved to database table '{request.table_name}'"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error exporting to database: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download exported file
    
    Args:
        filename: Filename to download
    
    Returns:
        File response
    """
    # Resolve absolute path
    file_path = os.path.abspath(os.path.join(settings.EXPORT_DIR, filename))
    
    app_logger.info(f"Download request for: {filename}")
    app_logger.info(f"Resolved file path: {file_path}")
    app_logger.info(f"File exists: {os.path.exists(file_path)}")
    
    if not os.path.exists(file_path):
        app_logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")
    
    # Determine media type based on extension
    media_type = 'application/octet-stream'
    if filename.endswith('.xlsx'):
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif filename.endswith('.csv'):
        media_type = 'text/csv'
    elif filename.endswith('.json'):
        media_type = 'application/json'
    
    app_logger.info(f"Sending file: {filename} ({os.path.getsize(file_path)} bytes)")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
