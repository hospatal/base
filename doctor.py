import os
import spesialis 
import login 
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
file_dokter = os.path.join(script_dir, 'doctors.txt')

daftar_dokter = {}

def muat_dokter():
    """Memuat data dokter dari file doctors.txt ke dictionary daftar_dokter."""
    global daftar_dokter
    daftar_dokter.clear() 
    
    if os.path.exists(file_dokter):
        with open(file_dokter, 'r') as file:
            for baris in file:
                data = baris.strip().split(',')
                if len(data) >= 5: 
                    email = data[0]
                    nama = data[1]
                    id_spesial = data[2]
                    telepon = data[3]
                    alamat = data[4]
                    
                    daftar_dokter[email] = {
                        "nama": nama,
                        "id_spesial": id_spesial,
                        "telepon": telepon,
                        "alamat": alamat
                    }
    else:
        with open(file_dokter, 'w') as file:
            pass # Buat file kosong jika belum ada

def tampilkan_dokter():
    """Menampilkan semua data dokter yang tersimpan."""
    muat_dokter() 
    spesialis.muat_spesialisasi() 
    
    print(f"\n{Fore.CYAN}--- DAFTAR DOKTER ---{Style.RESET_ALL}")
    if not daftar_dokter:
        print(f"{Fore.YELLOW}Belum ada data dokter.{Style.RESET_ALL}")
    else:
        for email, dokter in daftar_dokter.items():
            nama_spesial = "Tidak diketahui"
            id_spesial = dokter['id_spesial']
            if id_spesial in spesialis.daftar_spesialisasi:
                nama_spesial = spesialis.daftar_spesialisasi[id_spesial]['nama']
            
            print(f"{Fore.GREEN}Email: {email}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Nama: {dokter['nama']}")
            print(f"Spesialisasi: {nama_spesial} (ID: {id_spesial})")
            print(f"Telepon: {dokter['telepon']}")  
            print(f"Alamat: {dokter['alamat']}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-' * 30}{Style.RESET_ALL}")

def tambah_dokter(): # Fungsi untuk Admin
    """Menambahkan data dokter baru dengan validasi terhadap data pengguna."""
    print(f"\n{Fore.CYAN}--- TAMBAH PROFIL DOKTER BARU (Admin) ---{Style.RESET_ALL}")
    
    email = input(f"{Fore.YELLOW}Masukkan Email dokter (harus sudah terdaftar sebagai pengguna 'dokter'): {Style.RESET_ALL}")
    
    login.load_users() 
    if email not in login.users:
        print(f"{Fore.RED}Email '{email}' tidak terdaftar dalam sistem pengguna.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Harap daftarkan pengguna dengan email ini dan peran 'dokter' terlebih dahulu melalui menu registrasi atau manajemen pengguna.{Style.RESET_ALL}")
        return
    if login.users[email]['role'] != 'dokter':
        print(f"{Fore.RED}Pengguna dengan email '{email}' terdaftar, tetapi perannya bukan 'dokter'. Peran saat ini: {login.users[email]['role']}.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Pastikan peran pengguna sudah benar di manajemen pengguna sebelum menambahkan profil dokter.{Style.RESET_ALL}")
        return
        
    muat_dokter() 
    if email in daftar_dokter:
        print(f"{Fore.RED}Profil detail untuk dokter dengan email '{email}' sudah ada.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Anda bisa mengeditnya melalui menu 'Edit Data Dokter'.{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}Email '{email}' valid dan terdaftar sebagai dokter. Silakan lengkapi detail profil:{Style.RESET_ALL}")
    nama = input(f"{Fore.YELLOW}Nama lengkap dokter: {Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Daftar Spesialisasi Tersedia:{Style.RESET_ALL}")
    spesialis.tampilkan_spesialisasi() 
    id_spesial = input(f"\n{Fore.YELLOW}Masukkan ID Spesialisasi: {Style.RESET_ALL}")
    
    spesialis.muat_spesialisasi() 
    if id_spesial not in spesialis.daftar_spesialisasi:
        print(f"{Fore.RED}ID Spesialisasi tidak valid!{Style.RESET_ALL}")
        return
    
    telepon = input(f"{Fore.YELLOW}Nomor telepon: {Style.RESET_ALL}")
    alamat = input(f"{Fore.YELLOW}Alamat: {Style.RESET_ALL}")
    
    try:
        with open(file_dokter, 'a') as file:
            file.write(f"{email},{nama},{id_spesial},{telepon},{alamat}\n")
        
        daftar_dokter[email] = {
            "nama": nama,
            "id_spesial": id_spesial,
            "telepon": telepon,
            "alamat": alamat
        }
        print(f"{Fore.GREEN}Profil dokter {nama} berhasil ditambahkan!{Style.RESET_ALL}")
    except IOError:
        print(f"{Fore.RED}Gagal menyimpan data dokter ke file.{Style.RESET_ALL}")

