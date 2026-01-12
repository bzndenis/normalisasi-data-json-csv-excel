#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk extract dan rangkum semua record yang gagal dari log file.
"""

import re
import json
from collections import defaultdict

log_file = 'import_pendampingan.log'
output_file = 'ringkasan_record_gagal.txt'

# Baca log file
with open(log_file, 'r', encoding='utf-8') as f:
    log_content = f.read()

# Kategori error
pendamping_errors = []
missing_kps_errors = []
no_email_nama_errors = []
other_errors = []

# Extract semua error
lines = log_content.split('\n')

for i, line in enumerate(lines):
    # Error: Pendamping tidak ditemukan
    if 'Pendamping tidak ditemukan untuk nama' in line:
        pendamping_errors.append({
            'line_num': i + 1,
            'message': line,
            'context': '\n'.join(lines[max(0, i-2):min(len(lines), i+3)])
        })
    
    # Error: Record tidak memiliki email maupun nama
    elif 'Record tidak memiliki email maupun nama pendamping' in line:
        no_email_nama_errors.append({
            'line_num': i + 1,
            'message': line,
            'context': '\n'.join(lines[max(0, i-5):min(len(lines), i+2)])
        })
    
    # Error: KPS tidak ditemukan dan gagal dibuat (karena no_sk kosong atau error lain)
    elif 'KPS tidak ditemukan dan gagal dibuat' in line:
        # Ambil MISSING KPS yang mengikutinya
        missing_kps_data = None
        if i + 1 < len(lines) and 'MISSING KPS:' in lines[i + 1]:
            try:
                json_match = re.search(r'\{.*\}', lines[i + 1])
                if json_match:
                    missing_kps_data = json.loads(json_match.group())
            except:
                pass
        
        missing_kps_errors.append({
            'line_num': i + 1,
            'message': line,
            'missing_kps_data': missing_kps_data,
            'context': '\n'.join(lines[max(0, i-2):min(len(lines), i+3)])
        })
    
    # Error lainnya
    elif 'ERROR' in line and 'Error insert pendampingan' not in line:
        other_errors.append({
            'line_num': i + 1,
            'message': line,
            'context': '\n'.join(lines[max(0, i-2):min(len(lines), i+10)])
        })

# Tulis ringkasan ke file
print("Menulis ringkasan ke file...")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 100 + "\n")
    f.write("RINGKASAN LENGKAP RECORD YANG GAGAL\n")
    f.write("=" * 100 + "\n\n")
    
    # 1. Pendamping tidak ditemukan
    f.write(f"\n1. GAGAL KARENA PENDAMPING TIDAK DITEMUKAN: {len(pendamping_errors)} record\n")
    f.write("-" * 100 + "\n")
    for idx, err in enumerate(pendamping_errors, 1):
        f.write(f"\n{idx}. Line {err['line_num']}:\n")
        f.write(f"   {err['message']}\n")
        # Extract nama dan email dari message
        nama_match = re.search(r"nama '([^']+)'", err['message'])
        email_match = re.search(r"email '([^']+)'", err['message'])
        if nama_match:
            f.write(f"   Nama: {nama_match.group(1)}\n")
        if email_match:
            f.write(f"   Email: {email_match.group(1)}\n")
    
    # 2. KPS tidak ditemukan dan gagal dibuat
    f.write(f"\n\n2. GAGAL KARENA KPS TIDAK DITEMUKAN/DIBUAT: {len(missing_kps_errors)} record\n")
    f.write("-" * 100 + "\n")
    
    # Kelompokkan berdasarkan penyebab
    no_sk_empty = []
    no_sk_filled = []
    
    for err in missing_kps_errors:
        if err['missing_kps_data']:
            no_sk = err['missing_kps_data'].get('no_sk', '')
            if not no_sk or no_sk.strip() == '':
                no_sk_empty.append(err)
            else:
                no_sk_filled.append(err)
        else:
            no_sk_filled.append(err)
    
    f.write(f"\n   a) KPS gagal dibuat karena NO SK KOSONG: {len(no_sk_empty)} record\n")
    f.write("   " + "-" * 96 + "\n")
    for idx, err in enumerate(no_sk_empty[:50], 1):  # Limit 50 untuk tidak terlalu panjang
        f.write(f"\n   {idx}. Line {err['line_num']}:\n")
        if err['missing_kps_data']:
            data = err['missing_kps_data']
            f.write(f"      No SK: (KOSONG)\n")
            f.write(f"      SKEMA PS: {data.get('skema_ps', 'N/A')}\n")
            f.write(f"      Nama Pendamping: {data.get('nama_pendamping', 'N/A')}\n")
            f.write(f"      Email: {data.get('email', 'N/A')}\n")
            f.write(f"      KPS: {data.get('kps', 'N/A')}\n")
        f.write(f"      {err['message']}\n")
    
    if len(no_sk_empty) > 50:
        f.write(f"\n   ... dan {len(no_sk_empty) - 50} record lainnya dengan NO SK kosong\n")
    
    f.write(f"\n   b) KPS gagal dibuat karena error lain (NO SK ada): {len(no_sk_filled)} record\n")
    f.write("   " + "-" * 96 + "\n")
    for idx, err in enumerate(no_sk_filled[:30], 1):  # Limit 30
        f.write(f"\n   {idx}. Line {err['line_num']}:\n")
        f.write(f"      {err['message']}\n")
        if err['missing_kps_data']:
            data = err['missing_kps_data']
            f.write(f"      No SK: {data.get('no_sk', 'N/A')}\n")
            f.write(f"      SKEMA PS: {data.get('skema_ps', 'N/A')}\n")
            f.write(f"      KPS: {data.get('kps', 'N/A')}\n")
    
    if len(no_sk_filled) > 30:
        f.write(f"\n   ... dan {len(no_sk_filled) - 30} record lainnya\n")
    
    # 3. Record tanpa email dan nama
    f.write(f"\n\n3. GAGAL KARENA TIDAK MEMILIKI EMAIL MAUPUN NAMA PENDAMPING: {len(no_email_nama_errors)} record\n")
    f.write("-" * 100 + "\n")
    f.write("   (Ini biasanya record dengan NO kosong yang tidak bisa resolve pendamping_id karena tidak ada data identitas)\n")
    for idx, err in enumerate(no_email_nama_errors[:20], 1):  # Limit 20
        f.write(f"\n   {idx}. Line {err['line_num']}: {err['message']}\n")
    
    if len(no_email_nama_errors) > 20:
        f.write(f"\n   ... dan {len(no_email_nama_errors) - 20} record lainnya\n")
    
    # 4. Error lainnya
    f.write(f"\n\n4. ERROR LAINNYA: {len(other_errors)} record\n")
    f.write("-" * 100 + "\n")
    for idx, err in enumerate(other_errors, 1):
        f.write(f"\n{idx}. Line {err['line_num']}:\n")
        f.write(f"   {err['message']}\n")
        if 'context' in err and err['context']:
            f.write(f"   Context:\n{err['context'][:500]}\n")
    
    # Ringkasan statistik
    f.write("\n\n" + "=" * 100 + "\n")
    f.write("RINGKASAN STATISTIK\n")
    f.write("=" * 100 + "\n")
    f.write(f"Total record gagal karena pendamping tidak ditemukan: {len(pendamping_errors)}\n")
    f.write(f"Total record gagal karena KPS tidak ditemukan/dibuat: {len(missing_kps_errors)}\n")
    f.write(f"  - Karena NO SK kosong: {len(no_sk_empty)}\n")
    f.write(f"  - Karena error lain: {len(no_sk_filled)}\n")
    f.write(f"Total record tanpa email/nama: {len(no_email_nama_errors)}\n")
    f.write(f"Total error lainnya: {len(other_errors)}\n")
    f.write(f"TOTAL SEMUA ERROR: {len(pendamping_errors) + len(missing_kps_errors) + len(no_email_nama_errors) + len(other_errors)}\n")

print(f"Ringkasan lengkap telah dibuat di: {output_file}")
print(f"\nStatistik:")
print(f"- Pendamping tidak ditemukan: {len(pendamping_errors)}")
print(f"- KPS tidak ditemukan/dibuat: {len(missing_kps_errors)}")
print(f"  - NO SK kosong: {len(no_sk_empty)}")
print(f"  - Error lain: {len(no_sk_filled)}")
print(f"- Tidak ada email/nama: {len(no_email_nama_errors)}")
print(f"- Error lainnya: {len(other_errors)}")
