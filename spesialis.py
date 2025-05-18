import os
# Import colorama untuk warna
from colorama import Fore, Back, Style, init
# Import pyfiglet untuk teks banner
import pyfiglet

# Initialize colorama
init(autoreset=True)

# File untuk menyimpan data spesialisasi
file_spesialisasi = 'specializations.txt'

# Dictionary untuk menyimpan data spesialisasi sementara
daftar_spesialisasi = {}

# Fungsi untuk memuat data dari file
def muat_spesialisasi():
    # Hapus data lama
    daftar_spesialisasi.clear()
    
    # Cek apakah file ada
    if os.path.exists(file_spesialisasi):
        # Baca file
        file = open(file_spesialisasi, 'r')
        for baris in file:
            # Pisahkan data berdasarkan koma
            data = baris.strip().split(',')
            if len(data) >= 3:
                id_spesial = data[0]
                nama = data[1]
                deskripsi = data[2]
                # Simpan ke dictionary
                daftar_spesialisasi[id_spesial] = {
                    "nama": nama,
                    "deskripsi": deskripsi
                }
        file.close()
    else:
        # Buat file baru dengan data default
        file = open(file_spesialisasi, 'w')
        file.write("1,Umum,Dokter untuk penanganan penyakit umum\n")
        file.close()
        # Tambahkan data default ke dictionary
        daftar_spesialisasi["1"] = {
            "nama": "Umum",
            "deskripsi": "Dokter untuk penanganan penyakit umum"
        }

# Fungsi untuk menampilkan semua spesialisasi
def tampilkan_spesialisasi():
    # Muat data terbaru
    muat_spesialisasi()
    
    print(f"\n{Fore.CYAN}--- DAFTAR SPESIALISASI ---{Style.RESET_ALL}")
    if len(daftar_spesialisasi) == 0:
        print(f"{Fore.YELLOW}Belum ada data spesialisasi{Style.RESET_ALL}")
    else:
        for id_spesial in daftar_spesialisasi:
            spesial = daftar_spesialisasi[id_spesial]
            print(f"{Fore.GREEN}{id_spesial}. {spesial['nama']}{Style.RESET_ALL} - {spesial['deskripsi']}")

# Fungsi untuk mencari ID tertinggi
def cari_id_terakhir():
    id_tertinggi = 0
    for id_spesial in daftar_spesialisasi:
        if int(id_spesial) > id_tertinggi:
            id_tertinggi = int(id_spesial)
    return id_tertinggi + 1

# Fungsi untuk menambah spesialisasi baru
def tambah_spesialisasi():
    print(f"\n{Fore.CYAN}--- TAMBAH SPESIALISASI BARU ---{Style.RESET_ALL}")
    
    # Input data baru
    nama = input(f"{Fore.YELLOW}Masukkan nama spesialisasi: {Style.RESET_ALL}")
    deskripsi = input(f"{Fore.YELLOW}Masukkan deskripsi: {Style.RESET_ALL}")
    
    # Cari ID baru
    muat_spesialisasi()
    id_baru = str(cari_id_terakhir())
    
    # Tulis ke file
    file = open(file_spesialisasi, 'a')
    file.write(f"{id_baru},{nama},{deskripsi}\n")
    file.close()
    
    print(f"{Fore.GREEN}Spesialisasi {nama} berhasil ditambahkan dengan ID {id_baru}{Style.RESET_ALL}")

# Fungsi untuk mencari spesialisasi berdasarkan nama
def cari_spesialisasi_nama():
    print(f"\n{Fore.CYAN}--- CARI SPESIALISASI ---{Style.RESET_ALL}")
    kata_kunci = input(f"{Fore.YELLOW}Masukkan kata kunci nama: {Style.RESET_ALL}").lower()
    
    # Muat data terbaru
    muat_spesialisasi()
    
    # Cari yang cocok
    print(f"\n{Fore.CYAN}Hasil pencarian:{Style.RESET_ALL}")
    ketemu = False
    for id_spesial in daftar_spesialisasi:
        spesial = daftar_spesialisasi[id_spesial]
        if kata_kunci in spesial['nama'].lower():
            print(f"{Fore.GREEN}{id_spesial}. {spesial['nama']}{Style.RESET_ALL} - {spesial['deskripsi']}")
            ketemu = True
    
    if not ketemu:
        print(f"{Fore.RED}Tidak ditemukan spesialisasi yang sesuai{Style.RESET_ALL}")