def _simpan_semua_dokter():
    """Menyimpan semua data dokter dari dictionary ke file (overwrite)."""
    try:
        with open(file_dokter, 'w') as file:
            for email, dok_data in daftar_dokter.items():
                file.write(f"{email},{dok_data['nama']},{dok_data['id_spesial']},{dok_data['telepon']},{dok_data['alamat']}\n")
        return True
    except IOError:
        print(f"{Fore.RED}Gagal menyimpan semua data dokter ke file.{Style.RESET_ALL}")
        return False

def edit_dokter(): # Fungsi untuk Admin
    """Mengedit data dokter yang sudah ada dengan validasi konsistensi."""
    print(f"\n{Fore.CYAN}--- EDIT DATA DOKTER (Admin) ---{Style.RESET_ALL}")
    
    tampilkan_dokter() 
    email_edit = input(f"\n{Fore.YELLOW}Masukkan email dokter yang akan diedit: {Style.RESET_ALL}")
    
    muat_dokter() 
    if email_edit not in daftar_dokter:
        print(f"{Fore.RED}Profil detail untuk dokter dengan email '{email_edit}' tidak ditemukan di daftar dokter.{Style.RESET_ALL}")
        return

    login.load_users() 
    if email_edit not in login.users:
        print(f"{Fore.RED}PERINGATAN KERAS: Email '{email_edit}' ada di profil dokter, tetapi TIDAK terdaftar di sistem pengguna utama!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ini menandakan inkonsistensi data. Sebaiknya perbaiki data pengguna atau hapus profil dokter ini jika pengguna sudah tidak ada.{Style.RESET_ALL}")
        return 
    if login.users[email_edit]['role'] != 'dokter':
        print(f"{Fore.RED}PERINGATAN: Pengguna dengan email '{email_edit}' terdaftar, tetapi perannya BUKAN 'dokter' (Peran saat ini: {login.users[email_edit]['role']}).{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ini bisa menyebabkan masalah. Sebaiknya perbaiki peran pengguna di manajemen pengguna sebelum melanjutkan edit profil dokter.{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}Data pengguna untuk '{email_edit}' konsisten. Lanjutkan mengedit profil dokter.{Style.RESET_ALL}")
    dokter_lama = daftar_dokter[email_edit]
    print(f"\n{Fore.CYAN}Data Lama Dokter ({email_edit}):{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Nama: {dokter_lama['nama']}")
    spesialis.muat_spesialisasi()
    nama_spesial_lama = spesialis.daftar_spesialisasi.get(dokter_lama['id_spesial'], {}).get('nama', 'Tidak diketahui')
    print(f"Spesialisasi: {nama_spesial_lama} (ID: {dokter_lama['id_spesial']})")
    print(f"Telepon: {dokter_lama['telepon']}")
    print(f"Alamat: {dokter_lama['alamat']}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Masukkan data baru (kosongkan jika tidak ingin diubah){Style.RESET_ALL}")
    nama_baru = input(f"{Fore.YELLOW}Nama baru: {Style.RESET_ALL}") or dokter_lama['nama']
    
    print(f"\n{Fore.CYAN}Daftar Spesialisasi Tersedia:{Style.RESET_ALL}")
    spesialis.tampilkan_spesialisasi()
    id_spesial_baru_input = input(f"\n{Fore.YELLOW}ID Spesialisasi baru: {Style.RESET_ALL}")
    id_spesial_baru = dokter_lama['id_spesial'] 
    if id_spesial_baru_input:
        if id_spesial_baru_input not in spesialis.daftar_spesialisasi:
            print(f"{Fore.RED}ID Spesialisasi baru tidak valid! Spesialisasi tidak diubah.{Style.RESET_ALL}")
        else:
            id_spesial_baru = id_spesial_baru_input
            
    telepon_baru = input(f"{Fore.YELLOW}Telepon baru: {Style.RESET_ALL}") or dokter_lama['telepon']
    alamat_baru = input(f"{Fore.YELLOW}Alamat baru: {Style.RESET_ALL}") or dokter_lama['alamat']
    
    daftar_dokter[email_edit] = {
        "nama": nama_baru,
        "id_spesial": id_spesial_baru,
        "telepon": telepon_baru,
        "alamat": alamat_baru
    }
    
    if _simpan_semua_dokter():
        print(f"{Fore.GREEN}Data dokter berhasil diubah!{Style.RESET_ALL}")
    else:
        muat_dokter()

