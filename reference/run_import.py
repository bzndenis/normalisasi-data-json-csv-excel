#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrapper script untuk menjalankan import dengan output yang lebih jelas"""

import sys
import os

# Redirect output ke file juga
output_file = open('import_output.txt', 'w', encoding='utf-8')

def log(message):
    """Print ke console dan file"""
    print(message, flush=True)
    output_file.write(message + '\n')
    output_file.flush()

log("=" * 80)
log("MEMULAI IMPORT DATA PENDAMPINGAN")
log("=" * 80)

try:
    # Import dan jalankan main script
    import import_pendampingan
    log("Module import_pendampingan berhasil di-import")
    
    # Jalankan main function
    log("Memanggil main()...")
    import_pendampingan.main()
    
    log("\nScript selesai!")
    
except Exception as e:
    log(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    log("\nTraceback:")
    for line in traceback.format_exc().split('\n'):
        log(line)
    sys.exit(1)
finally:
    output_file.close()
