"""
Export Service
==============
Handles data export operations to various formats.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from app.config import settings
from app.utils.logger import app_logger
from fastapi import HTTPException


class ExportService:
    """
    Service for exporting data to various formats.
    """
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: str = None) -> str:
        """
        Export DataFrame to CSV file
        
        Args:
            df: DataFrame to export
            filename: Optional filename (will be generated if not provided)
        
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.csv"
        
        # Ensure .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        file_path = os.path.join(settings.EXPORT_DIR, filename)
        
        try:
            df.to_csv(file_path, index=False, encoding='utf-8')
            app_logger.info(f"Exported to CSV: {file_path}")
            return file_path
        except Exception as e:
            app_logger.error(f"Error exporting to CSV: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error exporting to CSV: {str(e)}"
            )
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, filename: str = None) -> str:
        """
        Export DataFrame to Excel file
        
        Args:
            df: DataFrame to export
            filename: Optional filename (will be generated if not provided)
        
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.xlsx"
        
        # Ensure .xlsx extension
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        file_path = os.path.join(settings.EXPORT_DIR, filename)
        
        try:
            df.to_excel(file_path, index=False, engine='openpyxl')
            app_logger.info(f"Exported to Excel: {file_path}")
            return file_path
        except Exception as e:
            app_logger.error(f"Error exporting to Excel: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error exporting to Excel: {str(e)}"
            )
    
    @staticmethod
    def export_to_json(df: pd.DataFrame, filename: str = None) -> str:
        """
        Export DataFrame to JSON file
        
        Args:
            df: DataFrame to export
            filename: Optional filename (will be generated if not provided)
        
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"export_{timestamp}.json"
        
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        file_path = os.path.join(settings.EXPORT_DIR, filename)
        
        try:
            # Replace NaN with None for proper JSON serialization
            df_clean = df.replace({np.nan: None})
            df_clean.to_json(file_path, orient='records', indent=2, force_ascii=False)
            app_logger.info(f"Exported to JSON: {file_path}")
            return file_path
        except Exception as e:
            app_logger.error(f"Error exporting to JSON: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error exporting to JSON: {str(e)}"
            )
    
    @staticmethod
    def get_download_url(file_path: str) -> str:
        """
        Get download URL for exported file
        
        Args:
            file_path: Path to file
        
        Returns:
            Download URL
        """
        filename = Path(file_path).name
        return f"/api/export/download/{filename}"
