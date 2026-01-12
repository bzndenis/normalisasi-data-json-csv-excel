import json
import re

def normalisasi_email(email):
    """
    Menghapus semua spasi dari email dan melengkapi email yang tidak lengkap
    """
    if email and isinstance(email, str):
        # Hapus semua spasi dari email
        email_normalized = email.replace(" ", "")
        
        # Perbaiki email yang tidak lengkap (cek SEBELUM menghapus titik di akhir)
        # Kasus 1: @gmail.co -> @gmail.com
        if email_normalized.endswith('@gmail.co'):
            email_normalized = email_normalized + 'm'
        
        # Kasus 2: @gmail. -> @gmail.com
        elif email_normalized.endswith('@gmail.'):
            email_normalized = email_normalized + 'com'
        
        # Kasus 3: @yahoo.co -> @yahoo.com
        elif email_normalized.endswith('@yahoo.co'):
            email_normalized = email_normalized + 'm'
        
        # Kasus 4: @yahoo. -> @yahoo.com
        elif email_normalized.endswith('@yahoo.'):
            email_normalized = email_normalized + 'com'
        
        # Kasus 5: @hotmail.co -> @hotmail.com
        elif email_normalized.endswith('@hotmail.co'):
            email_normalized = email_normalized + 'm'
        
        # Kasus 6: @hotmail. -> @hotmail.com
        elif email_normalized.endswith('@hotmail.'):
            email_normalized = email_normalized + 'com'
        
        # Kasus 7: Domain lain yang berakhir dengan .co (umumnya .com)
        elif '@' in email_normalized and email_normalized.endswith('.co') and not email_normalized.endswith('.com'):
            # Cek apakah ini domain yang umumnya .com
            domain = email_normalized.split('@')[1].split('.')[0].lower()
            # Domain umum yang biasanya .com
            common_domains = ['gmail', 'yahoo', 'hotmail', 'outlook', 'live', 'msn', 'aol']
            if domain in common_domains:
                email_normalized = email_normalized + 'm'
        
        # Kasus 8: Domain lain yang berakhir dengan . (umumnya .com)
        elif '@' in email_normalized and email_normalized.endswith('.'):
            domain = email_normalized.split('@')[1].rstrip('.').lower()
            # Domain umum yang biasanya .com
            common_domains = ['gmail', 'yahoo', 'hotmail', 'outlook', 'live', 'msn', 'aol']
            if domain in common_domains:
                email_normalized = email_normalized.rstrip('.') + 'com'
            else:
                # Untuk domain lain, tambahkan 'com' jika tidak ada ekstensi
                email_normalized = email_normalized.rstrip('.') + 'com'
        
        # Hapus titik di akhir jika ada (misal: email@gmail.com. -> email@gmail.com)
        # Lakukan SETELAH semua perbaikan di atas
        email_normalized = email_normalized.rstrip('.')
        
        return email_normalized
    return email

def perbaiki_email_di_json(file_path):
    """
    Membaca file JSON, memperbaiki email yang terpisah, dan menyimpan kembali
    """
    # Baca file JSON
    print(f"Membaca file: {file_path}")
    
    # Baca konten file sebagai string dulu
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Bersihkan karakter kontrol yang tidak valid (kecuali \n, \r, \t)
    # JSON tidak mengizinkan karakter kontrol kecuali yang disebutkan
    def clean_control_chars(text):
        result = []
        for char in text:
            # Izinkan karakter kontrol standar: \n, \r, \t
            if ord(char) < 32 and char not in '\n\r\t':
                continue
            result.append(char)
        return ''.join(result)
    
    content = clean_control_chars(content)
    
    # Cek apakah file sudah memiliki bracket array
    content_stripped = content.strip()
    if not content_stripped.startswith('['):
        # Tambahkan bracket pembuka jika belum ada
        content = '[' + content_stripped
    if not content_stripped.endswith(']'):
        # Tambahkan bracket penutup jika belum ada
        if not content.endswith(']'):
            content = content.rstrip() + '\n]'
    
    # Parse JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        # Coba perbaiki dengan menghapus koma trailing di akhir
        content = content.rstrip().rstrip(',').rstrip() + '\n]'
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e2:
            print(f"Error parsing JSON setelah perbaikan: {e2}")
            raise
    
    # Hitung jumlah email yang diperbaiki
    jumlah_perbaikan = 0
    total_email = 0
    
    # Proses setiap item dalam array
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "EMAIL" in item:
                total_email += 1
                email_lama = item["EMAIL"]
                email_baru = normalisasi_email(email_lama)
                
                if email_lama != email_baru:
                    print(f"Memperbaiki: '{email_lama}' -> '{email_baru}'")
                    item["EMAIL"] = email_baru
                    jumlah_perbaikan += 1
    elif isinstance(data, dict):
        # Jika data adalah single object
        if "EMAIL" in data:
            total_email += 1
            email_lama = data["EMAIL"]
            email_baru = normalisasi_email(email_lama)
            
            if email_lama != email_baru:
                print(f"Memperbaiki: '{email_lama}' -> '{email_baru}'")
                data["EMAIL"] = email_baru
                jumlah_perbaikan += 1
    
    # Simpan kembali ke file
    print(f"\nMenyimpan file yang sudah diperbaiki...")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    
    # Hapus bracket array jika file aslinya tidak memilikinya
    # (opsional - jika ingin mempertahankan format asli)
    # Tapi untuk konsistensi, kita biarkan dengan bracket array
    
    print(f"\nSelesai!")
    print(f"Total email ditemukan: {total_email}")
    print(f"Email yang diperbaiki: {jumlah_perbaikan}")
    
    return jumlah_perbaikan

if __name__ == "__main__":
    file_path = "Data Pendamping_28102025.json"
    
    try:
        perbaiki_email_di_json(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan!")
    except json.JSONDecodeError as e:
        print(f"Error: File JSON tidak valid - {e}")
    except Exception as e:
        print(f"Error: {e}")

