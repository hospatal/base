import os
from colorama import Fore, Back, Style, init
import pyfiglet

init(autoreset=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
file_spesialisasi = os.path.join(script_dir, 'specializations.txt')

# Dictionary untuk menyimpan data spesialisasi sementara
daftar_spesialisasi = {}

# Fungsi untuk memuat data dari file
def muat_spesialisasi():
    global daftar_spesialisasi
    daftar_spesialisasi.clear()
    
    if os.path.exists(file_spesialisasi):
        with open(file_spesialisasi, 'r') as file:
            for baris in file:
                data = baris.strip().split(',')
                if len(data) >= 3:
                    id_spesial = data[0]
                    nama = data[1]
                    deskripsi = data[2]
                    daftar_spesialisasi[id_spesial] = {
                        "nama": nama,
                        "deskripsi": deskripsi
                    }
    else:
        # Buat file baru dengan data default jika tidak ada
        with open(file_spesialisasi, 'w') as file:
            file.write("1,Umum,Dokter untuk penanganan penyakit umum\n")
        # Tambahkan data default ke dictionary
        daftar_spesialisasi["1"] = {
            "nama": "Umum",
            "deskripsi": "Dokter untuk penanganan penyakit umum"
        }

# Fungsi untuk menampilkan semua spesialisasi
def tampilkan_spesialisasi():
    muat_spesialisasi()
    
    print(f"\n{Fore.CYAN}--- DAFTAR SPESIALISASI ---{Style.RESET_ALL}")
    if not daftar_spesialisasi:
        print(f"{Fore.YELLOW}Belum ada data spesialisasi.{Style.RESET_ALL}")
    else:
        for id_spesial, spesial in daftar_spesialisasi.items():
            print(f"{Fore.GREEN}{id_spesial}. {spesial['nama']}{Style.RESET_ALL} - {spesial['deskripsi']}")

# Fungsi untuk mencari ID tertinggi berikutnya
def cari_id_terakhir():
    muat_spesialisasi() # Pastikan data termuat
    id_tertinggi = 0
    if not daftar_spesialisasi: # Jika kosong, mulai dari 0
        return 1
    for id_spesial in daftar_spesialisasi.keys():
        try:
            if int(id_spesial) > id_tertinggi:
                id_tertinggi = int(id_spesial)
        except ValueError:
            continue # Abaikan ID yang tidak valid
    return id_tertinggi + 1

# Fungsi untuk menambah spesialisasi baru
def tambah_spesialisasi():
    print(f"\n{Fore.CYAN}--- TAMBAH SPESIALISASI BARU ---{Style.RESET_ALL}")
    
    nama = input(f"{Fore.YELLOW}Masukkan nama spesialisasi: {Style.RESET_ALL}")
    deskripsi = input(f"{Fore.YELLOW}Masukkan deskripsi: {Style.RESET_ALL}")
    
    id_baru = str(cari_id_terakhir())
    
    # Tambahkan ke dictionary dulu
    daftar_spesialisasi[id_baru] = {"nama": nama, "deskripsi": deskripsi}
    # Tulis ke file (mode append)
    try:
        with open(file_spesialisasi, 'a') as file:
            file.write(f"{id_baru},{nama},{deskripsi}\n")
        print(f"{Fore.GREEN}Spesialisasi '{nama}' berhasil ditambahkan dengan ID {id_baru}.{Style.RESET_ALL}")
    except IOError:
        print(f"{Fore.RED}Gagal menyimpan spesialisasi ke file.{Style.RESET_ALL}")
        muat_spesialisasi() # Rollback in-memory by reloading from file


# Fungsi untuk mencari spesialisasi berdasarkan nama
def cari_spesialisasi_nama():
    print(f"\n{Fore.CYAN}--- CARI SPESIALISASI ---{Style.RESET_ALL}")
    kata_kunci = input(f"{Fore.YELLOW}Masukkan kata kunci nama: {Style.RESET_ALL}").lower()
    
    muat_spesialisasi()
    
    print(f"\n{Fore.CYAN}Hasil pencarian untuk '{kata_kunci}':{Style.RESET_ALL}")
    ketemu = False
    for id_spesial, spesial in daftar_spesialisasi.items():
        if kata_kunci in spesial['nama'].lower():
            print(f"{Fore.GREEN}{id_spesial}. {spesial['nama']}{Style.RESET_ALL} - {spesial['deskripsi']}")
            ketemu = True
    
    if not ketemu:
        print(f"{Fore.RED}Tidak ditemukan spesialisasi yang sesuai.{Style.RESET_ALL}")

# Fungsi internal untuk menyimpan semua spesialisasi ke file (overwrite)
def _simpan_semua_spesialisasi():
    try:
        with open(file_spesialisasi, 'w') as file:
            for id_spesial, data in daftar_spesialisasi.items():
                file.write(f"{id_spesial},{data['nama']},{data['deskripsi']}\n")
        return True
    except IOError:
        print(f"{Fore.RED}Gagal menyimpan semua spesialisasi ke file.{Style.RESET_ALL}")
        return False

# Fungsi untuk mengedit spesialisasi
def edit_spesialisasi():
    print(f"\n{Fore.CYAN}--- EDIT SPESIALISASI ---{Style.RESET_ALL}")
    tampilkan_spesialisasi()
    
    id_edit = input(f"\n{Fore.YELLOW}Masukkan ID spesialisasi yang akan diedit: {Style.RESET_ALL}")
    
    muat_spesialisasi() # Pastikan data terbaru
    if id_edit not in daftar_spesialisasi:
        print(f"{Fore.RED}ID tidak ditemukan!{Style.RESET_ALL}")
        return
    
    data_lama = daftar_spesialisasi[id_edit]
    print(f"{Fore.BLUE}Data lama: {data_lama['nama']} - {data_lama['deskripsi']}{Style.RESET_ALL}")
    nama_baru = input(f"{Fore.YELLOW}Nama baru (kosongkan jika tidak diubah): {Style.RESET_ALL}") or data_lama['nama']
    desk_baru = input(f"{Fore.YELLOW}Deskripsi baru (kosongkan jika tidak diubah): {Style.RESET_ALL}") or data_lama['deskripsi']
    
    # Update di memori
    daftar_spesialisasi[id_edit] = {"nama": nama_baru, "deskripsi": desk_baru}
    
    if _simpan_semua_spesialisasi():
        print(f"{Fore.GREEN}Data spesialisasi berhasil diubah!{Style.RESET_ALL}")
    else:
        muat_spesialisasi() # Rollback jika gagal simpan

# Fungsi untuk menghapus spesialisasi
def hapus_spesialisasi():
    print(f"\n{Fore.CYAN}--- HAPUS SPESIALISASI ---{Style.RESET_ALL}")
    tampilkan_spesialisasi()
    
    id_hapus = input(f"\n{Fore.YELLOW}Masukkan ID spesialisasi yang akan dihapus: {Style.RESET_ALL}")
    
    muat_spesialisasi()
    if id_hapus not in daftar_spesialisasi:
        print(f"{Fore.RED}ID tidak ditemukan!{Style.RESET_ALL}")
        return
    
    nama_spesial = daftar_spesialisasi[id_hapus]['nama']
    # PERINGATAN: Tambahkan pengecekan apakah spesialisasi ini digunakan oleh dokter
    # Jika iya, mungkin tidak boleh dihapus atau berikan peringatan lebih lanjut.
    # Untuk saat ini, kita lanjutkan dengan konfirmasi sederhana.
    konfirmasi = input(f"{Fore.RED}Yakin hapus spesialisasi '{nama_spesial}' (ID: {id_hapus})? (y/n): {Style.RESET_ALL}")
    
    if konfirmasi.lower() != 'y':
        print(f"{Fore.YELLOW}Penghapusan dibatalkan.{Style.RESET_ALL}")
        return
    
    # Hapus dari memori
    del daftar_spesialisasi[id_hapus]
    
    if _simpan_semua_spesialisasi():
        print(f"{Fore.GREEN}Spesialisasi '{nama_spesial}' berhasil dihapus.{Style.RESET_ALL}")
    else:
        muat_spesialisasi() # Rollback jika gagal simpan

# Fungsi menu spesialisasi
def menu_spesialisasi():
    while True:
        print(f"\n{Fore.CYAN}")
        banner = pyfiglet.figlet_format("SPESIALISASI", font="small")
        print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}========== MENU SPESIALISASI =========={Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Daftar Spesialisasi")
        print(f"2. Tambah Spesialisasi Baru")
        print(f"3. Edit Spesialisasi")
        print(f"4. Hapus Spesialisasi")
        print(f"5. Cari Spesialisasi")
        print(f"{Fore.RED}0. Kembali ke Menu Admin Utama{Style.RESET_ALL}") # Diubah dari EXIT
        
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
            print(f"{Fore.YELLOW}Kembali ke menu admin utama...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid!{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}") # Tambah pause

if __name__ == "__main__":
    menu_spesialisasi()