# Fungsi untuk mengedit spesialisasi
def edit_spesialisasi():
    print(f"\n{Fore.CYAN}--- EDIT SPESIALISASI ---{Style.RESET_ALL}")
    
    # Tampilkan daftar
    tampilkan_spesialisasi()
    
    # Input ID yang mau diedit
    id_edit = input(f"\n{Fore.YELLOW}Masukkan ID yang akan diedit: {Style.RESET_ALL}")
    
    # Cek apakah ID ada
    muat_spesialisasi()
    if id_edit not in daftar_spesialisasi:
        print(f"{Fore.RED}ID tidak ditemukan!{Style.RESET_ALL}")
        return
    
    # Input data baru
    print(f"{Fore.BLUE}Data lama: {daftar_spesialisasi[id_edit]['nama']} - {daftar_spesialisasi[id_edit]['deskripsi']}{Style.RESET_ALL}")
    nama_baru = input(f"{Fore.YELLOW}Nama baru (kosongkan jika tidak diubah): {Style.RESET_ALL}")
    desk_baru = input(f"{Fore.YELLOW}Deskripsi baru (kosongkan jika tidak diubah): {Style.RESET_ALL}")
    
    # Jika input kosong, pakai data lama
    if nama_baru == "":
        nama_baru = daftar_spesialisasi[id_edit]['nama']
    if desk_baru == "":
        desk_baru = daftar_spesialisasi[id_edit]['deskripsi']
    
    # Simpan semua data ke file
    file = open(file_spesialisasi, 'w')
    for id_spesial in daftar_spesialisasi:
        if id_spesial == id_edit:
            # Tulis data yang diedit
            file.write(f"{id_spesial},{nama_baru},{desk_baru}\n")
            # Update dictionary
            daftar_spesialisasi[id_spesial]['nama'] = nama_baru
            daftar_spesialisasi[id_spesial]['deskripsi'] = desk_baru
        else:
            # Tulis data lainnya tanpa perubahan
            spesial = daftar_spesialisasi[id_spesial]
            file.write(f"{id_spesial},{spesial['nama']},{spesial['deskripsi']}\n")
    file.close()
    
    print(f"{Fore.GREEN}Data spesialisasi berhasil diubah!{Style.RESET_ALL}")

# Fungsi untuk menghapus spesialisasi
def hapus_spesialisasi():
    print(f"\n{Fore.CYAN}--- HAPUS SPESIALISASI ---{Style.RESET_ALL}")
    
    # Tampilkan daftar
    tampilkan_spesialisasi()
    
    # Input ID yang mau dihapus
    id_hapus = input(f"\n{Fore.YELLOW}Masukkan ID yang akan dihapus: {Style.RESET_ALL}")
    
    # Cek apakah ID ada
    muat_spesialisasi()
    if id_hapus not in daftar_spesialisasi:
        print(f"{Fore.RED}ID tidak ditemukan!{Style.RESET_ALL}")
        return
    
    # Konfirmasi hapus
    nama_spesial = daftar_spesialisasi[id_hapus]['nama']
    konfirmasi = input(f"{Fore.RED}Yakin hapus spesialisasi '{nama_spesial}'? (y/n): {Style.RESET_ALL}")
    
    if konfirmasi.lower() != 'y':
        print(f"{Fore.YELLOW}Penghapusan dibatalkan{Style.RESET_ALL}")
        return
    
    # Simpan data selain yang dihapus ke file
    file = open(file_spesialisasi, 'w')
    for id_spesial in daftar_spesialisasi:
        if id_spesial != id_hapus:
            spesial = daftar_spesialisasi[id_spesial]
            file.write(f"{id_spesial},{spesial['nama']},{spesial['deskripsi']}\n")
    file.close()
    
    # Hapus dari dictionary
    del daftar_spesialisasi[id_hapus]
    print(f"{Fore.GREEN}Spesialisasi '{nama_spesial}' berhasil dihapus{Style.RESET_ALL}")

# Fungsi menu spesialisasi
def menu_spesialisasi():
    while True:
        # Tampilkan banner
        print(f"\n{Fore.CYAN}")
        banner = pyfiglet.figlet_format("SPESIALISASI", font="small")
        print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}========== MENU SPESIALISASI =========={Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Daftar Spesialisasi")
        print(f"2. Tambah Spesialisasi Baru")
        print(f"3. Edit Spesialisasi")
        print(f"4. Hapus Spesialisasi")
        print(f"5. Cari Spesialisasi")
        print(f"{Fore.RED}0. EXIT{Style.RESET_ALL}")
        
        pilihan = input(f"{Fore.MAGENTA}Pilih menu (0-5): {Style.RESET_ALL}")
        
        if pilihan == "1":
            tampilkan_spesialisasi()
        elif pilihan == "2":
            tambah_spesialisasi()
        elif pilihan == "3":
            edit_spesialisasi()
        elif pilihan == "4":
            hapus_spesialisasi()
        elif pilihan == "5":
            cari_spesialisasi_nama()
        elif pilihan == "0":
            print(f"{Fore.YELLOW}Kembali ke menu utama...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid!{Style.RESET_ALL}")

# Jalankan program jika dieksekusi langsung
if __name__ == "__main__":
    menu_spesialisasi()