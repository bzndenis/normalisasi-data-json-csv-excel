"""
Normalization Engine Service
============================
Orchestrates data normalization using modular normalizers.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app.models.schemas import (
    ColumnNormalizationConfig,
    NormalizationStatistics
)
from app.normalizers.text_normalizer import TextNormalizer
from app.normalizers.email_normalizer import EmailNormalizer
from app.normalizers.sk_normalizer import SKNormalizer
from app.utils.logger import normalization_logger


class NormalizationEngine:
    """
    Service that orchestrates data normalization using modular normalizers.
    """
    
    @staticmethod
    def normalize_dataframe(
        df: pd.DataFrame,
        columns_config: List[ColumnNormalizationConfig]
    ) -> tuple[pd.DataFrame, List[NormalizationStatistics]]:
        """
        Normalize DataFrame based on column configurations
        
        Args:
            df: DataFrame to normalize
            columns_config: List of column normalization configurations
        
        Returns:
            Tuple of (normalized_df, statistics)
        """
        normalized_df = df.copy()
        statistics = []
        
        for config in columns_config:
            if not config.enabled:
                continue
            
            column_name = config.column_name
            
            if column_name not in normalized_df.columns:
                normalization_logger.warning(f"Column '{column_name}' not found in DataFrame")
                continue
            
            # Store original data for comparison
            original_series = normalized_df[column_name].copy()
            
            # Apply normalization based on column type
            try:
                if config.column_type == 'text' and config.text_rules:
                    normalizer = TextNormalizer(config.text_rules.model_dump())
                    normalized_df[column_name] = normalizer.normalize_series(normalized_df[column_name])
                
                elif config.column_type == 'email' and config.email_rules:
                    normalizer = EmailNormalizer(config.email_rules.model_dump())
                    normalized_df[column_name] = normalizer.normalize_series(normalized_df[column_name])
                
                elif config.column_type == 'sk' and config.sk_rules:
                    normalizer = SKNormalizer(config.sk_rules.model_dump())
                    normalized_df[column_name] = normalizer.normalize_series(normalized_df[column_name])
                
                # Calculate statistics
                stats = NormalizationEngine._calculate_statistics(
                    column_name,
                    original_series,
                    normalized_df[column_name]
                )
                statistics.append(stats)
                
                normalization_logger.info(
                    f"Normalized column '{column_name}' - "
                    f"{stats.rows_changed} rows changed ({stats.change_percentage:.2f}%)"
                )
                
            except Exception as e:
                normalization_logger.error(f"Error normalizing column '{column_name}': {str(e)}")
                # Revert to original if error
                normalized_df[column_name] = original_series
        
        return normalized_df, statistics
    
    @staticmethod
    def _calculate_statistics(
        column_name: str,
        original: pd.Series,
        normalized: pd.Series
    ) -> NormalizationStatistics:
        """
        Calculate normalization statistics for a column
        
        Args:
            column_name: Name of the column
            original: Original series
            normalized: Normalized series
        
        Returns:
            NormalizationStatistics object
        """
        # Compare original and normalized values
        # Handle NaN values in comparison
        original_str = original.fillna('').astype(str)
        normalized_str = normalized.fillna('').astype(str)
        
        changed_mask = original_str != normalized_str
        rows_changed = changed_mask.sum()
        rows_unchanged = len(original) - rows_changed
        change_percentage = (rows_changed / len(original) * 100) if len(original) > 0 else 0
        
        return NormalizationStatistics(
            column_name=column_name,
            rows_changed=int(rows_changed),
            rows_unchanged=int(rows_unchanged),
            change_percentage=round(change_percentage, 2)
        )
    
    @staticmethod
    def get_changes_details(
        original_df: pd.DataFrame,
        normalized_df: pd.DataFrame,
        column_name: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get detailed changes for a specific column
        
        Args:
            original_df: Original DataFrame
            normalized_df: Normalized DataFrame
            column_name: Column to get changes for
            limit: Maximum number of changes to return
        
        Returns:
            List of change details
        """
        changes = []
        
        if column_name not in original_df.columns or column_name not in normalized_df.columns:
            return changes
        
        original = original_df[column_name].fillna('').astype(str)
        normalized = normalized_df[column_name].fillna('').astype(str)
        
        changed_indices = original != normalized
        changed_rows = original_df.index[changed_indices].tolist()[:limit]
        
        for idx in changed_rows:
            changes.append({
                'row_index': int(idx),
                'original_value': original.iloc[idx],
                'normalized_value': normalized.iloc[idx]
            })
        
        return changes
