"""
Normalization Routes
====================
API endpoints for data normalization operations.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import NormalizationRequest, NormalizationResponse, PreviewComparison
from app.services.upload_handler import UploadHandler
from app.services.normalization_engine import NormalizationEngine
from app.services.data_analyzer import DataAnalyzer
from app.utils.logger import app_logger


router = APIRouter(prefix="/api/normalize", tags=["Normalization"])


@router.post("/", response_model=NormalizationResponse)
async def normalize_data(request: NormalizationRequest):
    """
    Normalize data based on column configurations
    
    Args:
        request: Normalization request with file_id and column configs
    
    Returns:
        Normalization response with new file_id and statistics
    """
    try:
        # Get original data
        original_df = UploadHandler.get_data(request.file_id)
        
        # Normalize data
        normalized_df, statistics = NormalizationEngine.normalize_dataframe(
            original_df,
            request.columns_config
        )
        
        # Generate new file ID for normalized data
        normalized_file_id = UploadHandler.generate_file_id()
        UploadHandler.store_data(normalized_file_id, normalized_df)
        
        app_logger.info(
            f"Normalization completed: {request.file_id} -> {normalized_file_id}"
        )
        
        return NormalizationResponse(
            success=True,
            message="Data normalized successfully",
            normalized_file_id=normalized_file_id,
            statistics=statistics
        )
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error normalizing data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preview/{original_file_id}/{normalized_file_id}", response_model=PreviewComparison)
async def preview_normalization(original_file_id: str, normalized_file_id: str, limit: int = 10):
    """
    Preview normalization changes (before vs after)
    
    Args:
        original_file_id: Original file ID
        normalized_file_id: Normalized file ID
        limit: Number of rows to preview
    
    Returns:
        Preview comparison with original and normalized data
    """
    try:
        # Get both datasets
        original_df = UploadHandler.get_data(original_file_id)
        normalized_df = UploadHandler.get_data(normalized_file_id)
        
        # Get preview data
        original_preview = DataAnalyzer.get_preview_data(original_df, limit)
        normalized_preview = DataAnalyzer.get_preview_data(normalized_df, limit)
        
        # Calculate statistics for all columns
        statistics = []
        for column in original_df.columns:
            if column in normalized_df.columns:
                stats = NormalizationEngine._calculate_statistics(
                    column,
                    original_df[column],
                    normalized_df[column]
                )
                statistics.append(stats)
        
        return PreviewComparison(
            original_data=original_preview,
            normalized_data=normalized_preview,
            changes_summary=statistics
        )
    
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error previewing normalization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
