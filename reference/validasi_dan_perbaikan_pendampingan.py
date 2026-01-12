#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk validasi dan perbaikan data pendampingan agar sesuai dengan JSON.

Script ini akan:
1. Membaca data dari JSON file
2. Membaca data dari tabel pendampingan di database
3. Membandingkan dan mengidentifikasi ketidaksesuaian
4. Memperbaiki data yang tidak sesuai dengan JSON

Author: Data Engineering Script
Date: 2025
"""

import json
import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor

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
LOG_FILE = 'validasi_pendampingan.log'

# Mapping field JSON ke field database
JSON_FIELD_MAPPING = {
    'tahun_pendampingan': 'TAHUN PENDAMPINGAN',
    'no_sk_kps': 'NO SK KPS',
    'nama_pendamping': 'NAMA PENDAMPING',
    'email': 'EMAIL',
    'skema_ps': 'SKEMA PS',
    'no': 'NO',
    'keterangan': 'KETERANGAN',
    'kps': 'KPS',
}

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
# FUNGSI UTILITAS
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
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File tidak ditemukan: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError("Format JSON harus berupa list of objects")
        
        logger.info(f"Berhasil membaca {len(data)} record dari {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {e}")
        raise
    except Exception as e:
        logger.error(f"Error membaca file: {e}")
        raise


def safe_str(value, default=''):
    """
    Convert value to string safely, handling None and non-string types.
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
    """
    cur = conn.cursor()
    
    email = safe_str(record.get(JSON_FIELD_MAPPING['email']), '')
    nama = safe_str(record.get(JSON_FIELD_MAPPING['nama_pendamping']), '')
    
    try:
        # Prioritas 1: Cari berdasarkan email
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
                return results[0][0]
            elif len(results) > 1:
                logger.warning(f"Email '{email}' ditemukan lebih dari satu user")
                return None
        
        # Prioritas 2: Cari berdasarkan nama
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
                return results[0][0]
            elif len(results) > 1:
                logger.warning(f"Nama '{nama}' ditemukan lebih dari satu user")
                return None
        
        return None
            
    except psycopg2.Error as e:
        logger.error(f"Error query pendamping: {e}")
        return None
    finally:
        cur.close()


def resolve_kps_id(conn, no_sk: str, skema_ps: Optional[str] = None) -> Optional[int]:
    """
    Resolve kps_id dari tabel master_kps berdasarkan NO SK KPS.
    
    Hanya mencari untuk schema 'ha' dan 'kk'.
    Schema lain akan return None.
    """
    no_sk_str = safe_str(no_sk)
    if not no_sk_str:
        return None
    
    # Validasi: Hanya proses untuk schema 'ha' dan 'kk'
    schema_normalized = None
    if skema_ps:
        skema_lower = safe_str(skema_ps).lower().strip()
        if skema_lower in ['ha', 'hutan adat', 'lphd', 'hn', 'lphn']:
            schema_normalized = 'ha'
        elif skema_lower == 'kk':
            schema_normalized = 'kk'
        else:
            # Schema lain tidak diproses di master_kps
            return None
    
    if not schema_normalized:
        return None
    
    cur = conn.cursor()
    
    try:
        # Cari dengan filter schema
        cur.execute(
            """
            SELECT id FROM master_kps 
            WHERE TRIM(no_sk) = TRIM(%s)
              AND LOWER(TRIM(COALESCE(schema, ''))) = %s
            LIMIT 2
            """,
            (no_sk_str, schema_normalized)
        )
        results = cur.fetchall()
        
        if len(results) == 1:
            return results[0][0]
        elif len(results) > 1:
            logger.warning(f"No SK '{no_sk_str}' dengan schema '{schema_normalized}' ditemukan lebih dari satu")
            return results[0][0]
        
        # Cari tanpa filter schema (fallback)
        cur.execute(
            """
            SELECT id FROM master_kps 
            WHERE TRIM(no_sk) = TRIM(%s)
            LIMIT 2
            """,
            (no_sk_str,)
        )
        results = cur.fetchall()
        
        if len(results) == 1:
            return results[0][0]
        elif len(results) > 1:
            return results[0][0]
        
        return None
        
    except psycopg2.Error as e:
        logger.error(f"Error query KPS: {e}")
        return None
    finally:
        cur.close()


# ============================================================================
# FUNGSI VALIDASI
# ============================================================================

def build_json_key(record: Dict, conn) -> Optional[Tuple]:
    """
    Membangun key unik untuk record JSON.
    Key: (pendamping_id, tahun_pendampingan, kps_id)
    """
    pendamping_id = resolve_pendamping_id(conn, record)
    if pendamping_id is None:
        return None
    
    tahun_raw = record.get(JSON_FIELD_MAPPING['tahun_pendampingan'])
    tahun = safe_str(tahun_raw) if tahun_raw else None
    if not tahun:
        return None
    
    no_sk_kps = safe_str(record.get(JSON_FIELD_MAPPING['no_sk_kps']))
    skema_ps_raw = record.get(JSON_FIELD_MAPPING['skema_ps'])
    skema_ps = safe_str(skema_ps_raw) if skema_ps_raw else None
    kps_id = resolve_kps_id(conn, no_sk_kps, skema_ps)
    
    return (pendamping_id, tahun, kps_id)


def load_db_pendampingan(conn) -> Dict[Tuple, Dict]:
    """
    Memuat semua data dari tabel pendampingan.
    
    Returns:
        Dict dengan key (pendamping_id, tahun_pendampingan, kps_id) dan value dict record
    """
    cur = conn.cursor(cursor_factory=DictCursor)
    
    try:
        cur.execute("""
            SELECT 
                id_pendampingan,
                pendamping_id,
                tahun_pendampingan,
                kps_id,
                keterangan,
                waktu_upload
            FROM pendampingan
        """)
        
        records = cur.fetchall()
        result = {}
        
        for record in records:
            key = (
                record['pendamping_id'],
                safe_str(record['tahun_pendampingan']),
                record['kps_id']
            )
            result[key] = dict(record)
        
        logger.info(f"Berhasil memuat {len(result)} record dari tabel pendampingan")
        return result
        
    except psycopg2.Error as e:
        logger.error(f"Error query pendampingan: {e}")
        raise
    finally:
        cur.close()


def validate_data(conn, json_records: List[Dict]) -> Dict:
    """
    Validasi data JSON dengan data di database.
    
    Returns:
        Dict dengan hasil validasi:
        - missing_in_db: List record JSON yang tidak ada di DB
        - missing_in_json: List record DB yang tidak ada di JSON
        - different_data: List record yang berbeda
        - stats: Statistik validasi
    """
    logger.info("Memulai validasi data...")
    
    # Load data dari database
    db_records = load_db_pendampingan(conn)
    
    # Build index JSON records
    json_index = {}
    json_records_by_key = {}
    missing_pendamping = []
    
    last_pendamping_id = None
    last_tahun = None
    
    for idx, record in enumerate(json_records, 1):
        if idx % 500 == 0:
            logger.info(f"Processing JSON record {idx}/{len(json_records)}...")
        
        # Handle multi-KPS (NO kosong)
        no_value = record.get(JSON_FIELD_MAPPING['no'])
        no_value_str = safe_str(no_value)
        is_no_empty = (no_value is None or no_value_str == '')
        
        if is_no_empty and last_pendamping_id is not None:
            pendamping_id = last_pendamping_id
            tahun = last_tahun
        else:
            pendamping_id = resolve_pendamping_id(conn, record)
            if pendamping_id is None:
                missing_pendamping.append({
                    'index': idx,
                    'record': record,
                    'reason': 'Pendamping tidak ditemukan'
                })
                continue
            
            tahun_raw = record.get(JSON_FIELD_MAPPING['tahun_pendampingan'])
            tahun = safe_str(tahun_raw) if tahun_raw else None
            if not tahun:
                missing_pendamping.append({
                    'index': idx,
                    'record': record,
                    'reason': 'Tahun pendampingan tidak ada'
                })
                continue
        
        # Resolve kps_id
        no_sk_kps = safe_str(record.get(JSON_FIELD_MAPPING['no_sk_kps']))
        skema_ps_raw = record.get(JSON_FIELD_MAPPING['skema_ps'])
        skema_ps = safe_str(skema_ps_raw) if skema_ps_raw else None
        kps_id = resolve_kps_id(conn, no_sk_kps, skema_ps)
        
        key = (pendamping_id, tahun, kps_id)
        
        # Simpan record JSON
        json_index[key] = {
            'index': idx,
            'record': record,
            'pendamping_id': pendamping_id,
            'tahun': tahun,
            'kps_id': kps_id
        }
        json_records_by_key[key] = record
        
        # Update tracking untuk record berikutnya
        if not is_no_empty:
            last_pendamping_id = pendamping_id
            last_tahun = tahun
    
    logger.info(f"Berhasil memproses {len(json_index)} record JSON (valid)")
    if missing_pendamping:
        logger.warning(f"Terdapat {len(missing_pendamping)} record JSON yang tidak bisa diproses (pendamping tidak ditemukan)")
    
    # Identifikasi perbedaan
    missing_in_db = []
    missing_in_json = []
    different_data = []
    
    # Record yang ada di JSON tapi tidak ada di DB
    for key, json_data in json_index.items():
        if key not in db_records:
            missing_in_db.append(json_data)
    
    # Record yang ada di DB tapi tidak ada di JSON
    for key, db_record in db_records.items():
        if key not in json_index:
            missing_in_json.append({
                'key': key,
                'db_record': db_record
            })
    
    # Record yang ada di kedua tapi mungkin berbeda (untuk future: bisa cek field lain)
    for key in json_index.keys() & db_records.keys():
        # Untuk saat ini, jika key sama berarti data sama
        # Bisa ditambahkan validasi field lain jika diperlukan
        pass
    
    stats = {
        'total_json_records': len(json_records),
        'valid_json_records': len(json_index),
        'missing_pendamping': len(missing_pendamping),
        'total_db_records': len(db_records),
        'missing_in_db': len(missing_in_db),
        'missing_in_json': len(missing_in_json),
        'matching_records': len(json_index.keys() & db_records.keys())
    }
    
    return {
        'missing_in_db': missing_in_db,
        'missing_in_json': missing_in_json,
        'different_data': different_data,
        'missing_pendamping': missing_pendamping,
        'stats': stats
    }


# ============================================================================
# FUNGSI PERBAIKAN
# ============================================================================

def insert_missing_records(conn, missing_records: List[Dict], dry_run: bool = False) -> int:
    """
    Insert record yang missing di database.
    
    Args:
        conn: Koneksi database
        missing_records: List record yang perlu di-insert
        dry_run: Jika True, hanya log tanpa insert
        
    Returns:
        int: Jumlah record yang berhasil di-insert
    """
    if not missing_records:
        logger.info("Tidak ada record yang perlu di-insert")
        return 0
    
    logger.info(f"Memulai insert {len(missing_records)} record yang missing...")
    
    cur = conn.cursor()
    success_count = 0
    
    try:
        for idx, json_data in enumerate(missing_records, 1):
            if idx % 100 == 0:
                logger.info(f"Progress insert: {idx}/{len(missing_records)}")
            
            record = json_data['record']
            pendamping_id = json_data['pendamping_id']
            tahun = json_data['tahun']
            kps_id = json_data['kps_id']
            
            # Ambil keterangan
            keterangan = safe_str(record.get(JSON_FIELD_MAPPING['keterangan']))
            if not keterangan:
                keterangan = f"Import dari {JSON_FILE}"
            
            if dry_run:
                logger.info(f"[DRY RUN] Akan insert: pendamping_id={pendamping_id}, tahun={tahun}, kps_id={kps_id}")
                success_count += 1
                continue
            
            # Insert ke database
            try:
                cur.execute(
                    """
                    INSERT INTO pendampingan 
                    (pendamping_id, tahun_pendampingan, kps_id, keterangan, waktu_upload)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_pendampingan
                    """,
                    (
                        pendamping_id,
                        tahun,
                        kps_id,
                        keterangan[:255],
                        datetime.utcnow()
                    )
                )
                id_pendampingan = cur.fetchone()[0]
                logger.debug(f"Inserted pendampingan id={id_pendampingan}")
                success_count += 1
                
                # Commit per 100 record
                if success_count % 100 == 0:
                    conn.commit()
                    logger.debug(f"Committed batch: {success_count} records")
                    
            except psycopg2.IntegrityError as e:
                # Duplicate key atau constraint violation
                logger.warning(f"Record mungkin sudah ada (duplicate): {e}")
                conn.rollback()
            except psycopg2.Error as e:
                logger.error(f"Error insert record: {e}")
                logger.error(f"Data: pendamping_id={pendamping_id}, tahun={tahun}, kps_id={kps_id}")
                conn.rollback()
        
        # Final commit
        if not dry_run:
            conn.commit()
            logger.info(f"Final commit selesai. Total {success_count} record berhasil di-insert")
        
    except Exception as e:
        logger.error(f"Error dalam proses insert: {e}")
        if not dry_run:
            conn.rollback()
        raise
    finally:
        cur.close()
    
    return success_count


def delete_extra_records(conn, extra_records: List[Dict], dry_run: bool = False) -> int:
    """
    Hapus record yang ada di DB tapi tidak ada di JSON.
    
    Args:
        conn: Koneksi database
        extra_records: List record yang perlu dihapus
        dry_run: Jika True, hanya log tanpa delete
        
    Returns:
        int: Jumlah record yang berhasil dihapus
    """
    if not extra_records:
        logger.info("Tidak ada record yang perlu dihapus")
        return 0
    
    logger.info(f"Memulai hapus {len(extra_records)} record yang tidak ada di JSON...")
    
    cur = conn.cursor()
    success_count = 0
    
    try:
        for idx, extra_data in enumerate(extra_records, 1):
            if idx % 100 == 0:
                logger.info(f"Progress delete: {idx}/{len(extra_records)}")
            
            db_record = extra_data['db_record']
            id_pendampingan = db_record['id_pendampingan']
            
            if dry_run:
                logger.info(f"[DRY RUN] Akan hapus: id_pendampingan={id_pendampingan}, "
                          f"pendamping_id={db_record['pendamping_id']}, "
                          f"tahun={db_record['tahun_pendampingan']}, "
                          f"kps_id={db_record['kps_id']}")
                success_count += 1
                continue
            
            # Delete dari database
            try:
                cur.execute(
                    "DELETE FROM pendampingan WHERE id_pendampingan = %s",
                    (id_pendampingan,)
                )
                logger.debug(f"Deleted pendampingan id={id_pendampingan}")
                success_count += 1
                
                # Commit per 100 record
                if success_count % 100 == 0:
                    conn.commit()
                    logger.debug(f"Committed batch: {success_count} records")
                    
            except psycopg2.Error as e:
                logger.error(f"Error delete record: {e}")
                logger.error(f"Data: id_pendampingan={id_pendampingan}")
                conn.rollback()
        
        # Final commit
        if not dry_run:
            conn.commit()
            logger.info(f"Final commit selesai. Total {success_count} record berhasil dihapus")
        
    except Exception as e:
        logger.error(f"Error dalam proses delete: {e}")
        if not dry_run:
            conn.rollback()
        raise
    finally:
        cur.close()
    
    return success_count


# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    """Entry point utama script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validasi dan perbaikan data pendampingan')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Hanya validasi tanpa melakukan perubahan (default: False)')
    parser.add_argument('--fix', action='store_true',
                       help='Lakukan perbaikan data (insert missing, delete extra)')
    parser.add_argument('--insert-only', action='store_true',
                       help='Hanya insert record yang missing, tidak hapus record extra')
    parser.add_argument('--delete-only', action='store_true',
                       help='Hanya hapus record yang extra, tidak insert record missing')
    
    args = parser.parse_args()
    
    print("=" * 80, flush=True)
    print("VALIDASI DAN PERBAIKAN DATA PENDAMPINGAN", flush=True)
    print("=" * 80, flush=True)
    
    if args.dry_run:
        print("MODE: DRY RUN (tidak akan melakukan perubahan)", flush=True)
    elif args.fix:
        print("MODE: PERBAIKAN (akan melakukan perubahan)", flush=True)
    else:
        print("MODE: VALIDASI SAJA (tidak akan melakukan perubahan)", flush=True)
        print("Gunakan --fix untuk melakukan perbaikan", flush=True)
    
    print("=" * 80, flush=True)
    
    conn = None
    
    try:
        # Baca JSON
        logger.info(f"Membaca file JSON: {JSON_FILE}")
        json_records = load_json(JSON_FILE)
        
        # Koneksi database
        logger.info("Membuka koneksi database...")
        conn = get_connection()
        
        # Validasi
        logger.info("Memulai proses validasi...")
        validation_result = validate_data(conn, json_records)
        
        # Tampilkan hasil validasi
        stats = validation_result['stats']
        logger.info("=" * 80)
        logger.info("HASIL VALIDASI")
        logger.info("=" * 80)
        logger.info(f"Total record di JSON: {stats['total_json_records']}")
        logger.info(f"Record JSON yang valid: {stats['valid_json_records']}")
        logger.info(f"Record JSON yang tidak bisa diproses: {stats['missing_pendamping']}")
        logger.info(f"Total record di database: {stats['total_db_records']}")
        logger.info(f"Record yang cocok: {stats['matching_records']}")
        logger.info(f"Record missing di database: {stats['missing_in_db']}")
        logger.info(f"Record extra di database: {stats['missing_in_json']}")
        logger.info("=" * 80)
        
        # Perbaikan
        if args.fix and not args.dry_run:
            logger.info("Memulai proses perbaikan...")
            
            # Insert missing records
            if not args.delete_only:
                logger.info("Memproses insert record yang missing...")
                inserted = insert_missing_records(conn, validation_result['missing_in_db'], dry_run=False)
                logger.info(f"Berhasil insert {inserted} record")
            
            # Delete extra records
            if not args.insert_only:
                logger.info("Memproses hapus record yang extra...")
                deleted = delete_extra_records(conn, validation_result['missing_in_json'], dry_run=False)
                logger.info(f"Berhasil hapus {deleted} record")
            
            logger.info("Proses perbaikan selesai!")
        elif args.dry_run:
            logger.info("DRY RUN: Menampilkan perubahan yang akan dilakukan...")
            
            if not args.delete_only:
                logger.info("Record yang akan di-insert:")
                insert_missing_records(conn, validation_result['missing_in_db'], dry_run=True)
            
            if not args.insert_only:
                logger.info("Record yang akan dihapus:")
                delete_extra_records(conn, validation_result['missing_in_json'], dry_run=True)
        
        # Simpan laporan detail
        report_file = 'laporan_validasi_pendampingan.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            # Convert untuk JSON serialization
            report_data = {
                'stats': stats,
                'missing_in_db_count': len(validation_result['missing_in_db']),
                'missing_in_json_count': len(validation_result['missing_in_json']),
                'missing_pendamping_count': len(validation_result['missing_pendamping']),
                'timestamp': datetime.utcnow().isoformat()
            }
            json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Laporan detail disimpan ke: {report_file}")
        
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
    
    logger.info("=" * 80)
    logger.info("PROSES SELESAI")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()


