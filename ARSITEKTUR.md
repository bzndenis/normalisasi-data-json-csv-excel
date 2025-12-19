# Arsitektur Aplikasi Data Normalization

## 📐 Overview Arsitektur

Aplikasi ini dibangun dengan arsitektur **modular dan layered** untuk memudahkan maintenance, testing, dan pengembangan future features.

## 🏛️ Arsitektur Layers

```
┌─────────────────────────────────────────────────┐
│           PRESENTATION LAYER (Frontend)         │
│    HTML Templates + CSS + Vanilla JavaScript    │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│              API LAYER (Routes)                 │
│   FastAPI Routers - HTTP Request Handling       │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│          BUSINESS LOGIC LAYER (Services)        │
│  Upload, Analysis, Normalization, Export Logic  │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│         DOMAIN LOGIC (Normalizers)              │
│   Text, Email, SK Normalization Rules           │
└─────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────┐
│         DATA LAYER (Storage & Database)         │
│   In-Memory Store, File System, SQL Databases   │
└─────────────────────────────────────────────────┘
```

## 📦 Component Breakdown

### 1. **Presentation Layer** (`templates/`, `static/`)

**Tanggung Jawab**:
- Rendering HTML pages
- User interaction handling
- Client-side form validation
- API calls via JavaScript

**Komponen Utama**:
- `base.html`: Template dasar dengan header & navigation
- `index.html`: Homepage dengan feature showcase
- `upload.html`: Upload interface (file & database)
- `analysis.html`: Data quality analysis display
- `normalization.html`: Normalization rule configuration
- `preview.html`: Before/After comparison
- `export.html`: Export options

**Design Pattern**: Template Inheritance (Jinja2)

---

### 2. **API Layer** (`app/routes/`)

**Tanggung Jawab**:
- HTTP request/response handling
- Input validation (Pydantic)
- Error handling & status codes
- API documentation (OpenAPI)

**Komponen**:

#### `upload.py`
```python
POST /api/upload/file
- Upload file (JSON, CSV, Excel)
- Return: file_id, basic metadata
```

#### `database.py`
```python
POST /api/database/connect
- Connect to MySQL/PostgreSQL
- Read table data
- Return: file_id

POST /api/database/test
- Test database connection
```

#### `analysis.py`
```python
GET /api/analysis/{file_id}
- Analyze data quality
- Return: column issues, preview data
```

#### `normalization.py`
```python
POST /api/normalize/
- Execute normalization based on rules
- Return: normalized_file_id, statistics

GET /api/normalize/preview/{original_id}/{normalized_id}
- Compare before/after
```

#### `export.py`
```python
POST /api/export/file
- Export to CSV/Excel/JSON

POST /api/export/database
- Save to database table

GET /api/export/download/{filename}
- Download exported file
```

**Design Pattern**: Router Pattern (FastAPI)

---

### 3. **Business Logic Layer** (`app/services/`)

**Tanggung Jawab**:
- Orchestrate business workflows
- Data transformation
- Integration between components

**Komponen**:

#### `upload_handler.py`
**Fungsi**:
- Handle file uploads
- Read various file formats (JSON, CSV, Excel)
- Connect to databases
- In-memory data storage

**Key Methods**:
```python
handle_file_upload(file: UploadFile) -> (file_id, DataFrame, filename)
read_from_database(connection_string, table) -> (file_id, DataFrame)
get_data(file_id) -> DataFrame
store_data(file_id, df)
```

#### `data_analyzer.py`
**Fungsi**:
- Analyze data quality per column
- Detect various issues:
  - Null values
  - Leading/trailing spaces
  - Excessive whitespace
  - Inconsistent capitalization
  - Special characters
  - Invalid emails
  - Invalid SK numbers

**Key Methods**:
```python
analyze_dataframe(df) -> List[ColumnIssue]
analyze_column(df, column) -> ColumnIssue
get_preview_data(df, limit) -> List[Dict]
```

#### `normalization_engine.py`
**Fungsi**:
- Orchestrate normalization process
- Apply normalizers to columns
- Calculate statistics
- Track changes

**Key Methods**:
```python
normalize_dataframe(df, configs) -> (normalized_df, statistics)
get_changes_details(original_df, normalized_df, column) -> List[changes]
```

#### `database_connector.py`
**Fungsi**:
- Database connection management
- Read/write operations
- Connection testing

**Key Methods**:
```python
build_connection_string(config) -> str
test_connection(connection_string) -> bool
read_table(connection_string, table) -> DataFrame
write_table(df, connection_string, table, if_exists) -> int
```

#### `export_service.py`
**Fungsi**:
- Export to various formats
- File download management

**Key Methods**:
```python
export_to_csv(df, filename) -> file_path
export_to_excel(df, filename) -> file_path
export_to_json(df, filename) -> file_path
get_download_url(file_path) -> url
```

