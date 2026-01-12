#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk import data pendampingan dari JSON ke database PostgreSQL.

Author: Data Engineering Script
Date: 2025
"""

import json
import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
from psycopg2.pool import SimpleConnectionPool

# ============================================================================
# KONFIGURASI
# ============================================================================

# Konfigurasi Database PostgreSQL
DB_CONFIG = {
    'host': os.getenv('PGHOST', 'localhost'),
    'port': os.getenv('PGPORT', '5432'),
    'dbname': os.getenv('PGDATABASE', 'gokendali_dev'),
    'user': os.getenv('PGUSER', 'postgres'),
    'password': os.getenv('PGPASSWORD', '')
}

# File JSON input
JSON_FILE = 'Data Pendamping_28102025.json'

# Log file
LOG_FILE = 'import_pendampingan.log'

# Mapping field JSON ke field database
JSON_FIELD_MAPPING = {
    'tahun_pendampingan': 'TAHUN PENDAMPINGAN',
    'no_sk_kps': 'NO SK KPS',
    'nama_pendamping': 'NAMA PENDAMPING',
    'email': 'EMAIL',
    'skema_ps': 'SKEMA PS',
    'no': 'NO',
    'keterangan': 'KETERANGAN',  # Field opsional, bisa tidak ada
    'kps': 'KPS',
}

# Konfigurasi resolusi SKEMA PS
# Mapping SKEMA PS ke schema yang perlu dicek
SKEMA_PS_MAPPING = {
    'ha': 'ha',  # Hutan Adat
    'kk': 'kk',  # Kemitraan Kehutanan
    'pphkm': 'pphkm',  # Pengelolaan Hutan Produksi dengan HKM
    'pphd': 'pphd',
    'pphtr': 'pphtr',
    'hn': 'hn',  # Hutan Nagari
    'lphn': 'hn',  # Lembaga Pengelola Hutan Nagari
    'lphd': 'ha',  # Lembaga Pengelola Hutan Desa (mapping ke ha)
    'hutan adat': 'ha',  # Hutan Adat (full text)
}

# Opsi: Jika kps_id tidak ditemukan, apakah tetap insert dengan NULL?
# True = insert dengan kps_id NULL, False = skip dan log
# CATATAN: Untuk schema selain 'ha'/'kk' (pphkm, pphd, pphkr), kps_id akan None 
# dan record tetap akan di-insert dengan kps_id = None (expected behavior)
# Set True agar SEMUA record tetap di-insert ke tabel pendampingan dengan relasi ke user_id
INSERT_WITH_NULL_KPS_ID = True

# Batch size untuk commit
BATCH_SIZE = 100

# ============================================================================
# SETUP LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# ============================================================================
# FUNGSI UTILITAS DATABASE
# ============================================================================

def get_connection():
    """
    Membuat koneksi ke database PostgreSQL.
    
    Returns:
        psycopg2.connection: Koneksi database
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info(f"Berhasil terkoneksi ke database {DB_CONFIG['dbname']}")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Error koneksi database: {e}")
        raise


