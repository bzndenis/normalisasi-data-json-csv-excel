"""
Email Normalizer
================
Normalizes email addresses.
"""

import re
from typing import Any
from app.normalizers.base import BaseNormalizer
from app.utils.validators import is_valid_email


class EmailNormalizer(BaseNormalizer):
    """
    Normalizer for email addresses.
    
    Supports:
    - Converting to lowercase
    - Trimming spaces
    - Email format validation
    - Domain validation (optional)
    """
    
    # Common valid email domains for validation
    COMMON_DOMAINS = [
        'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
        'live.com', 'icloud.com', 'mail.com', 'aol.com',
        'go.id', 'ac.id', 'co.id'  # Indonesian domains
    ]
    
    def normalize(self, value: Any) -> Any:
        """
        Normalize an email value
        
        Args:
            value: Email value to normalize
        
        Returns:
            Normalized email value
        """
        # Handle None and empty values
        if value is None or value == '':
            return value
        
        # Convert to string
        email = str(value)
        
        # Apply normalization rules
        
        # 1. Trim spaces
        if self.get_rule('trim_spaces', True):
            email = email.strip()
        
        # 2. Convert to lowercase
        if self.get_rule('to_lowercase', True):
            email = email.lower()
        
        # 3. Remove all whitespace (emails shouldn't have spaces)
        email = re.sub(r'\s+', '', email)
        
        # 4. Validate format
        if self.get_rule('validate_format', True):
            if not self._is_valid_format(email):
                # Return original if invalid (or could return None/empty)
                return value
        
        # 5. Validate domain (optional)
        if self.get_rule('validate_domain', False):
            if not self._is_valid_domain(email):
                # Return original if invalid domain
                return value
        
        return email
    
    @staticmethod
    def _is_valid_format(email: str) -> bool:
        """
        Check if email has valid format
        
        Args:
            email: Email to validate
        
        Returns:
            True if valid format, False otherwise
        """
        return is_valid_email(email)
    
    @staticmethod
    def _is_valid_domain(email: str) -> bool:
        """
        Check if email domain is in common domains list
        
        Args:
            email: Email to validate
        
        Returns:
            True if domain is valid, False otherwise
        """
        try:
            domain = email.split('@')[1]
            return domain in EmailNormalizer.COMMON_DOMAINS
        except (IndexError, AttributeError):
            return False
    
    @staticmethod
    def extract_domain(email: str) -> str:
        """
        Extract domain from email
        
        Args:
            email: Email address
        
        Returns:
            Domain part of email
        """
        try:
            return email.split('@')[1]
        except (IndexError, AttributeError):
            return ''
