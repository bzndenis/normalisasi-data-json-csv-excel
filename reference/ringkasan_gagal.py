#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script sederhana untuk ringkasan record gagal"""

import json
import re

log_file = 'import_pendampingan.log'
output_file = 'ringkasan_record_gagal.txt'

with open(log_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Kategorisasi
pendamping_gagal = []
kps_no_sk_kosong = []
kps_error_lain = []
no_email_nama = []

i = 0
while i < len(lines):
    line = lines[i]
    
    # Pendamping tidak ditemukan
    if 'Pendamping tidak ditemukan untuk nama' in line:
        nama_match = re.search(r"nama '([^']+)'", line)
        email_match = re.search(r"email '([^']+)'", line)
        pendamping_gagal.append({
            'line': i+1,
            'nama': nama_match.group(1) if nama_match else '',
            'email': email_match.group(1) if email_match else ''
        })
    
    # Record tanpa email/nama
    elif 'Record tidak memiliki email maupun nama pendamping' in line:
        no_email_nama.append({'line': i+1})
    
    # KPS gagal dibuat
    elif 'KPS tidak ditemukan dan gagal dibuat' in line:
        no_sk_match = re.search(r"no_sk='([^']*)'", line)
        skema_match = re.search(r"skema_ps='([^']*)'", line)
        no_sk = no_sk_match.group(1) if no_sk_match else ''
        
        # Ambil MISSING KPS data
        missing_data = None
        if i + 1 < len(lines) and 'MISSING KPS:' in lines[i+1]:
            try:
                json_str = re.search(r'\{.*\}', lines[i+1])
                if json_str:
                    missing_data = json.loads(json_str.group())
            except:
                pass
        
        if not no_sk or no_sk.strip() == '':
            kps_no_sk_kosong.append({
                'line': i+1,
                'data': missing_data
            })
        else:
            kps_error_lain.append({
                'line': i+1,
                'no_sk': no_sk,
                'skema_ps': skema_match.group(1) if skema_match else '',
                'data': missing_data
            })
    
    i += 1

# Tulis output
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 100 + "\n")
    f.write("RINGKASAN LENGKAP RECORD YANG GAGAL\n")
    f.write("=" * 100 + "\n\n")
    
    # 1. Pendamping tidak ditemukan
    f.write(f"1. GAGAL: PENDAMPING TIDAK DITEMUKAN ({len(pendamping_gagal)} record)\n")
    f.write("-" * 100 + "\n")
    for idx, item in enumerate(pendamping_gagal, 1):
        f.write(f"{idx}. Line {item['line']}: Nama='{item['nama']}', Email='{item['email']}'\n")
    
    # 2. KPS gagal - NO SK kosong
    f.write(f"\n\n2. GAGAL: KPS TIDAK DIBUAT KARENA NO SK KOSONG ({len(kps_no_sk_kosong)} record)\n")
    f.write("-" * 100 + "\n")
    f.write("(Record ini tidak bisa dibuat master_kps karena validasi memerlukan no_sk)\n\n")
    for idx, item in enumerate(kps_no_sk_kosong[:100], 1):  # Limit 100
        f.write(f"{idx}. Line {item['line']}:\n")
        if item['data']:
            f.write(f"   SKEMA PS: {item['data'].get('skema_ps', 'N/A')}\n")
            f.write(f"   KPS: {item['data'].get('kps', 'N/A')}\n")
            f.write(f"   Nama Pendamping: {item['data'].get('nama_pendamping', 'N/A')}\n")
            f.write(f"   Email: {item['data'].get('email', 'N/A')}\n")
        f.write("\n")
    
    if len(kps_no_sk_kosong) > 100:
        f.write(f"... dan {len(kps_no_sk_kosong) - 100} record lainnya dengan NO SK kosong\n")
    
    # 3. KPS error lain
    f.write(f"\n\n3. GAGAL: KPS TIDAK DITEMUKAN/DIBUAT - ERROR LAIN ({len(kps_error_lain)} record)\n")
    f.write("-" * 100 + "\n")
    for idx, item in enumerate(kps_error_lain[:50], 1):  # Limit 50
        f.write(f"{idx}. Line {item['line']}:\n")
        f.write(f"   No SK: {item['no_sk']}\n")
        f.write(f"   SKEMA PS: {item['skema_ps']}\n")
        if item['data']:
            f.write(f"   KPS: {item['data'].get('kps', 'N/A')}\n")
        f.write("\n")
    
    if len(kps_error_lain) > 50:
        f.write(f"... dan {len(kps_error_lain) - 50} record lainnya\n")
    
    # 4. Tidak ada email/nama
    f.write(f"\n\n4. GAGAL: TIDAK MEMILIKI EMAIL MAUPUN NAMA PENDAMPING ({len(no_email_nama)} record)\n")
    f.write("-" * 100 + "\n")
    f.write("(Record dengan NO kosong yang tidak bisa resolve pendamping_id)\n")
    for idx, item in enumerate(no_email_nama[:50], 1):
        f.write(f"{idx}. Line {item['line']}\n")
    
    if len(no_email_nama) > 50:
        f.write(f"... dan {len(no_email_nama) - 50} record lainnya\n")
    
    # Statistik
    f.write("\n\n" + "=" * 100 + "\n")
    f.write("STATISTIK RINGKAS\n")
    f.write("=" * 100 + "\n")
    f.write(f"Pendamping tidak ditemukan: {len(pendamping_gagal)}\n")
    f.write(f"KPS gagal (NO SK kosong): {len(kps_no_sk_kosong)}\n")
    f.write(f"KPS gagal (error lain): {len(kps_error_lain)}\n")
    f.write(f"Tidak ada email/nama: {len(no_email_nama)}\n")
    f.write(f"TOTAL: {len(pendamping_gagal) + len(kps_no_sk_kosong) + len(kps_error_lain) + len(no_email_nama)}\n")

print(f"Ringkasan dibuat: {output_file}")
print(f"Statistik: Pendamping={len(pendamping_gagal)}, KPS no_sk kosong={len(kps_no_sk_kosong)}, KPS error lain={len(kps_error_lain)}, No email/nama={len(no_email_nama)}")
