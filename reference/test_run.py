#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script untuk debugging"""

import sys
import os

print("Starting test...")
sys.stdout.flush()

# Test 1: JSON file exists
json_file = "Data Pendamping_28102025.json"
if os.path.exists(json_file):
    print(f"✓ JSON file found: {json_file}")
    file_size = os.path.getsize(json_file) / (1024 * 1024)  # MB
    print(f"  File size: {file_size:.2f} MB")
else:
    print(f"✗ JSON file NOT found: {json_file}")
    sys.exit(1)

# Test 2: Database connection
try:
    import psycopg2
    print("✓ psycopg2 imported")
    
    # Try to connect
    db_config = {
        'host': os.getenv('PGHOST', 'localhost'),
        'port': os.getenv('PGPORT', '5432'),
        'dbname': os.getenv('PGDATABASE', 'gokendali_dev'),
        'user': os.getenv('PGUSER', 'postgres'),
        'password': os.getenv('PGPASSWORD', '')
    }
    
    print(f"  Connecting to: {db_config['host']}:{db_config['port']}/{db_config['dbname']} as {db_config['user']}")
    conn = psycopg2.connect(**db_config)
    print("✓ Database connection successful")
    conn.close()
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    sys.exit(1)

# Test 3: Import main script
try:
    import import_pendampingan
    print("✓ import_pendampingan module loaded")
except Exception as e:
    print(f"✗ Failed to import module: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nAll tests passed! Ready to run main script.")
sys.stdout.flush()
