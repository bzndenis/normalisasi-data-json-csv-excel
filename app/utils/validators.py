"""
Custom Validators
=================
Custom validation functions for data normalization.
"""

import re
from typing import Optional
from email_validator import validate_email as email_validate, EmailNotValidError


def is_valid_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email string to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        email_validate(email)
        return True
    except EmailNotValidError:
        return False


def is_valid_sk_number(sk_number: str, pattern: Optional[str] = None) -> bool:
    """
    Validate SK (Surat Keputusan) number format
    
    Args:
        sk_number: SK number to validate
        pattern: Optional regex pattern to validate against
    
    Returns:
        True if valid, False otherwise
    """
    if pattern is None:
        # Default pattern: XXX/XXX/XXXX (flexible with separators)
        pattern = r'^\d+[/\-_][A-Za-z0-9]+[/\-_]\d{4}$'
    
    return bool(re.match(pattern, sk_number.strip()))


def has_excessive_whitespace(text: str) -> bool:
    """
    Check if text has excessive whitespace
    
    Args:
        text: Text to check
    
    Returns:
        True if has excessive whitespace, False otherwise
    """
    # Check for multiple consecutive spaces, tabs, or newlines
    return bool(re.search(r'\s{2,}', text))


def has_leading_trailing_spaces(text: str) -> bool:
    """
    Check if text has leading or trailing spaces
    
    Args:
        text: Text to check
    
    Returns:
        True if has leading/trailing spaces, False otherwise
    """
    return text != text.strip()


def has_special_characters(text: str, allowed_chars: str = '') -> bool:
    """
    Check if text contains special characters
    
    Args:
        text: Text to check
        allowed_chars: String of allowed special characters
    
    Returns:
        True if has special characters (not in allowed list), False otherwise
    """
    # Pattern: matches anything that's not alphanumeric, space, or in allowed_chars
    pattern = f'[^A-Za-z0-9\\s{re.escape(allowed_chars)}]'
    return bool(re.search(pattern, text))


def is_inconsistent_case(text: str) -> bool:
    """
    Check if text has inconsistent capitalization
    
    Args:
        text: Text to check
    
    Returns:
        True if has inconsistent case, False otherwise
    """
    # Check if text is mixed case (not all upper, not all lower, not title case)
    return (
        text != text.upper() and 
        text != text.lower() and 
        text != text.title() and
        any(c.isupper() for c in text) and 
        any(c.islower() for c in text)
    )
