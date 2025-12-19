"""
Pydantic Schemas
================
Data validation and serialization models using Pydantic.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Any, Literal
from datetime import datetime


# ============================================================================
# DATABASE CONNECTION SCHEMAS
# ============================================================================

class DatabaseConnectionSchema(BaseModel):
    """Database connection configuration"""
    db_type: Literal["mysql", "postgresql"]
    host: str
    port: int
    username: str
    password: str
    database: str
    table: str


# ============================================================================
# UPLOAD SCHEMAS
# ============================================================================

class UploadResponse(BaseModel):
    """Response after file upload"""
    success: bool
    message: str
    file_id: str
    filename: str
    rows: int
    columns: List[str]


# ============================================================================
# DATA ANALYSIS SCHEMAS
# ============================================================================

class ColumnIssue(BaseModel):
    """Issues found in a column"""
    column_name: str
    total_rows: int
    null_count: int
    null_percentage: float
    has_leading_trailing_spaces: int
    has_excessive_whitespace: int
    has_inconsistent_case: int
    has_special_characters: int
    invalid_emails: int = 0  # Only for email columns
    invalid_sk_numbers: int = 0  # Only for SK columns
    sample_values: List[Any] = Field(default_factory=list)


class DataAnalysisResponse(BaseModel):
    """Response from data analysis"""
    file_id: str
    total_rows: int
    total_columns: int
    column_issues: List[ColumnIssue]
    preview_data: List[Dict[str, Any]]


# ============================================================================
# NORMALIZATION SCHEMAS
# ============================================================================

class TextNormalizationRules(BaseModel):
    """Text normalization rules configuration"""
    trim_spaces: bool = True
    remove_excessive_whitespace: bool = True
    case_conversion: Optional[Literal["upper", "lower", "title"]] = None
    remove_special_chars: bool = False
    allowed_special_chars: str = ""


class EmailNormalizationRules(BaseModel):
    """Email normalization rules configuration"""
    to_lowercase: bool = True
    trim_spaces: bool = True
    validate_format: bool = True
    validate_domain: bool = False


class SKNormalizationRules(BaseModel):
    """SK number normalization rules configuration"""
    remove_special_chars: bool = True
    standardize_format: bool = True
    delimiter: Literal["slash", "dash", "underscore"] = "slash"
    validate_pattern: bool = True
    pattern: Optional[str] = None


class ColumnNormalizationConfig(BaseModel):
    """Normalization configuration for a single column"""
    column_name: str
    enabled: bool = True
    column_type: Literal["text", "email", "sk", "other"] = "text"
    text_rules: Optional[TextNormalizationRules] = None
    email_rules: Optional[EmailNormalizationRules] = None
    sk_rules: Optional[SKNormalizationRules] = None


class NormalizationRequest(BaseModel):
    """Request to normalize data"""
    file_id: str
    columns_config: List[ColumnNormalizationConfig]


class NormalizationStatistics(BaseModel):
    """Statistics about normalization changes"""
    column_name: str
    rows_changed: int
    rows_unchanged: int
    change_percentage: float


class NormalizationResponse(BaseModel):
    """Response from normalization"""
    success: bool
    message: str
    normalized_file_id: str
    statistics: List[NormalizationStatistics]


# ============================================================================
# PREVIEW SCHEMAS
# ============================================================================

class PreviewComparison(BaseModel):
    """Before and after comparison for preview"""
    original_data: List[Dict[str, Any]]
    normalized_data: List[Dict[str, Any]]
    changes_summary: List[NormalizationStatistics]


# ============================================================================
# EXPORT SCHEMAS
# ============================================================================

class ExportToFileRequest(BaseModel):
    """Request to export data to file"""
    file_id: str
    format: Literal["csv", "excel", "json"]
    filename: Optional[str] = None


class ExportToDatabaseRequest(BaseModel):
    """Request to export data to database"""
    file_id: str
    connection: DatabaseConnectionSchema
    table_name: str
    if_exists: Literal["fail", "replace", "append"] = "replace"


class ExportResponse(BaseModel):
    """Response from export operation"""
    success: bool
    message: str
    file_path: Optional[str] = None
    download_url: Optional[str] = None


# ============================================================================
# ERROR RESPONSE
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    details: Optional[str] = None
