"""
Base Normalizer
===============
Abstract base class for all normalizers.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
import pandas as pd


class BaseNormalizer(ABC):
    """
    Abstract base class for all normalizers.
    
    All normalizer classes should inherit from this class and implement
    the normalize method.
    """
    
    def __init__(self, rules: Dict[str, Any] = None):
        """
        Initialize normalizer with rules
        
        Args:
            rules: Dictionary of normalization rules
        """
        self.rules = rules or {}
    
    @abstractmethod
    def normalize(self, value: Any) -> Any:
        """
        Normalize a single value
        
        Args:
            value: Value to normalize
        
        Returns:
            Normalized value
        """
        pass
    
    def normalize_series(self, series: pd.Series) -> pd.Series:
        """
        Normalize a pandas Series (column)
        
        Args:
            series: Pandas Series to normalize
        
        Returns:
            Normalized Series
        """
        return series.apply(self.normalize)
    
    def get_rule(self, key: str, default: Any = None) -> Any:
        """
        Get a rule value
        
        Args:
            key: Rule key
            default: Default value if key not found
        
        Returns:
            Rule value
        """
        return self.rules.get(key, default)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rules={self.rules})"
