# Panduan Instalasi & Menjalankan Aplikasi

## 📋 Prerequisites

Pastikan Anda sudah menginstall:
- Python 3.9 atau lebih tinggi
- pip (Python package manager)

## 🚀 Langkah Instalasi

### 1. Buka Terminal/Command Prompt di Folder Project

Buka Command Prompt atau PowerShell, lalu navigate ke folder project:

```bash
cd c:\laragon\www\normalisasi-data-json-csv-excel
```

### 2. Install Dependencies

Jalankan perintah berikut untuk menginstall semua library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

**Catatan**: Proses instalasi mungkin memakan waktu beberapa menit tergantung koneksi internet Anda.

### 3. Verifikasi Instalasi

Pastikan semua dependencies terinstall dengan baik:

```bash
python -c "import fastapi, pandas, sqlalchemy; print('✓ All dependencies installed successfully!')"
```

## ▶️ Menjalankan Aplikasi

### Cara 1: Menggunakan Uvicorn langsung

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Cara 2: Menggunakan Python main

```bash
python -m app.main
```

### Cara 3: Development mode dengan auto-reload

```bash
uvicorn app.main:app --reload
```

## 🌐 Mengakses Aplikasi

Setelah aplikasi berjalan, Anda akan melihat output seperti ini:

```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Starting Data Normalization App v1.0.0
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Buka browser dan akses:

- **Homepage**: http://localhost:8000
- **Upload Page**: http://localhost:8000/upload
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc

## 📊 Testing dengan Sample Data

1. Buka http://localhost:8000/upload
2. Upload file dari folder `data/`:
   - `sample.json`
   - `sample.csv`
3. Ikuti workflow:
   - Upload → Analisis → Normalisasi → Preview → Export

## 🔧 Troubleshooting

### Error: "No module named 'fastapi'"

**Solusi**: Install dependencies lagi
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"

**Solusi**: Port 8000 sudah digunakan program lain. Gunakan port berbeda:
```bash
uvicorn app.main:app --reload --port 8001
```

### Error: Database connection failed

**Solusi**: Pastikan MySQL/PostgreSQL sudah berjalan dan kredensial di `.env` benar

### File upload error

**Solusi**: Pastikan folder `uploads` dan `exports` sudah ada (akan dibuat otomatis saat aplikasi start)

## 🛑 Menghentikan Aplikasi

Tekan `CTRL + C` di terminal untuk menghentikan server

## 📖 Dokumentasi API

Setelah aplikasi berjalan, akses Swagger UI di:
http://localhost:8000/docs

Di sana Anda bisa:
- Melihat semua endpoint API
- Testing API langsung dari browser
- Melihat request/response schema

## 💡 Tips Development

1. **Auto-reload**: Gunakan flag `--reload` agar aplikasi restart otomatis saat ada perubahan code
2. **Logging**: Cek folder `logs/` untuk melihat application logs
3. **Sample Data**: Gunakan file di folder `data/` untuk testing
4. **Environment Variables**: Edit `.env` untuk konfigurasi custom

## 🎯 Next Steps

Setelah aplikasi berjalan:

1. ✅ Upload sample data
2. ✅ Coba fitur analisis data
3. ✅ Konfigurasi normalisasi rules
4. ✅ Export hasil normalisasi
5. ✅ Coba koneksi database (jika ada MySQL/PostgreSQL)

## 📞 Butuh Bantuan?

- Cek log di folder `logs/` untuk error details
- Review dokumentasi di `README.md`
- Check API docs di http://localhost:8000/docs

---

**Selamat menggunakan Data Normalization App! 🚀**