def edit_own_profile(email_dokter_login): 
    """Memungkinkan dokter yang sedang login untuk mengedit profilnya sendiri."""
    print(f"\n{Fore.CYAN}--- EDIT PROFIL SAYA ---{Style.RESET_ALL}")
    
    muat_dokter() 
    
    if email_dokter_login not in daftar_dokter:
        print(f"{Fore.RED}Profil detail Anda belum dibuat oleh Admin. Silakan hubungi Admin.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Admin dapat menambahkan detail Anda melalui menu Manajemen Dokter -> Tambah Dokter Baru, menggunakan email Anda: {email_dokter_login}{Style.RESET_ALL}")
        return

    dokter_lama = daftar_dokter[email_dokter_login]
    print(f"\n{Fore.CYAN}Data Profil Anda Saat Ini:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Nama: {dokter_lama['nama']}")
    
    spesialis.muat_spesialisasi() 
    nama_spesial_lama = "Tidak diketahui"
    if dokter_lama['id_spesial'] in spesialis.daftar_spesialisasi:
        nama_spesial_lama = spesialis.daftar_spesialisasi[dokter_lama['id_spesial']]['nama']
    print(f"Spesialisasi: {nama_spesial_lama} (ID: {dokter_lama['id_spesial']})")
    print(f"Telepon: {dokter_lama['telepon']}")
    print(f"Alamat: {dokter_lama['alamat']}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Masukkan data baru (kosongkan jika tidak ingin diubah){Style.RESET_ALL}")
    
    nama_baru = input(f"{Fore.YELLOW}Nama baru (Nama saat ini: {dokter_lama['nama']}): {Style.RESET_ALL}") or dokter_lama['nama']
    
    print(f"\n{Fore.CYAN}Daftar Spesialisasi Tersedia:{Style.RESET_ALL}")
    spesialis.tampilkan_spesialisasi() 
    
    id_spesial_baru_input = input(f"\n{Fore.YELLOW}ID Spesialisasi baru (ID saat ini: {dokter_lama['id_spesial']}): {Style.RESET_ALL}")
    id_spesial_baru = dokter_lama['id_spesial'] 
    
    if id_spesial_baru_input: 
        if id_spesial_baru_input not in spesialis.daftar_spesialisasi:
            print(f"{Fore.RED}ID Spesialisasi baru tidak valid! Spesialisasi tidak diubah, menggunakan ID lama ({dokter_lama['id_spesial']}).{Style.RESET_ALL}")
        else:
            id_spesial_baru = id_spesial_baru_input 
            
    telepon_baru = input(f"{Fore.YELLOW}Telepon baru (Telepon saat ini: {dokter_lama['telepon']}): {Style.RESET_ALL}") or dokter_lama['telepon']
    alamat_baru = input(f"{Fore.YELLOW}Alamat baru (Alamat saat ini: {dokter_lama['alamat']}): {Style.RESET_ALL}") or dokter_lama['alamat']
    
    daftar_dokter[email_dokter_login] = {
        "nama": nama_baru,
        "id_spesial": id_spesial_baru,
        "telepon": telepon_baru,
        "alamat": alamat_baru
    }
    
    if _simpan_semua_dokter():
        print(f"{Fore.GREEN}Profil Anda berhasil diperbarui!{Style.RESET_ALL}")
    else:
        muat_dokter()

def hapus_dokter(): # Fungsi untuk Admin
    """Menghapus data dokter (biasanya dilakukan oleh Admin)."""
    print(f"\n{Fore.CYAN}--- HAPUS PROFIL DOKTER (Admin) ---{Style.RESET_ALL}")
    
    tampilkan_dokter() 
    email_hapus = input(f"\n{Fore.YELLOW}Masukkan email dokter yang profilnya akan dihapus: {Style.RESET_ALL}")
    
    muat_dokter() 
    if email_hapus not in daftar_dokter:
        print(f"{Fore.RED}Email dokter tidak ditemukan di daftar profil dokter!{Style.RESET_ALL}")
        return
    
    nama_dokter = daftar_dokter[email_hapus]['nama']
    konfirmasi = input(f"{Fore.RED}Yakin ingin menghapus profil detail dokter {nama_dokter} ({email_hapus})? \n(Ini hanya menghapus profil dari daftar dokter, bukan akun pengguna). (y/n): {Style.RESET_ALL}")
    
    if konfirmasi.lower() != 'y':
        print(f"{Fore.YELLOW}Penghapusan profil dokter dibatalkan.{Style.RESET_ALL}")
        return
    
    del daftar_dokter[email_hapus]
    
    if _simpan_semua_dokter():
        print(f"{Fore.GREEN}Profil dokter {nama_dokter} berhasil dihapus.{Style.RESET_ALL}")
    else:
        muat_dokter() 

