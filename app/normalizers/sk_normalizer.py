"""
SK Number Normalizer
====================
Normalizes SK (Surat Keputusan) numbers.
"""

import re
from typing import Any
from app.normalizers.base import BaseNormalizer


class SKNormalizer(BaseNormalizer):
    """
    Normalizer for SK (Surat Keputusan) numbers.
    
    Supports:
    - Removing irrelevant symbols
    - Standardizing format (e.g., 123/ABC/2024)
    - Normalizing delimiters (/, -, _)
    - Pattern validation
    """
    
    DELIMITER_MAP = {
        'slash': '/',
        'dash': '-',
        'underscore': '_'
    }
    
    def normalize(self, value: Any) -> Any:
        """
        Normalize an SK number value
        
        Args:
            value: SK number value to normalize
        
        Returns:
            Normalized SK number value
        """
        # Handle None and empty values
        if value is None or value == '':
            return value
        
        # Convert to string and trim
        sk_number = str(value).strip()
        
        # Apply normalization rules
        
        # 1. Remove all special characters except numbers, letters, and common delimiters
        if self.get_rule('remove_special_chars', True):
            sk_number = re.sub(r'[^A-Za-z0-9/\-_]', '', sk_number)
        
        # 2. Standardize delimiter
        if self.get_rule('standardize_format', True):
            delimiter_type = self.get_rule('delimiter', 'slash')
            delimiter = self.DELIMITER_MAP.get(delimiter_type, '/')
            
            # Replace all delimiters with standardized one
            sk_number = re.sub(r'[/\-_]+', delimiter, sk_number)
        
        # 3. Validate pattern
        if self.get_rule('validate_pattern', True):
            pattern = self.get_rule('pattern')
            if pattern and not re.match(pattern, sk_number):
                # If custom pattern provided and doesn't match, return original
                return value
            elif not pattern:
                # Default validation: should have at least 2 delimiters
                delimiter_type = self.get_rule('delimiter', 'slash')
                delimiter = self.DELIMITER_MAP.get(delimiter_type, '/')
                if sk_number.count(delimiter) < 2:
                    return value
        
        return sk_number
    
    @staticmethod
    def extract_parts(sk_number: str, delimiter: str = '/') -> tuple:
        """
        Extract parts of SK number
        
        Args:
            sk_number: SK number string
            delimiter: Delimiter used in SK number
        
        Returns:
            Tuple of (number, code, year)
        """
        try:
            parts = sk_number.split(delimiter)
            if len(parts) >= 3:
                return parts[0], parts[1], parts[2]
            return None, None, None
        except Exception:
            return None, None, None
    
    @staticmethod
    def format_sk(number: str, code: str, year: str, delimiter: str = '/') -> str:
        """
        Format SK number from parts
        
        Args:
            number: SK number part
            code: Code part
            year: Year part
            delimiter: Delimiter to use
        
        Returns:
            Formatted SK number
        """
        return f"{number}{delimiter}{code}{delimiter}{year}"
    
    @staticmethod
    def validate_year(year: str) -> bool:
        """
        Validate year part of SK number
        
        Args:
            year: Year string
        
        Returns:
            True if valid 4-digit year, False otherwise
        """
        return bool(re.match(r'^\d{4}$', year))
