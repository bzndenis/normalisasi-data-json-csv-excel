"""
Analysis Routes
===============
API endpoints for data analysis operations.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import DataAnalysisResponse
from app.services.upload_handler import UploadHandler
from app.services.data_analyzer import DataAnalyzer
from app.utils.logger import app_logger


router = APIRouter(prefix="/api/analysis", tags=["Analysis"])


@router.get("/{file_id}", response_model=DataAnalysisResponse)
async def analyze_data(file_id: str):
    """
    Analyze data quality for uploaded file
    
    Args:
        file_id: File ID from upload
    
    Returns:
        Data analysis response with issues and preview
    """
    try:
        # Get data
        df = UploadHandler.get_data(file_id)
        
        # Analyze columns
        column_issues = DataAnalyzer.analyze_dataframe(df)
        
        # Get preview data
        preview_data = DataAnalyzer.get_preview_data(df, limit=10)
        
        app_logger.info(f"Analysis completed for file_id: {file_id}")
        
        return DataAnalysisResponse(
            file_id=file_id,
            total_rows=len(df),
            total_columns=len(df.columns),
            column_issues=column_issues,
            preview_data=preview_data
        )
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error analyzing data for file_id {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
