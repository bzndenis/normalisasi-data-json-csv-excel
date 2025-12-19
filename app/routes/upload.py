"""
Upload Routes
=============
API endpoints for file upload operations.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import UploadResponse, ErrorResponse
from app.services.upload_handler import UploadHandler
from app.utils.logger import app_logger


router = APIRouter(prefix="/api/upload", tags=["Upload"])


@router.post("/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a file (JSON, CSV, or Excel)
    
    Args:
        file: Uploaded file
    
    Returns:
        Upload response with file ID and basic info
    """
    try:
        file_id, df, filename = await UploadHandler.handle_file_upload(file)
        
        return UploadResponse(
            success=True,
            message="File uploaded successfully",
            file_id=file_id,
            filename=filename,
            rows=len(df),
            columns=df.columns.tolist()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Unexpected error in file upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
