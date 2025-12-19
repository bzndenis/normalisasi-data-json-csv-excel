# Aplikasi Normalisasi Data

Aplikasi web-based untuk normalisasi data dari berbagai sumber (JSON, CSV, Excel, Database).

## 🎯 Fitur Utama

- ✅ Upload file JSON, CSV, dan Excel
- ✅ Koneksi ke database MySQL dan PostgreSQL
- ✅ Analisis data otomatis (deteksi masalah)
- ✅ Normalisasi data berbasis aturan yang dapat dikonfigurasi
- ✅ Preview Before vs After
- ✅ Export ke CSV, Excel, JSON
- ✅ Simpan langsung ke database

## 🏗️ Arsitektur

```
normalisasi-data-json-csv-excel/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── routes/                 # API routes
│   │   ├── __init__.py
│   │   ├── upload.py           # Upload file endpoints
│   │   ├── database.py         # Database connection endpoints
│   │   ├── analysis.py         # Data analysis endpoints
│   │   ├── normalization.py    # Normalization endpoints
│   │   └── export.py           # Export endpoints
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── upload_handler.py   # File upload handling
│   │   ├── data_analyzer.py    # Data quality analysis
│   │   ├── normalization_engine.py  # Normalization orchestrator
│   │   ├── database_connector.py    # Database operations
│   │   └── export_service.py   # Export operations
│   ├── normalizers/            # Normalization rules (modular)
│   │   ├── __init__.py
│   │   ├── base.py             # Base normalizer class
│   │   ├── text_normalizer.py  # Text normalization rules
│   │   ├── email_normalizer.py # Email normalization rules
│   │   └── sk_normalizer.py    # SK number normalization rules
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic models
│   │   └── database.py         # SQLAlchemy models
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── logger.py           # Logging configuration
│       └── validators.py       # Custom validators
├── static/                     # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── img/
├── templates/                  # HTML templates (Jinja2)
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   ├── analysis.html
│   ├── normalization.html
│   ├── preview.html
│   └── export.html
├── uploads/                    # Temporary file uploads
├── exports/                    # Exported files
├── data/                       # Example datasets
│   ├── sample.json
│   ├── sample.csv
│   └── sample.xlsx
├── logs/                       # Application logs
├── tests/                      # Unit tests
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Teknologi Stack

- **Backend**: FastAPI
- **Data Processing**: Pandas, NumPy
- **Database**: SQLAlchemy (MySQL, PostgreSQL)
- **Validation**: Pydantic
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Logging**: Python logging

## 📦 Instalasi

### 1. Clone atau ekstrak project

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Konfigurasi environment
```bash
cp .env.example .env
# Edit .env sesuai kebutuhan
```

### 4. Jalankan aplikasi
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Akses aplikasi
Buka browser: `http://localhost:8000`

## 📋 Panduan Penggunaan

### 1. Upload File / Koneksi Database
- Pilih sumber data (File atau Database)
- Upload file JSON/CSV/Excel ATAU isi form koneksi database
- Klik "Analisis Data"

### 2. Review Analisis
- Lihat ringkasan masalah per kolom
- Review preview data asli

### 3. Konfigurasi Normalisasi
- Pilih kolom yang akan dinormalisasi
- Aktifkan/nonaktifkan aturan normalisasi per kolom
- Klik "Normalisasi Data"

### 4. Preview Hasil
- Lihat perbandingan Before vs After
- Review statistik perubahan
- Klik "Undo" jika perlu memperbaiki

### 5. Export / Simpan
- Pilih format export (CSV, Excel, JSON)
- ATAU simpan langsung ke database
- Download hasil

## 🔧 Konfigurasi Normalisasi

### Text Normalization
- Trim spasi
- Konversi case (UPPER, lower, Title)
- Hapus simbol aneh
- Normalisasi whitespace

### Email Normalization
- Lowercase
- Hapus spasi
- Validasi format
- Validasi domain (opsional)

### SK Number Normalization
- Hapus simbol tidak relevan
- Standarisasi format (123/ABC/2024)
- Normalisasi delimiter (/, -, _)
- Validasi regex

## 📝 Logging

Log disimpan di folder `logs/` dengan format:
- `app_YYYY-MM-DD.log`: Application logs
- `normalization_YYYY-MM-DD.log`: Normalization process logs

## 🧪 Testing

```bash
pytest tests/
```

## 📚 API Documentation

Akses Swagger UI: `http://localhost:8000/docs`
Akses ReDoc: `http://localhost:8000/redoc`

## 🔐 Keamanan

- Validasi file upload (type, size)
- SQL injection protection (SQLAlchemy)
- Input sanitization
- Error handling untuk non-technical users

## 🎯 Pengembangan Lanjutan

- [ ] Normalization profiles (preset aturan)
- [ ] Riwayat normalisasi
- [ ] Batch file processing
- [ ] API-only mode (headless)
- [ ] Validasi berbasis kamus eksternal
- [ ] Scheduled normalization tasks
- [ ] Multi-user support dengan authentication

## 📄 Lisensi

MIT License