**Design Pattern**: Service Layer Pattern

---

### 4. **Domain Logic Layer** (`app/normalizers/`)

**Tanggung Jawab**:
- Define normalization rules
- Execute normalization logic
- Extensible normalization system

**Komponen**:

#### `base.py` - BaseNormalizer (Abstract)
```python
class BaseNormalizer(ABC):
    @abstractmethod
    def normalize(value) -> normalized_value
    
    def normalize_series(series) -> normalized_series
```

#### `text_normalizer.py` - TextNormalizer
**Rules**:
- ✅ Trim leading/trailing spaces
- ✅ Remove excessive whitespace
- ✅ Case conversion (UPPER, lower, Title)
- ✅ Remove special characters (with allowed list)

#### `email_normalizer.py` - EmailNormalizer
**Rules**:
- ✅ Convert to lowercase
- ✅ Trim spaces
- ✅ Validate email format
- ✅ Validate domain (optional)

#### `sk_normalizer.py` - SKNormalizer
**Rules**:
- ✅ Remove irrelevant symbols
- ✅ Standardize format (123/ABC/2024)
- ✅ Normalize delimiter (/, -, _)
- ✅ Validate pattern

**Design Pattern**: Strategy Pattern + Template Method

**Extensibility Example**:
```python
# Adding a new normalizer is easy:

class PhoneNormalizer(BaseNormalizer):
    def normalize(self, value):
        # Remove all non-digits
        digits = re.sub(r'\D', '', str(value))
        
        # Format: +62-XXX-XXXX-XXXX
        if digits.startswith('0'):
            digits = '62' + digits[1:]
        
        return f"+{digits[:2]}-{digits[2:5]}-{digits[5:9]}-{digits[9:]}"
```

---

### 5. **Models Layer** (`app/models/`)

**Tanggung Jawab**:
- Data validation (Pydantic)
- Request/Response schemas
- Type safety

**Komponen**:

#### `schemas.py`
**Schema Categories**:

1. **Connection Schemas**:
   - `DatabaseConnectionSchema`

2. **Upload Schemas**:
   - `UploadResponse`

3. **Analysis Schemas**:
   - `ColumnIssue`
   - `DataAnalysisResponse`

4. **Normalization Schemas**:
   - `TextNormalizationRules`
   - `EmailNormalizationRules`
   - `SKNormalizationRules`
   - `ColumnNormalizationConfig`
   - `NormalizationRequest`
   - `NormalizationResponse`
   - `NormalizationStatistics`

5. **Preview Schemas**:
   - `PreviewComparison`

6. **Export Schemas**:
   - `ExportToFileRequest`
   - `ExportToDatabaseRequest`
   - `ExportResponse`

7. **Error Schemas**:
   - `ErrorResponse`

**Design Pattern**: Data Transfer Object (DTO)

---

### 6. **Utilities Layer** (`app/utils/`)

**Komponen**:

#### `logger.py`
- Centralized logging configuration
- File & console handlers
- Rotating file logs

#### `validators.py`
- Custom validation functions
- Email validation
- SK number validation
- Text quality checks

#### `config.py`
- Environment variable management
- Settings provider
- Directory management

---

## 🔄 Data Flow Diagram

### Upload & Analysis Flow

```
User
  │
  ├─ Upload File
  │    │
  │    ↓
  │  [upload.py] POST /api/upload/file
  │    │
  │    ↓
  │  [upload_handler.py] handle_file_upload()
  │    │
  │    ├─ Validate file
  │    ├─ Save to disk
  │    ├─ Read to DataFrame
  │    └─ Store in memory (file_id)
  │    │
  │    ↓
  │  Return: file_id, metadata
  │
  └─ View Analysis
       │
       ↓
     [analysis.py] GET /api/analysis/{file_id}
       │
       ↓
     [data_analyzer.py] analyze_dataframe()
       │
       ├─ For each column:
       │    ├─ Count nulls
       │    ├─ Check whitespace
       │    ├─ Check case consistency
       │    ├─ Check special chars
       │    ├─ Validate emails (if email column)
       │    └─ Validate SK (if SK column)
       │
       ↓
     Return: ColumnIssue[], preview_data[]
```

### Normalization Flow

```
User configures rules
  │
  ↓
[normalization.py] POST /api/normalize/
  │
  ↓
[normalization_engine.py] normalize_dataframe()
  │
  ├─ For each column config:
  │    │
  │    ├─ If type == 'text':
  │    │    └─ [text_normalizer.py] normalize_series()
  │    │
  │    ├─ If type == 'email':
  │    │    └─ [email_normalizer.py] normalize_series()
  │    │
  │    └─ If type == 'sk':
  │         └─ [sk_normalizer.py] normalize_series()
  │    │
  │    └─ Calculate statistics (rows changed, %)
  │
  ├─ Generate new file_id
  └─ Store normalized DataFrame
  │
  ↓
Return: normalized_file_id, statistics[]
```

