"""
Text Normalizer
===============
Normalizes general text data.
"""

import re
from typing import Any
from app.normalizers.base import BaseNormalizer


class TextNormalizer(BaseNormalizer):
    """
    Normalizer for general text data.
    
    Supports:
    - Trimming spaces
    - Removing excessive whitespace
    - Case conversion (UPPER, lower, Title)
    - Removing special characters
    """
    
    def normalize(self, value: Any) -> Any:
        """
        Normalize a text value
        
        Args:
            value: Text value to normalize
        
        Returns:
            Normalized text value
        """
        # Handle None and non-string values
        if value is None or value == '':
            return value
        
        # Convert to string
        text = str(value)
        
        # Apply normalization rules
        
        # 1. Trim leading/trailing spaces
        if self.get_rule('trim_spaces', True):
            text = text.strip()
        
        # 2. Remove excessive whitespace (multiple spaces, tabs, newlines)
        if self.get_rule('remove_excessive_whitespace', True):
            text = re.sub(r'\s+', ' ', text)
        
        # 3. Case conversion
        case_conversion = self.get_rule('case_conversion')
        if case_conversion == 'upper':
            text = text.upper()
        elif case_conversion == 'lower':
            text = text.lower()
        elif case_conversion == 'title':
            text = text.title()
        
        # 4. Remove special characters
        if self.get_rule('remove_special_chars', False):
            allowed_chars = self.get_rule('allowed_special_chars', '')
            # Keep alphanumeric, spaces, and allowed special characters
            pattern = f'[^A-Za-z0-9\\s{re.escape(allowed_chars)}]'
            text = re.sub(pattern, '', text)
        
        return text
    
    @staticmethod
    def remove_special_characters(text: str, allowed: str = '') -> str:
        """
        Remove special characters from text
        
        Args:
            text: Text to process
            allowed: String of allowed special characters
        
        Returns:
            Text without special characters
        """
        pattern = f'[^A-Za-z0-9\\s{re.escape(allowed)}]'
        return re.sub(pattern, '', text)
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """
        Normalize whitespace in text (convert multiple spaces to single space)
        
        Args:
            text: Text to process
        
        Returns:
            Text with normalized whitespace
        """
        return re.sub(r'\s+', ' ', text.strip())