def load_json(file_path: str) -> List[Dict]:
    """
    Membaca dan memuat data dari file JSON.
    
    Args:
        file_path: Path ke file JSON
        
    Returns:
        List[Dict]: List dari dictionary record JSON
        
    Raises:
        FileNotFoundError: Jika file tidak ditemukan
        json.JSONDecodeError: Jika format JSON tidak valid
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Format JSON harus berupa list of objects")
        
        logger.info(f"Berhasil membaca {len(data)} record dari {file_path}")
        
        # Log contoh 2 record pertama untuk debugging
        if len(data) > 0:
            logger.debug(f"Contoh record 1: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
        if len(data) > 1:
            logger.debug(f"Contoh record 2: {json.dumps(data[1], indent=2, ensure_ascii=False)}")
        
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {e}")
        raise
    except Exception as e:
        logger.error(f"Error membaca file: {e}")
        raise


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def safe_str(value, default=''):
    """
    Convert value to string safely, handling None and non-string types.
    
    Args:
        value: Value to convert (can be None, int, str, etc.)
        default: Default value if None or empty
        
    Returns:
        str: String representation of value, or default if None/empty
    """
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value.strip() if value.strip() else default
    return str(value).strip() if str(value).strip() else default


# ============================================================================
# FUNGSI RESOLUSI ID
# ============================================================================

def resolve_pendamping_id(conn, record: Dict) -> Optional[int]:
    """
    Resolve pendamping_id dari tabel users berdasarkan data JSON.
    
    Prioritas pencarian:
    1. Email (jika ada)
    2. Nama lengkap
    
    Args:
        conn: Koneksi database
        record: Dictionary record JSON
        
    Returns:
        Optional[int]: user_id jika ditemukan tepat satu, None jika tidak
    """
    cur = conn.cursor()
    
    email = safe_str(record.get(JSON_FIELD_MAPPING['email']), '')
    nama = safe_str(record.get(JSON_FIELD_MAPPING['nama_pendamping']), '')
    
    try:
        # Prioritas 1: Cari berdasarkan email (lebih unik)
        if email:
            cur.execute(
                """
                SELECT user_id FROM users 
                WHERE LOWER(TRIM(user_email)) = LOWER(TRIM(%s))
                LIMIT 2
                """,
                (email,)
            )
            results = cur.fetchall()
            
            if len(results) == 1:
                user_id = results[0][0]
                logger.debug(f"Pendamping ditemukan via email '{email}': user_id={user_id}")
                return user_id
            elif len(results) > 1:
                logger.warning(f"Email '{email}' ditemukan lebih dari satu user. Skip record ini.")
                return None
        
        # Prioritas 2: Cari berdasarkan nama (kurang reliable, bisa duplikat)
        if nama:
            cur.execute(
                """
                SELECT user_id FROM users 
                WHERE LOWER(TRIM(user_nama)) = LOWER(TRIM(%s))
                LIMIT 2
                """,
                (nama,)
            )
            results = cur.fetchall()
            
            if len(results) == 1:
                user_id = results[0][0]
                logger.debug(f"Pendamping ditemukan via nama '{nama}': user_id={user_id}")
                return user_id
            elif len(results) > 1:
                logger.warning(f"Nama '{nama}' ditemukan lebih dari satu user. Skip record ini.")
                return None
            elif len(results) == 0:
                logger.warning(f"Pendamping tidak ditemukan untuk nama '{nama}' dan email '{email}'")
                return None
        
        # Jika email dan nama kosong
        if not email and not nama:
            logger.warning("Record tidak memiliki email maupun nama pendamping")
            return None
            
    except psycopg2.Error as e:
        logger.error(f"Error query pendamping: {e}")
        return None
    finally:
        cur.close()
    
    return None


def create_master_kps(conn, record: Dict, no_sk: str, skema_ps: Optional[str] = None) -> Optional[int]:
    """
    Membuat record baru di master_kps jika KPS tidak ditemukan.
    
    CATATAN PENTING: Hanya membuat record untuk schema 'ha' dan 'kk'.
    Schema lain (pphkm, pphd, pphkr, dll) TIDAK akan dimasukkan ke master_kps.
    
    Args:
        conn: Koneksi database
        record: Dictionary record JSON untuk mengambil data tambahan
        no_sk: Nomor SK KPS
        skema_ps: SKEMA PS dari JSON
        
    Returns:
        Optional[int]: kps_id (field 'id' di master_kps) jika berhasil dibuat, None jika gagal atau bukan schema ha/kk
    """
    # Validasi: Hanya buat master_kps untuk schema 'ha' dan 'kk'
    if skema_ps:
        skema_lower = safe_str(skema_ps).lower().strip()
        # Normalisasi schema: semua variasi ha dijadikan 'ha'
        if skema_lower in ['ha', 'hutan adat', 'lphd', 'hn', 'lphn']:
            normalized_schema = 'ha'
        elif skema_lower == 'kk':
            normalized_schema = 'kk'
        else:
            # Schema lain (pphkm, pphd, pphkr, dll) tidak diproses
            logger.info(f"Schema '{skema_ps}' bukan ha/kk, tidak akan dibuat di master_kps. Skip.")
            return None
    else:
        logger.info(f"Schema tidak tersedia, tidak akan dibuat di master_kps. Skip.")
        return None
    
    cur = conn.cursor()
    
    # Initialize variables
    nama_kps = ''
    
    try:
        # Ambil data dari JSON record untuk mengisi master_kps
        nama_kps = safe_str(record.get(JSON_FIELD_MAPPING['kps']))
        provinsi = safe_str(record.get('PROVINSI'))
        kabupaten = safe_str(record.get('KABUPATEN/KOTA'))
        kecamatan = safe_str(record.get('KECAMATAN'))
        desa = safe_str(record.get('DESA/KELURAHAN'))
        luas_sk_ps_raw = record.get('LUAS SK PS')
        luas_sk = None
        if luas_sk_ps_raw:
            try:
                luas_sk = float(luas_sk_ps_raw)
            except (ValueError, TypeError):
                luas_sk = None
        
        # Ambil tahun pendampingan untuk kps_tahun
        tahun_pendampingan_raw = record.get(JSON_FIELD_MAPPING['tahun_pendampingan'])
        kps_tahun = safe_str(tahun_pendampingan_raw) if tahun_pendampingan_raw else None
        
        # Validasi minimal: no_sk dan nama_kps harus ada
        if not no_sk or not nama_kps:
            logger.warning(f"Tidak bisa membuat master_kps: no_sk atau nama_kps kosong. no_sk='{no_sk}', nama_kps='{nama_kps}'")
            return None
        
        # Mapping skema_ps ke schema field
        # Gunakan normalized_schema yang sudah ditentukan di awal fungsi
        schema_value = normalized_schema
        
        # Insert ke master_kps dengan field lengkap
        # Pastikan semua field yang relevan diisi, termasuk untuk schema kk dan ha
        cur.execute(
            """
            INSERT INTO master_kps 
            (no_sk, file_sk, kps_file_sk,
             nama_kps, kps_nama, 
             schema,
             nama_prov, kps_provinsi,
             nama_kab, kps_kab,
             nama_kec,
             nama_desa, kps_desa,
             luas_sk, kps_luas,
             kps_tahun,
             created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id
            """,
            (
                no_sk,  # no_sk
                no_sk,  # file_sk (gunakan no_sk sebagai default)
                no_sk,  # kps_file_sk (gunakan no_sk sebagai default)
                nama_kps,  # nama_kps
                nama_kps,  # kps_nama
                schema_value,  # schema (hanya 'ha' atau 'kk')
                provinsi,  # nama_prov
                provinsi,  # kps_provinsi
                kabupaten,  # nama_kab
                kabupaten,  # kps_kab
                kecamatan,  # nama_kec
                desa,  # nama_desa
                desa,  # kps_desa
                luas_sk,  # luas_sk (numeric)
                str(luas_sk) if luas_sk else None,  # kps_luas (varchar)
                kps_tahun,  # kps_tahun
            )
        )
        
        kps_id = cur.fetchone()[0]
        logger.info(f"KPS baru dibuat di master_kps: id={kps_id}, no_sk='{no_sk}', nama_kps='{nama_kps}'")
        return kps_id
        
    except psycopg2.Error as e:
        logger.error(f"Error create master_kps: {e}")
        logger.error(f"Data: no_sk={no_sk}, nama_kps={nama_kps}, skema_ps={skema_ps}")
        conn.rollback()
        return None
    finally:
        cur.close()
    
    return None


def resolve_kps_id(conn, no_sk: str, skema_ps: Optional[str] = None, record: Optional[Dict] = None) -> Optional[int]:
    """
    Resolve kps_id dari tabel master_kps berdasarkan NO SK KPS.
    
    CATATAN PENTING: Hanya mencari/membuat di master_kps untuk schema 'ha' dan 'kk'.
    Schema lain (pphkm, pphd, pphkr, dll) akan return None dan tidak diproses di master_kps.
    
    Alur pencarian:
    1. Cek apakah schema adalah 'ha' atau 'kk' (jika tidak, return None)
    2. Cari di master_kps berdasarkan no_sk
    3. Jika tidak ketemu dan skema_ps ada, cari dengan filter schema
    4. Jika masih tidak ketemu DAN record tersedia, buat record baru di master_kps (hanya untuk ha/kk)
    5. Jika tidak bisa dibuat atau bukan schema ha/kk, return None
    
    Args:
        conn: Koneksi database
        no_sk: Nomor SK KPS dari JSON
        skema_ps: SKEMA PS dari JSON (opsional)
        record: Dictionary record JSON untuk membuat master_kps baru jika tidak ditemukan (opsional)
        
    Returns:
        Optional[int]: kps_id (field 'id' di master_kps) jika ditemukan atau dibuat, None jika tidak atau bukan schema ha/kk
    """
    no_sk_str = safe_str(no_sk)
    if not no_sk_str:
        return None
    
    # Validasi: Hanya proses untuk schema 'ha' dan 'kk'
    schema_normalized = None
    is_valid_schema = False
    if skema_ps:
        skema_lower = safe_str(skema_ps).lower().strip()
        # Normalisasi schema
        if skema_lower == 'hutan adat' or skema_lower == 'lphd':
            schema_normalized = 'ha'
            is_valid_schema = True
        elif skema_lower in ['hn', 'lphn']:
            schema_normalized = 'ha'  # hn dan lphn dianggap sebagai ha
            is_valid_schema = True
        elif skema_lower == 'ha':
            schema_normalized = 'ha'
            is_valid_schema = True
        elif skema_lower == 'kk':
            schema_normalized = 'kk'
            is_valid_schema = True
        else:
            # Schema lain (pphkm, pphd, pphkr, dll) tidak diproses di master_kps
            logger.debug(f"Schema '{skema_ps}' bukan ha/kk, tidak akan dicari/dibuat di master_kps. Return None.")
            return None
    
    # Jika tidak ada schema, tidak bisa proses (butuh schema untuk menentukan apakah ha/kk)
    if not skema_ps:
        logger.debug(f"Schema tidak tersedia, tidak akan dicari/dibuat di master_kps. Return None.")
        return None
    
    cur = conn.cursor()
    no_sk_clean = no_sk_str
    
    try:
        
        # Langkah 1: Cari di master_kps berdasarkan no_sk (prioritas: dengan schema jika ada)
        if schema_normalized:
            # Cari dengan filter schema terlebih dahulu (lebih spesifik)
            cur.execute(
                """
                SELECT id FROM master_kps 
                WHERE TRIM(no_sk) = TRIM(%s)
                  AND LOWER(TRIM(COALESCE(schema, ''))) = %s
                LIMIT 2
                """,
                (no_sk_clean, schema_normalized)
            )
            results = cur.fetchall()
            
            if len(results) == 1:
                kps_id = results[0][0]
                logger.debug(f"KPS ditemukan via no_sk + schema '{no_sk_clean}' + '{schema_normalized}': kps_id={kps_id}")
                return kps_id
            elif len(results) > 1:
                logger.warning(f"No SK '{no_sk_clean}' dengan schema '{schema_normalized}' ditemukan lebih dari satu. Menggunakan yang pertama.")
                return results[0][0]
        
        # Langkah 2: Cari tanpa filter schema (fallback)
        cur.execute(
            """
            SELECT id FROM master_kps 
            WHERE TRIM(no_sk) = TRIM(%s)
            LIMIT 2
            """,
            (no_sk_clean,)
        )
        results = cur.fetchall()
        
        if len(results) == 1:
            kps_id = results[0][0]
            logger.debug(f"KPS ditemukan via no_sk '{no_sk_clean}' (tanpa filter schema): kps_id={kps_id}")
            return kps_id
        elif len(results) > 1:
            logger.warning(f"No SK '{no_sk_clean}' ditemukan lebih dari satu di master_kps. Menggunakan yang pertama.")
            return results[0][0]
        
        # Langkah 3: Fuzzy match dengan schema (jika masih belum ketemu)
        # Coba cari dengan ILIKE untuk no_sk yang mungkin sedikit berbeda formatnya
        if schema_normalized:
            cur.execute(
                """
                SELECT id FROM master_kps 
                WHERE LOWER(TRIM(COALESCE(schema, ''))) = %s
                  AND (TRIM(no_sk) ILIKE %s OR TRIM(no_sk) = %s)
                LIMIT 2
                """,
                (schema_normalized, f'%{no_sk_clean}%', no_sk_clean)
            )
            results = cur.fetchall()
            
            if len(results) == 1:
                kps_id = results[0][0]
                logger.debug(f"KPS ditemukan via schema fuzzy match '{schema_normalized}': kps_id={kps_id}")
                return kps_id
        
        # Langkah 4: Tidak ditemukan - buat record baru jika record JSON tersedia dan schema adalah ha/kk
        logger.warning(f"KPS tidak ditemukan untuk no_sk '{no_sk_clean}' dan skema_ps '{skema_ps}'")
        
        # Hanya buat master_kps baru jika schema adalah ha atau kk
        if record is not None and is_valid_schema:
            logger.info(f"Mencoba membuat KPS baru di master_kps untuk no_sk '{no_sk_clean}' dengan schema '{schema_normalized}'...")
            new_kps_id = create_master_kps(conn, record, no_sk_clean, skema_ps)
            if new_kps_id:
                logger.info(f"KPS baru berhasil dibuat: kps_id={new_kps_id}")
                return new_kps_id
            else:
                logger.error(f"Gagal membuat KPS baru untuk no_sk '{no_sk_clean}'")
                return None
        elif record is None:
            logger.warning(f"Record JSON tidak tersedia, tidak bisa membuat KPS baru untuk no_sk '{no_sk_clean}'")
            return None
        else:
            logger.info(f"Schema '{skema_ps}' bukan ha/kk, tidak akan membuat KPS di master_kps. Return None.")
            return None
        
    except psycopg2.Error as e:
        logger.error(f"Error query KPS: {e}")
        return None
    finally:
        cur.close()
    
    return None


# ============================================================================
# FUNGSI INSERT & PROCESSING
# ============================================================================

def insert_pendampingan(conn, row_data: Dict) -> bool:
    """
    Insert satu baris ke tabel pendampingan.
    
    Args:
        conn: Koneksi database
        row_data: Dictionary dengan keys:
            - pendamping_id: int (bisa None)
            - tahun_pendampingan: str
            - kps_id: int (bisa None)
            - keterangan: str
            - waktu_upload: datetime
            
    Returns:
        bool: True jika berhasil, False jika gagal
    """
    cur = conn.cursor()
    
    try:
        cur.execute(
            """
            INSERT INTO pendampingan 
            (pendamping_id, tahun_pendampingan, kps_id, keterangan, waktu_upload)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_pendampingan
            """,
            (
                row_data['pendamping_id'],
                str(row_data['tahun_pendampingan']),
                row_data['kps_id'],
                row_data['keterangan'],
                row_data['waktu_upload']
            )
        )
        id_pendampingan = cur.fetchone()[0]
        logger.debug(f"Inserted pendampingan id={id_pendampingan}, pendamping_id={row_data['pendamping_id']}, kps_id={row_data['kps_id']}")
        return True
        
    except psycopg2.Error as e:
        logger.error(f"Error insert pendampingan: {e}")
        logger.error(f"Data: {row_data}")
        conn.rollback()
        return False
    finally:
        cur.close()


def process_record(
    conn, 
    record: Dict, 
    last_pendamping_id: Optional[int] = None,
    last_tahun: Optional[str] = None
) -> Tuple[bool, Optional[int], Optional[str], str]:
    """
    Process satu record JSON dan insert ke database.
    
    Args:
        conn: Koneksi database
        record: Dictionary record JSON
        last_pendamping_id: user_id dari record sebelumnya (untuk kasus NO kosong)
        last_tahun: tahun dari record sebelumnya (untuk kasus NO kosong)
        
    Returns:
        Tuple[bool, Optional[int], Optional[str], str]:
            - success: bool
            - pendamping_id: int atau None
            - tahun: str atau None
            - error_message: str
    """
    # Validasi record
    if record is None or not isinstance(record, dict):
        return (False, None, None, "Record tidak valid (None atau bukan dictionary)")
    
    # Cek apakah NO kosong/null (indikator multi-KPS)
    no_value = record.get(JSON_FIELD_MAPPING['no'])
    no_value_str = safe_str(no_value)
    is_no_empty = (no_value is None or no_value_str == '')
    
    # Resolve pendamping_id
    if is_no_empty and last_pendamping_id is not None:
        # Gunakan pendamping_id dari record sebelumnya (multi-KPS)
        pendamping_id = last_pendamping_id
        nama_kps = safe_str(record.get(JSON_FIELD_MAPPING['kps']))
        logger.info(f"[MULTI-KPS] Record dengan NO kosong: menggunakan pendamping_id={pendamping_id} dari record sebelumnya, KPS='{nama_kps}'")
    else:
        # Resolve pendamping baru (record dengan NO terisi atau record pertama)
        nama_pendamping = safe_str(record.get(JSON_FIELD_MAPPING['nama_pendamping']))
        email_pendamping = safe_str(record.get(JSON_FIELD_MAPPING['email']))
        pendamping_id = resolve_pendamping_id(conn, record)
        if pendamping_id is None:
            # Jika tidak ditemukan, tidak bisa lanjut
            logger.warning(f"Record: Pendamping tidak ditemukan. NO={no_value}, nama='{nama_pendamping}', email='{email_pendamping}'")
            return (False, None, None, "Pendamping tidak ditemukan")
        logger.info(f"[PENDAMPING BARU] Record dengan NO={no_value}: pendamping_id={pendamping_id}, nama='{nama_pendamping}'")
    
    # Ambil tahun pendampingan
    tahun_raw = record.get(JSON_FIELD_MAPPING['tahun_pendampingan'])
    
    # Jika NO kosong dan ada last_tahun, gunakan tahun sebelumnya
    if is_no_empty and last_tahun:
        tahun = last_tahun
        logger.debug(f"Field NO kosong, menggunakan tahun sebelumnya: {tahun}")
    elif tahun_raw is None:
        # Jika tidak ada tahun dan bukan multi-KPS, error
        if not is_no_empty:
            return (False, pendamping_id, None, "Tahun pendampingan tidak ditemukan")
        # Jika NO kosong tapi tidak ada last_tahun, gunakan None (akan error di bawah)
        tahun = None
    else:
        tahun = safe_str(tahun_raw)
    
    # Final check: tahun harus ada
    if not tahun:
        return (False, pendamping_id, None, "Tahun pendampingan tidak ditemukan")
    
    # Resolve kps_id
    no_sk_kps = safe_str(record.get(JSON_FIELD_MAPPING['no_sk_kps']))
    skema_ps_raw = record.get(JSON_FIELD_MAPPING['skema_ps'])
    skema_ps = safe_str(skema_ps_raw) if skema_ps_raw else None
    
    # Pass record untuk membuat master_kps baru jika tidak ditemukan
    # CATATAN: resolve_kps_id hanya akan mencari/membuat di master_kps untuk schema 'ha' dan 'kk'
    # Schema lain (pphkm, pphd, pphkr, dll) akan return None (expected behavior)
    kps_id = resolve_kps_id(conn, no_sk_kps, skema_ps if skema_ps else None, record)
    
    # Cek apakah schema adalah ha/kk atau bukan
    is_ha_kk_schema = False
    if skema_ps:
        skema_lower = safe_str(skema_ps).lower().strip()
        if skema_lower in ['ha', 'kk', 'hutan adat', 'lphd', 'hn', 'lphn']:
            is_ha_kk_schema = True
    
    if kps_id is None:
        if is_ha_kk_schema:
            # Untuk schema ha/kk, jika kps_id None berarti tidak ditemukan/dibuat (error)
            error_msg = f"KPS tidak ditemukan dan gagal dibuat untuk no_sk='{no_sk_kps}', skema_ps='{skema_ps}'"
            logger.warning(error_msg)
            
            # Log ke tabel log_missing_kps (jika diperlukan)
            log_missing_kps(conn, record, no_sk_kps, skema_ps)
            
            if not INSERT_WITH_NULL_KPS_ID:
                return (False, pendamping_id, tahun, error_msg)
            # Jika INSERT_WITH_NULL_KPS_ID = True, lanjutkan dengan kps_id = None
        else:
            # Untuk schema selain ha/kk (pphkm, pphd, pphkr, dll), kps_id = None adalah expected
            # Karena kita tidak memasukkan schema tersebut ke master_kps
            logger.info(f"Schema '{skema_ps}' bukan ha/kk, kps_id akan None (tidak dimasukkan ke master_kps). Tetap insert ke pendampingan.")
            # Lanjutkan insert dengan kps_id = None
    
    # Ambil keterangan
    keterangan = safe_str(record.get(JSON_FIELD_MAPPING['keterangan']))
    if not keterangan:
        keterangan = f"Import dari {JSON_FILE}"
    
    # Waktu upload
    waktu_upload = datetime.utcnow()
    
    # Siapkan data untuk insert
    row_data = {
        'pendamping_id': pendamping_id,
        'tahun_pendampingan': tahun,
        'kps_id': kps_id,
        'keterangan': keterangan[:255],  # Batasi panjang sesuai constraint
        'waktu_upload': waktu_upload
    }
    
    # Insert
    success = insert_pendampingan(conn, row_data)
    
    if success:
        logger.debug(f"Record berhasil di-insert: pendamping_id={pendamping_id}, kps_id={kps_id}, tahun={tahun}")
        return (True, pendamping_id, tahun, "")
    else:
        logger.warning(f"Record GAGAL di-insert: pendamping_id={pendamping_id}, kps_id={kps_id}, tahun={tahun}")
        return (False, pendamping_id, tahun, "Error insert ke database")


def log_missing_kps(conn, record: Dict, no_sk: str, skema_ps: str):
    """
    Log record yang KPS-nya tidak ditemukan ke file log.
    Bisa juga di-extend untuk insert ke tabel log jika diperlukan.
    
    Args:
        conn: Koneksi database (untuk future: insert ke tabel log)
        record: Dictionary record JSON
        no_sk: Nomor SK yang tidak ditemukan
        skema_ps: SKEMA PS
    """
    log_data = {
        'no_sk': no_sk,
        'skema_ps': skema_ps,
        'nama_pendamping': record.get(JSON_FIELD_MAPPING['nama_pendamping'], ''),
        'email': record.get(JSON_FIELD_MAPPING['email'], ''),
        'kps': record.get(JSON_FIELD_MAPPING['kps'], ''),
        'timestamp': datetime.utcnow().isoformat()
    }
    
    logger.warning(f"MISSING KPS: {json.dumps(log_data, ensure_ascii=False)}")
    
    # Future: Bisa insert ke tabel log_missing_kps jika diperlukan
    # try:
    #     cur = conn.cursor()
    #     cur.execute(
    #         "INSERT INTO log_missing_kps (no_sk, skema_ps, ...) VALUES (...)",
    #         (...)
    #     )
    #     conn.commit()
    # except:
    #     pass


# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    """Entry point utama script."""
    # Tulis juga ke stdout dengan flush untuk memastikan output terlihat
    print("=" * 80, flush=True)
    print("MEMULAI IMPORT DATA PENDAMPINGAN", flush=True)
    print("=" * 80, flush=True)
    
    logger.info("=" * 80)
    logger.info("MEMULAI IMPORT DATA PENDAMPINGAN")
    logger.info("=" * 80)
    
    # Statistik
    stats = {
        'total_records': 0,
        'success': 0,
        'failed': 0,
        'failed_pendamping': 0,
        'failed_kps': 0,
        'failed_other': 0
    }
    
    conn = None
    
    try:
        # Baca JSON
        logger.info(f"Membaca file JSON: {JSON_FILE}")
        records = load_json(JSON_FILE)
        stats['total_records'] = len(records)
        
        # Koneksi database
        logger.info("Membuka koneksi database...")
        conn = get_connection()
        
        # Variabel untuk tracking record sebelumnya (untuk kasus NO kosong)
        last_pendamping_id = None
        last_tahun = None
        
        # Process setiap record
        logger.info(f"Memproses {len(records)} record...")
        
        for idx, record in enumerate(records, 1):
            if idx % 100 == 0:
                logger.info(f"Progress: {idx}/{len(records)} ({idx*100//len(records)}%)")
            
            # Skip jika record None atau bukan dictionary
            if record is None:
                logger.warning(f"Record {idx} adalah None, skip...")
                stats['failed'] += 1
                stats['failed_other'] += 1
                continue
            
            if not isinstance(record, dict):
                logger.warning(f"Record {idx} bukan dictionary (tipe: {type(record)}), skip...")
                stats['failed'] += 1
                stats['failed_other'] += 1
                continue
            
            # Process record
            success, pendamping_id, tahun, error_msg = process_record(
                conn, 
                record,
                last_pendamping_id,
                last_tahun
            )
            
            if success:
                stats['success'] += 1
                
                # Commit per batch
                if stats['success'] % BATCH_SIZE == 0:
                    conn.commit()
                    logger.debug(f"Committed batch: {stats['success']} records")
            else:
                stats['failed'] += 1
                
                # Kategorikan error
                if "Pendamping tidak ditemukan" in error_msg:
                    stats['failed_pendamping'] += 1
                elif "KPS tidak ditemukan" in error_msg:
                    stats['failed_kps'] += 1
                else:
                    stats['failed_other'] += 1
                
                logger.debug(f"Record {idx} gagal: {error_msg}")
            
            # Update tracking untuk record berikutnya
            # Logika tracking yang BENAR:
            # 1. Tracking hanya di-update jika record dengan NO TERISI berhasil di-insert
            #    - Record dengan NO terisi = pendamping baru → update tracking SEBELUM record berikutnya diproses
            # 2. Record dengan NO kosong = multi-KPS (masih pendamping yang sama)
            #    - Tracking TIDAK di-update → tetap menggunakan pendamping dari record sebelumnya
            # 3. Ini memastikan semua record NO kosong berikutnya tetap menggunakan pendamping yang sama
            #    sampai muncul record baru dengan NO terisi
            no_value = record.get(JSON_FIELD_MAPPING['no'])
            no_value_str = safe_str(no_value)
            no_value_is_filled = (no_value is not None and no_value_str != '')
            nama_kps = safe_str(record.get(JSON_FIELD_MAPPING['kps']))
            
            if success and pendamping_id is not None:
                # Update tracking HANYA untuk record dengan NO terisi (pendamping baru)
                if no_value_is_filled:
                    # Record dengan NO terisi = pendamping baru, update tracking
                    old_pendamping_id = last_pendamping_id
                    last_pendamping_id = pendamping_id
                    if tahun:
                        last_tahun = tahun
                    logger.info(f"[TRACKING UPDATE] Record {idx}: NO={no_value} terisi → tracking di-update: pendamping_id={pendamping_id} (sebelumnya={old_pendamping_id}), tahun={tahun}, KPS='{nama_kps}'")
                else:
                    # Record dengan NO kosong = multi-KPS, tracking TIDAK di-update
                    # Tracking tetap menggunakan pendamping yang sama dari record sebelumnya
                    # Jadi record NO kosong berikutnya masih menggunakan pendamping yang benar
                    logger.debug(f"[TRACKING NO UPDATE] Record {idx}: NO kosong (multi-KPS) → tracking TIDAK di-update, tetap menggunakan pendamping_id={last_pendamping_id}, tahun={last_tahun}, KPS='{nama_kps}'")
            elif not success:
                # Record gagal, logging untuk debugging
                logger.debug(f"[TRACKING NO UPDATE] Record {idx}: GAGAL di-insert → tracking TIDAK di-update, tetap menggunakan pendamping_id={last_pendamping_id}")
            elif pendamping_id is None:
                # Record berhasil tapi pendamping_id None (seharusnya tidak terjadi)
                logger.warning(f"[TRACKING NO UPDATE] Record {idx}: Berhasil tapi pendamping_id=None → tracking TIDAK di-update")
        
        # Final commit
        conn.commit()
        logger.info("Final commit selesai")
        
    except FileNotFoundError as e:
        logger.error(f"File tidak ditemukan: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {e}")
        sys.exit(1)
    except psycopg2.Error as e:
        logger.error(f"Error database: {e}")
        if conn:
            conn.rollback()
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error tidak terduga: {e}", exc_info=True)
        if conn:
            conn.rollback()
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            logger.info("Koneksi database ditutup")
    
    # Tampilkan ringkasan
    logger.info("=" * 80)
    logger.info("RINGKASAN HASIL IMPORT")
    logger.info("=" * 80)
    logger.info(f"Total record di JSON: {stats['total_records']}")
    logger.info(f"Berhasil di-insert: {stats['success']}")
    logger.info(f"Gagal: {stats['failed']}")
    logger.info(f"  - Gagal karena pendamping tidak ditemukan: {stats['failed_pendamping']}")
    logger.info(f"  - Gagal karena KPS tidak ditemukan: {stats['failed_kps']}")
    logger.info(f"  - Gagal karena error lain: {stats['failed_other']}")
    logger.info("=" * 80)
    
    if stats['success'] > 0:
        logger.info("✅ Import berhasil!")
    else:
        logger.warning("⚠️  Tidak ada record yang berhasil di-insert")
        sys.exit(1)


if __name__ == "__main__":
    main()