### Export Flow

```
User selects export format
  │
  ├─ Export to File
  │    │
  │    ↓
  │  [export.py] POST /api/export/file
  │    │
  │    ↓
  │  [export_service.py]
  │    │
  │    ├─ CSV: export_to_csv()
  │    ├─ Excel: export_to_excel()
  │    └─ JSON: export_to_json()
  │    │
  │    └─ Save to exports/ folder
  │    │
  │    ↓
  │  Return: download_url
  │
  └─ Export to Database
       │
       ↓
     [export.py] POST /api/export/database
       │
       ↓
     [database_connector.py] write_table()
       │
       ├─ Build connection string
       ├─ Create SQLAlchemy engine
       └─ DataFrame.to_sql()
       │
       ↓
     Return: rows_written
```

---

## 🎯 Design Principles

### 1. **Separation of Concerns**
Setiap layer memiliki tanggung jawab yang jelas:
- Routes: HTTP handling
- Services: Business logic
- Normalizers: Domain rules
- Models: Data validation

### 2. **Dependency Injection**
Services tidak hardcode dependencies, mudah untuk testing:
```python
# Good: Injected
def normalize_dataframe(df, normalizer_instance):
    return normalizer_instance.normalize_series(df['column'])

# Bad: Hardcoded
def normalize_dataframe(df):
    normalizer = TextNormalizer()  # Hard to mock in tests
```

### 3. **Single Responsibility Principle**
Setiap class/module punya satu tanggung jawab:
- `TextNormalizer`: Hanya normalisasi teks
- `EmailNormalizer`: Hanya normalisasi email
- `UploadHandler`: Hanya handle upload

### 4. **Open/Closed Principle**
Open for extension, closed for modification:
- Membuat normalizer baru: extend `BaseNormalizer`
- Tidak perlu modify existing code

### 5. **Interface Segregation**
Pydantic schemas sebagai contracts:
- Request schemas: What API expects
- Response schemas: What API returns
- Clear type hints throughout

---

## 🔒 Security Considerations

1. **File Upload**:
   - File type validation
   - File size limits
   - Sanitize filenames

2. **Database**:
   - SQL injection protection (SQLAlchemy)
   - No raw SQL queries

3. **Input Validation**:
   - Pydantic validation on all inputs
   - Type checking

4. **Error Handling**:
   - Don't expose internal errors to users
   - Log detailed errors internally

---

## 📊 Performance Considerations

1. **In-Memory Storage**:
   - Current: Dict-based storage (demo)
   - Production: Redis or Database

2. **Large Files**:
   - Chunk processing for very large files
   - Streaming responses

3. **Database Connections**:
   - Connection pooling (SQLAlchemy)
   - Lazy loading

---

## 🚀 Extensibility Examples

### Adding a New Normalizer

```python
# 1. Create normalizer in app/normalizers/phone_normalizer.py
class PhoneNormalizer(BaseNormalizer):
    def normalize(self, value):
        # Implementation
        pass

# 2. Add schema in app/models/schemas.py
class PhoneNormalizationRules(BaseModel):
    remove_spaces: bool = True
    country_code: str = "+62"

# 3. Add to ColumnNormalizationConfig
class ColumnNormalizationConfig(BaseModel):
    ...
    phone_rules: Optional[PhoneNormalizationRules] = None

# 4. Update normalization_engine.py
if config.column_type == 'phone' and config.phone_rules:
    normalizer = PhoneNormalizer(config.phone_rules.model_dump())
    normalized_df[column_name] = normalizer.normalize_series(...)
```

### Adding a New Export Format

```python
# In app/services/export_service.py
@staticmethod
def export_to_parquet(df: pd.DataFrame, filename: str = None) -> str:
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"export_{timestamp}.parquet"
    
    file_path = os.path.join(settings.EXPORT_DIR, filename)
    df.to_parquet(file_path, engine='pyarrow')
    return file_path
```

---

## 📈 Future Enhancements

1. **Authentication & Multi-User**:
   - JWT tokens
   - User-specific data isolation

2. **Normalization Profiles**:
   - Save/load preset rules
   - Share profiles between users

3. **Batch Processing**:
   - Process multiple files at once
   - Scheduled normalization tasks

4. **Advanced Analytics**:
   - Data quality scoring
   - Trend analysis over time

5. **API-Only Mode**:
   - Headless operation
   - Integration with other systems

---

**Dokumentasi ini memberikan overview lengkap arsitektur aplikasi untuk memudahkan maintenance dan pengembangan future features.**
