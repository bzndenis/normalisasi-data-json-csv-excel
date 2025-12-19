"""
Data Analyzer Service
=====================
Analyzes data quality and detects issues in columns.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app.models.schemas import ColumnIssue
from app.utils.validators import (
    has_excessive_whitespace,
    has_leading_trailing_spaces,
    has_special_characters,
    is_inconsistent_case,
    is_valid_email
)
from app.utils.logger import app_logger


class DataAnalyzer:
    """
    Service for analyzing data quality and detecting issues.
    """
    
    @staticmethod
    def analyze_dataframe(df: pd.DataFrame) -> List[ColumnIssue]:
        """
        Analyze all columns in a DataFrame
        
        Args:
            df: DataFrame to analyze
        
        Returns:
            List of ColumnIssue objects
        """
        column_issues = []
        
        for column in df.columns:
            issue = DataAnalyzer.analyze_column(df, column)
            column_issues.append(issue)
        
        app_logger.info(f"Analyzed {len(column_issues)} columns")
        return column_issues
    
    @staticmethod
    def analyze_column(df: pd.DataFrame, column: str) -> ColumnIssue:
        """
        Analyze a single column for issues
        
        Args:
            df: DataFrame
            column: Column name
        
        Returns:
            ColumnIssue object
        """
        total_rows = len(df)
        col_data = df[column]
        
        # Count null values
        null_count = col_data.isna().sum()
        null_percentage = (null_count / total_rows * 100) if total_rows > 0 else 0
        
        # Analyze non-null string values
        string_data = col_data.dropna().astype(str)
        
        # Check for leading/trailing spaces
        leading_trailing_count = sum(
            has_leading_trailing_spaces(str(val)) for val in string_data
        )
        
        # Check for excessive whitespace
        excessive_whitespace_count = sum(
            has_excessive_whitespace(str(val)) for val in string_data
        )
        
        # Check for inconsistent case
        inconsistent_case_count = sum(
            is_inconsistent_case(str(val)) for val in string_data
        )
        
        # Check for special characters
        special_chars_count = sum(
            has_special_characters(str(val)) for val in string_data
        )
        
        # Detect column type and perform specific validations
        invalid_emails = 0
        invalid_sk_numbers = 0
        
        # Simple email detection (column name contains 'email' or 'mail')
        if 'email' in column.lower() or 'mail' in column.lower():
            invalid_emails = sum(
                not is_valid_email(str(val)) for val in string_data if val
            )
        
        # Simple SK detection (column name contains 'sk' or 'nomor')
        if any(keyword in column.lower() for keyword in ['sk', 'nomor', 'number']):
            from app.utils.validators import is_valid_sk_number
            invalid_sk_numbers = sum(
                not is_valid_sk_number(str(val)) for val in string_data if val
            )
        
        # Get sample values (first 5 non-null unique values)
        sample_values = string_data.unique()[:5].tolist()
        
        return ColumnIssue(
            column_name=column,
            total_rows=total_rows,
            null_count=int(null_count),
            null_percentage=round(null_percentage, 2),
            has_leading_trailing_spaces=leading_trailing_count,
            has_excessive_whitespace=excessive_whitespace_count,
            has_inconsistent_case=inconsistent_case_count,
            has_special_characters=special_chars_count,
            invalid_emails=invalid_emails,
            invalid_sk_numbers=invalid_sk_numbers,
            sample_values=sample_values
        )
    
    @staticmethod
    def get_preview_data(df: pd.DataFrame, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get preview data from DataFrame
        
        Args:
            df: DataFrame
            limit: Number of rows to preview
        
        Returns:
            List of dictionaries representing rows
        """
        # Replace NaN with None for JSON serialization
        preview_df = df.head(limit).replace({np.nan: None})
        return preview_df.to_dict('records')
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics of DataFrame
        
        Args:
            df: DataFrame
        
        Returns:
            Dictionary with summary statistics
        """
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum(),
        }