def cari_dokter_spesialisasi():
    print(f"\n{Fore.CYAN}--- CARI DOKTER BERDASARKAN SPESIALISASI ---{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Daftar Spesialisasi Tersedia:{Style.RESET_ALL}")
    spesialis.tampilkan_spesialisasi()
    id_spesial_cari = input(f"\n{Fore.YELLOW}Masukkan ID spesialisasi yang dicari: {Style.RESET_ALL}")
    
    spesialis.muat_spesialisasi()
    if id_spesial_cari not in spesialis.daftar_spesialisasi:
        print(f"{Fore.RED}ID Spesialisasi tidak valid!{Style.RESET_ALL}")
        return
    
    muat_dokter()
    nama_spesial_dicari = spesialis.daftar_spesialisasi[id_spesial_cari]['nama']
    print(f"\n{Fore.CYAN}Dokter dengan spesialisasi '{nama_spesial_dicari}':{Style.RESET_ALL}")
    
    ketemu = False
    for email, dokter in daftar_dokter.items():
        if dokter['id_spesial'] == id_spesial_cari:
            print(f"\n{Fore.GREEN}Email: {email}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Nama: {dokter['nama']}")
            print(f"Telepon: {dokter['telepon']}")
            print(f"Alamat: {dokter['alamat']}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-' * 30}{Style.RESET_ALL}")
            ketemu = True
    
    if not ketemu:
        print(f"{Fore.RED}Tidak ditemukan dokter dengan spesialisasi '{nama_spesial_dicari}'.{Style.RESET_ALL}")


def cari_dokter_nama():
    print(f"\n{Fore.CYAN}--- CARI DOKTER BERDASARKAN NAMA ---{Style.RESET_ALL}")
    
    kata_kunci = input(f"{Fore.YELLOW}Masukkan nama dokter (sebagian kata juga bisa): {Style.RESET_ALL}").lower()
    
    muat_dokter()
    spesialis.muat_spesialisasi()
    
    print(f"\n{Fore.CYAN}Hasil pencarian untuk '{kata_kunci}':{Style.RESET_ALL}")
    ketemu = False
    for email, dokter in daftar_dokter.items():
        if kata_kunci in dokter['nama'].lower():
            nama_spesial = "Tidak diketahui"
            id_spesial = dokter['id_spesial']
            if id_spesial in spesialis.daftar_spesialisasi:
                nama_spesial = spesialis.daftar_spesialisasi[id_spesial]['nama']
                
            print(f"\n{Fore.GREEN}Email: {email}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Nama: {dokter['nama']}")
            print(f"Spesialisasi: {nama_spesial} (ID: {id_spesial})")
            print(f"Telepon: {dokter['telepon']}")
            print(f"Alamat: {dokter['alamat']}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-' * 30}{Style.RESET_ALL}")
            ketemu = True
    
    if not ketemu:
        print(f"{Fore.RED}Tidak ditemukan dokter dengan nama yang mengandung '{kata_kunci}'.{Style.RESET_ALL}")

def menu_dokter(): # Menu untuk Admin
    """Menu utama untuk manajemen data dokter (biasanya diakses oleh Admin)."""
    while True:
        print(f"\n{Fore.CYAN}")
        banner = pyfiglet.figlet_format("DATA DOKTER", font="small")
        print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}========== MENU DOKTER (Admin) =========={Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Daftar Dokter")
        print(f"2. Tambah Profil Dokter Baru") 
        print(f"3. Edit Data Dokter")
        print(f"4. Hapus Profil Dokter")      
        print(f"5. Cari Dokter berdasarkan Spesialisasi")
        print(f"6. Cari Dokter berdasarkan Nama")
        print(f"{Fore.RED}0. Kembali ke Menu Admin Utama{Style.RESET_ALL}")
        
        pilihan = input(f"{Fore.GREEN}Pilih menu (0-6): {Style.RESET_ALL}")
        
        if pilihan == "1":
            tampilkan_dokter()
        elif pilihan == "2":
            tambah_dokter()
        elif pilihan == "3":
            edit_dokter()
        elif pilihan == "4":
            hapus_dokter()
        elif pilihan == "5":
            cari_dokter_spesialisasi()
        elif pilihan == "6":
            cari_dokter_nama()
        elif pilihan == "0":
            print(f"{Fore.YELLOW}Kembali ke menu admin utama...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid! Coba lagi.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")


if __name__ == "__main__":
    print(f"{Fore.MAGENTA}Modul doctor.py dijalankan secara standalone untuk testing.{Style.RESET_ALL}")
    menu_dokter()