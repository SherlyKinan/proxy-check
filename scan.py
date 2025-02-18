import socket
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# File input yang berisi daftar IP dan port
file_input = "proxy.txt"

def Cek_proxy(ip, port, timeout=3):
    """Memeriksa koneksi IP dan PORT menggunakan socket"""
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False

def Clear_file(filepath):
    """Menghapus isi file sebelum menulis data baru"""
    open(filepath, 'w').close()  # Buka file dengan 'w' untuk mengosongkannya

def Save_to_file(filepath, data, cache):
    """Simpan data ke file tanpa duplikasi"""
    if data not in cache:
        with open(filepath, 'a') as f:
            f.write(data + '\n')
        cache.add(data)  # Tambahkan ke cache untuk mencegah duplikasi

def Cek_ip_port(line, save_path, active_cache, dead_cache):
    """Cek apakah proxy aktif atau tidak, lalu simpan hasilnya"""
    parts = line.strip().split(',')
    if len(parts) >= 2:
        ip_address = parts[0]
        try:
            port_number = int(parts[1])
        except ValueError:
            print(f"[ERROR] Port tidak valid : {parts[1]}")
            return
        
        country = parts[2] if len(parts) > 2 else "Unknown"
        organization = parts[3] if len(parts) > 3 else "Unknown"
        
        result = f"{ip_address},{port_number},{country},{organization}"
        
        if Cek_proxy(ip_address, port_number):
            Save_to_file(os.path.join(save_path, "active.txt"), result, active_cache)
            print(f"[AKTIF] {result} ")
        else:
            Save_to_file(os.path.join(save_path, "dead.txt"), result, dead_cache)
            print(f"[TIDAK AKTIF] {result}")

def Read_ip_port(filename, max_workers=100):
    """Baca IP dan port dari file, lalu cek statusnya dengan thread pool"""
    save_path = os.path.dirname(filename)  # Ambil folder dari file_input

    # Hapus isi file sebelum mulai
    Clear_file(os.path.join(save_path, "active.txt"))
    Clear_file(os.path.join(save_path, "dead.txt"))

    # Cache untuk mencegah duplikasi
    active_cache = set()
    dead_cache = set()

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(Cek_ip_port, line, save_path, active_cache, dead_cache) for line in lines]
            for future in as_completed(futures):
                future.result()  # Pastikan setiap tugas selesai

    except FileNotFoundError:
        print(f"File '{filename}' tidak ditemukan.")
    except ValueError:
        print("Format data salah. Pastikan IP dan port dipisah dengan koma.")

# Jalankan pengecekan proxy
Read_ip_port(file_input)
