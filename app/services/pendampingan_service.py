import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Generator
import psycopg2
from psycopg2.extras import execute_values
from app.config import settings

logger = logging.getLogger(__name__)

class PendampinganService:
    def __init__(self):
        # Configure DB connection based on settings or defaults
        self.db_config = {
            'host': settings.DB_HOST,
            'port': settings.DB_PORT,
            'dbname': settings.DB_NAME,
            'user': settings.DB_USER,
            'password': settings.DB_PASSWORD
        }
        
        # Mapping field JSON ke field database
        self.JSON_FIELD_MAPPING = {
            'tahun_pendampingan': 'TAHUN PENDAMPINGAN',
            'no_sk_kps': 'NO SK KPS',
            'nama_pendamping': 'NAMA PENDAMPING',
            'email': 'EMAIL',
            'skema_ps': 'SKEMA PS',
            'no': 'NO',
            'keterangan': 'KETERANGAN',
            'kps': 'KPS',
        }
        
        self.INSERT_WITH_NULL_KPS_ID = True

    def get_connection(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except psycopg2.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def safe_str(self, value, default=''):
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            return value.strip() if value.strip() else default
        return str(value).strip() if str(value).strip() else default

    def resolve_user_id(self, conn, record: Dict) -> Optional[int]:
        cur = conn.cursor()
        email = self.safe_str(record.get(self.JSON_FIELD_MAPPING['email']), '')
        nama = self.safe_str(record.get(self.JSON_FIELD_MAPPING['nama_pendamping']), '')
        
        try:
            if email:
                cur.execute("SELECT user_id FROM users WHERE LOWER(TRIM(user_email)) = LOWER(TRIM(%s)) LIMIT 2", (email,))
                results = cur.fetchall()
                if len(results) == 1:
                    return results[0][0]
            
            if nama:
                cur.execute("SELECT user_id FROM users WHERE LOWER(TRIM(user_nama)) = LOWER(TRIM(%s)) LIMIT 2", (nama,))
                results = cur.fetchall()
                if len(results) == 1:
                    return results[0][0]
                    
            return None
        finally:
            cur.close()

    def resolve_pendamping_id(self, conn, user_id: int) -> Optional[int]:
        """Resolve pendamping_id from master_pendamping table given a user_id"""
        if not user_id:
            return None
        cur = conn.cursor()
        try:
            cur.execute("SELECT pendamping_id FROM master_pendamping WHERE user_id = %s LIMIT 1", (user_id,))
            res = cur.fetchone()
            if res:
                return res[0]
            # Optional: Create master_pendamping record if missing? For now returning None.
            return None
        finally:
            cur.close()

    def resolve_kps_id(self, conn, no_sk: str, skema_ps: Optional[str] = None, record: Optional[Dict] = None) -> Optional[int]:
        no_sk_str = self.safe_str(no_sk)
        if not no_sk_str:
            return None
            
        schema_normalized = None
        is_valid_schema = False
        
        if skema_ps:
            skema_lower = self.safe_str(skema_ps).lower().strip()
            if skema_lower in ['hutan adat', 'lphd', 'ha', 'hn', 'lphn']:
                schema_normalized = 'ha'
                is_valid_schema = True
            elif skema_lower == 'kk':
                schema_normalized = 'kk'
                is_valid_schema = True
        
        if not skema_ps:
            return None
            
        cur = conn.cursor()
        try:
            # Search logic
            if schema_normalized:
                cur.execute("SELECT id FROM master_kps WHERE TRIM(no_sk) = TRIM(%s) AND LOWER(TRIM(COALESCE(schema, ''))) = %s LIMIT 1", (no_sk_str, schema_normalized))
                res = cur.fetchone()
                if res: return res[0]
                
            cur.execute("SELECT id FROM master_kps WHERE TRIM(no_sk) = TRIM(%s) LIMIT 1", (no_sk_str,))
            res = cur.fetchone()
            if res: return res[0]
            
            # Create logic if not found and allowed
            if record and is_valid_schema:
                try:
                    # Extract fields for creation
                    nama_kps = self.safe_str(record.get(self.JSON_FIELD_MAPPING['kps']))
                    # Enforce name presence
                    if not nama_kps:
                        logger.warning(f"Cannot create KPS for {no_sk_str}: Missing KPS Name")
                        return None

                    provinsi = self.safe_str(record.get('PROVINSI'))
                    kab_kota = self.safe_str(record.get('KABUPATEN/KOTA'))
                    kecamatan = self.safe_str(record.get('KECAMATAN'))
                    desa = self.safe_str(record.get('DESA/KELURAHAN'))
                    
                    luas_str = record.get('LUAS SK PS')
                    luas_sk = None
                    if luas_str:
                        try:
                            luas_sk = float(luas_str)
                        except (ValueError, TypeError):
                            pass

                    # Insert new KPS
                    cur.execute("""
                        INSERT INTO master_kps (
                            no_sk, schema, kps_name, 
                            provinsi, kabupaten_kota, kecamatan, desa_kelurahan,
                            luas_sk, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, NOW(), NOW()
                        ) RETURNING id
                    """, (
                        no_sk_str, schema_normalized, nama_kps,
                        provinsi, kab_kota, kecamatan, desa,
                        luas_sk
                    ))
                    
                    new_id = cur.fetchone()[0]
                    logger.info(f"Created new master_kps: {no_sk_str} ({schema_normalized}) - {nama_kps}")
                    return new_id
                    
                except Exception as e:
                    logger.error(f"Failed to auto-create KPS {no_sk_str}: {e}")
                    return None
                
            return None
        finally:
            cur.close()

    def create_pendamping(self, conn, record: Dict) -> Tuple[Optional[int], Optional[int]]:
        """
        Create a new user and master_pendamping record.
        Returns (pendamping_id, user_id)
        """
        nama = self.safe_str(record.get(self.JSON_FIELD_MAPPING['nama_pendamping']))
        email = self.safe_str(record.get(self.JSON_FIELD_MAPPING['email']))
        
        if not nama:
            return None, None
            
        # Generate dummy email if missing to satisfy NOT NULL constraint
        if not email:
            clean_name = "".join(c for c in nama if c.isalnum()).lower()
            timestamp = datetime.now().strftime("%f")
            email = f"{clean_name}.{timestamp}@noemail.com"
            
        cur = conn.cursor()
        try:
            # 1. Create User
            # Check if email exists (in case resolve missed it or race condition)
            cur.execute("SELECT user_id FROM users WHERE user_email = %s", (email,))
            if cur.fetchone():
                # If collision, try appending random
                email = f"{datetime.now().timestamp()}_{email}"
                
            cur.execute("""
                INSERT INTO users (user_nama, user_email, user_password, user_type, user_status, created_at, updated_at)
                VALUES (%s, %s, '123456', 'pendamping', 'aktif', NOW(), NOW())
                RETURNING user_id
            """, (nama, email))
            user_id = cur.fetchone()[0]
            
            # 2. Create Master Pendamping
            cur.execute("""
                INSERT INTO master_pendamping (user_id, created_at, updated_at)
                VALUES (%s, NOW(), NOW())
                RETURNING pendamping_id
            """, (user_id,))
            pendamping_id = cur.fetchone()[0]
            
            logger.info(f"Created new pendamping: {nama} ({email}) -> user_id={user_id}, pendamping_id={pendamping_id}")
            return pendamping_id, user_id
            
        except Exception as e:
            logger.error(f"Failed to create pendamping {nama}: {e}")
            return None, None
        finally:
            cur.close()

    def process_import(self, file_content: bytes) -> Generator[str, None, None]:
        """
        Process uploaded JSON file and yield progress updates.
        Yields JSON strings formatted for SSE: "data: {...}\n\n"
        """
        try:
            data = json.loads(file_content)
            if not isinstance(data, list):
                yield f"data: {json.dumps({'log': 'Error: JSON must be a list'})}\n\n"
                return

            total_records = len(data)
            stats = {'total': total_records, 'success': 0, 'failed': 0, 'created': 0}
            failed_details = []
            
            yield f"data: {json.dumps({'log': f'Starting import of {total_records} records', 'stats': stats})}\n\n"
            
            conn = self.get_connection()
            conn.autocommit = False # Use transaction
            
            last_pendamping_id = None
            last_user_id = None
            last_tahun = None
            
            for idx, record in enumerate(data, 1):
                try:
                    # Logic adaptation from reference
                    # 1. Validation (Email & No SK mandatories)
                    email_raw = self.safe_str(record.get(self.JSON_FIELD_MAPPING['email']))
                    no_sk_raw = self.safe_str(record.get(self.JSON_FIELD_MAPPING['no_sk_kps']))
                    
                    if not email_raw:
                        stats['failed'] += 1
                        failed_details.append({
                            'row': idx,
                            'reason': 'email_missing',
                            'message': 'Email is required',
                            'record': record
                        })
                        yield f"data: {json.dumps({'log': f'Row {idx}: Email missing'})}\n\n"
                        continue

                    if not no_sk_raw:
                        stats['failed'] += 1
                        failed_details.append({
                            'row': idx,
                            'reason': 'no_sk_missing',
                            'message': 'No SK KPS is required',
                            'record': record
                        })
                        yield f"data: {json.dumps({'log': f'Row {idx}: No SK KPS missing'})}\n\n"
                        continue

                    # 2. Resolve Pendamping
                    no_value = record.get(self.JSON_FIELD_MAPPING['no'])
                    is_no_empty = (no_value is None or self.safe_str(no_value) == '')
                    
                    pendamping_id = None
                    user_id = None
                    
                    if is_no_empty and last_pendamping_id:
                        pendamping_id = last_pendamping_id
                        user_id = last_user_id
                    else:
                        user_id = self.resolve_user_id(conn, record)
                        
                        if user_id:
                            # User exists, check master_pendamping
                            pendamping_id = self.resolve_pendamping_id(conn, user_id)
                            if not pendamping_id:
                                # User exists but not in master_pendamping -> Insert into master_pendamping
                                cur_create = conn.cursor()
                                try:
                                    cur_create.execute("""
                                        INSERT INTO master_pendamping (user_id, created_at, updated_at)
                                        VALUES (%s, NOW(), NOW())
                                        RETURNING pendamping_id
                                    """, (user_id,))
                                    pendamping_id = cur_create.fetchone()[0]
                                    stats['created'] += 1
                                    yield f"data: {json.dumps({'log': f'Row {idx}: Created master_pendamping for existing user {user_id}'})}\n\n"
                                finally:
                                    cur_create.close()
                        else:
                            # User does not exist -> Create User AND Master Pendamping
                            # Note: No need to generate dummy email, we checked valid email above
                            pendamping_id, user_id = self.create_pendamping(conn, record)
                            if pendamping_id:
                                stats['created'] += 1
                                yield f"data: {json.dumps({'log': f'Row {idx}: Created new user & pendamping'})}\n\n"

                        if pendamping_id and user_id:
                            last_pendamping_id = pendamping_id
                            last_user_id = user_id
                    
                    if not pendamping_id:
                        stats['failed'] += 1
                        error_msg = f"Pendamping not found and creation failed: {email_raw} / {self.safe_str(record.get(self.JSON_FIELD_MAPPING['nama_pendamping']))}"
                        failed_details.append({
                            'row': idx,
                            'reason': 'pendamping_creation_failed',
                            'message': error_msg,
                            'record': record
                        })
                        yield f"data: {json.dumps({'log': f'Row {idx}: {error_msg}'})}\n\n"
                        continue

                    # 3. Year
                    tahun = self.safe_str(record.get(self.JSON_FIELD_MAPPING['tahun_pendampingan']))
                    if is_no_empty and not tahun and last_tahun:
                        tahun = last_tahun
                    elif tahun:
                        last_tahun = tahun
                    
                    if not tahun:
                        stats['failed'] += 1
                        failed_details.append({
                            'row': idx,
                            'reason': 'year_missing',
                            'message': 'Tahun pendampingan missing',
                            'record': record
                        })
                        continue

                    # 4. Resolve KPS
                    no_sk = record.get(self.JSON_FIELD_MAPPING['no_sk_kps'])
                    skema = record.get(self.JSON_FIELD_MAPPING['skema_ps'])
                    kps_id = self.resolve_kps_id(conn, no_sk, skema, record)
                    
                    # Optional: Fail if KPS ID not resolved? 
                    # If No SK was present but invalid/not found, kps_id is None.
                    # Per user request "jika nomor sk ... tidak ada", we handled the *missing string* case.
                    # If the SK string exists but is not in DB, do we fail?
                    # "reference/import_pendampingan.py" allowed NULL kps_id.
                    # I will keep allowing NULL kps_id if resolve fails (but string exists), 
                    # ONLY failing if the string itself was missing (checked above).
                    
                    # 4. Insert
                    cur = conn.cursor()
                    keterangan = self.safe_str(record.get(self.JSON_FIELD_MAPPING['keterangan']), 'Imported via Web')
                    
                    # Update Insert to include user_id if the table supports it (as per SQL reference)
                    cur.execute("""
                        INSERT INTO pendampingan 
                        (pendamping_id, user_id, tahun_pendampingan, kps_id, keterangan, waktu_upload)
                        VALUES (%s, %s, %s, %s, %s, NOW())
                        RETURNING id_pendampingan
                    """, (pendamping_id, user_id, tahun, kps_id, keterangan))
                    
                    stats['success'] += 1
                    
                    if idx % 10 == 0:
                        progress = round((idx / total_records) * 100)
                        yield f"data: {json.dumps({'progress': progress, 'stats': stats})}\n\n"
                        conn.commit()
                        
                except Exception as e:
                    stats['failed'] += 1
                    failed_details.append({
                        'row': idx,
                        'reason': 'exception',
                        'message': str(e),
                        'record': record
                    })
                    logger.error(f"Error row {idx}: {e}")
                    conn.rollback()
            
            conn.commit()
            conn.close()
            
            # Generate Report if needed
            failed_report_url = None
            if failed_details:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"failed_import_{timestamp}.json"
                filepath = os.path.join(settings.EXPORT_DIR, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(failed_details, f, indent=2)
                
                failed_report_url = f"/static/exports/{filename}"
                # Ensure static mount or route exists for this, assume /exports maps there or serve via separate route.
                # Actually main.py mounts /static. If EXPORT_DIR is not inside static, we need a route.
                # Let's save to a path we can serve or create a route. 
                # For simplicity, assuming EXPORT_DIR is accessible or we create a route.
                # Let's use a specialized route to serve these.
                failed_report_url = f"/exports/{filename}"

            yield f"data: {json.dumps({'progress': 100, 'stats': stats, 'log': 'Import completed!', 'failed_report_url': failed_report_url})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'log': f'Critical Error: {str(e)}'})}\n\n"

    def load_db_pendampingan(self, conn) -> Dict:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT pendamping_id, tahun_pendampingan, kps_id, keterangan
                FROM pendampingan
            """)
            records = cur.fetchall()
            result = {}
            for record in records:
                key = (record[0], self.safe_str(record[1]), record[2])
                result[key] = {
                    'pendamping_id': record[0], 
                    'tahun': str(record[1]), 
                    'kps_id': record[2],
                    'keterangan': record[3]
                }
            return result
        finally:
            cur.close()

    def validate_data(self, file_content: bytes, fix: bool = False, dry_run: bool = False) -> Dict:
        try:
            json_records = json.loads(file_content)
        except json.JSONDecodeError:
            return {'error': 'Invalid JSON format'}
            
        conn = self.get_connection()
        try:
            db_records = self.load_db_pendampingan(conn)
            
            missing_in_db = []
            missing_in_json = []
            
            # Index JSON
            json_index = {}
            last_pendamping_id = None
            last_tahun = None
            
            for idx, record in enumerate(json_records):
                no_value = record.get(self.JSON_FIELD_MAPPING['no'])
                is_no_empty = (no_value is None or self.safe_str(no_value) == '')
                
                if is_no_empty and last_pendamping_id:
                    pendamping_id = last_pendamping_id
                    tahun = last_tahun
                else:
                    pendamping_id = self.resolve_pendamping_id(conn, record)
                    tahun = self.safe_str(record.get(self.JSON_FIELD_MAPPING['tahun_pendampingan']))
                    if pendamping_id:
                        last_pendamping_id = pendamping_id
                        last_tahun = tahun
                
                no_sk = record.get(self.JSON_FIELD_MAPPING['no_sk_kps'])
                skema = record.get(self.JSON_FIELD_MAPPING['skema_ps'])
                kps_id = self.resolve_kps_id(conn, no_sk, skema)
                
                if pendamping_id and tahun:
                    key = (pendamping_id, tahun, kps_id)
                    json_index[key] = record
            
            # Compare
            for key in json_index:
                if key not in db_records:
                    missing_in_db.append({'key': str(key), 'record': json_index[key]})
            
            for key in db_records:
                if key not in json_index:
                    missing_in_json.append({'key': str(key), 'db_record': db_records[key]})
            
            result = {
                'stats': {
                    'total_json': len(json_records),
                    'valid_json_keys': len(json_index),
                    'total_db': len(db_records),
                    'missing_in_db': len(missing_in_db),
                    'missing_in_json': len(missing_in_json)
                },
                'missing_in_db': missing_in_db[:50], # Limit output
                'missing_in_json': missing_in_json[:50]
            }
            
            # Fix logic placeholder (implement if needed)
            if fix and not dry_run:
                pass # Implement actual fix logic here
                
            return result
        finally:
            conn.close()

