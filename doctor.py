import os
import spesialis

from colorama import Fore, Back, Style, init

import pyfiglet


init(autoreset=True)


file_dokter = 'doctors.txt'


daftar_dokter = {}


def muat_dokter():
    
    daftar_dokter.clear()
    
    
    if os.path.exists(file_dokter):
        
        file = open(file_dokter, 'r')
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
        file.close()
    else:
        
        file = open(file_dokter, 'w')
        file.close()


def tampilkan_dokter():
    
    muat_dokter()
    spesialis.muat_spesialisasi()
    
    print(f"\n{Fore.CYAN}--- DAFTAR DOKTER ---{Style.RESET_ALL}")
    if len(daftar_dokter) == 0:
        print(f"{Fore.YELLOW}Belum ada data dokter{Style.RESET_ALL}")
    else:
        for email in daftar_dokter:
            dokter = daftar_dokter[email]
            
            
            nama_spesial = "Tidak diketahui"
            id_spesial = dokter['id_spesial']
            if id_spesial in spesialis.daftar_spesialisasi:
                nama_spesial = spesialis.daftar_spesialisasi[id_spesial]['nama']
            
            print(f"{Fore.GREEN}Email: {email}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Nama: {dokter['nama']}")
            print(f"Spesialisasi: {nama_spesial}")
            print(f"Telepon: {dokter['telepon']}")  
            print(f"Alamat: {dokter['alamat']}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-' * 30}{Style.RESET_ALL}")


def tambah_dokter():
    print(f"\n{Fore.CYAN}--- TAMBAH DOKTER BARU ---{Style.RESET_ALL}")
    
    
    email = input(f"{Fore.YELLOW}Email dokter: {Style.RESET_ALL}")
    
    
    muat_dokter()
    if email in daftar_dokter:
        print(f"{Fore.RED}Email sudah terdaftar!{Style.RESET_ALL}")
        return
    
    nama = input(f"{Fore.YELLOW}Nama dokter: {Style.RESET_ALL}")
    
    
    print(f"\n{Fore.CYAN}Daftar Spesialisasi:{Style.RESET_ALL}")
    spesialis.tampilkan_spesialisasi()
    
    id_spesial = input(f"\n{Fore.YELLOW}ID Spesialisasi: {Style.RESET_ALL}")
    
    
    spesialis.muat_spesialisasi()
    if id_spesial not in spesialis.daftar_spesialisasi:
        print(f"{Fore.RED}ID Spesialisasi tidak valid!{Style.RESET_ALL}")
        return
    
    telepon = input(f"{Fore.YELLOW}Nomor telepon: {Style.RESET_ALL}")
    alamat = input(f"{Fore.YELLOW}Alamat: {Style.RESET_ALL}")
    
    
    file = open(file_dokter, 'a')
    file.write(f"{email},{nama},{id_spesial},{telepon},{alamat}\n")
    file.close()
    
    
    daftar_dokter[email] = {
        "nama": nama,
        "id_spesial": id_spesial,
        "telepon": telepon,
        "alamat": alamat
    }
    
    print(f"{Fore.GREEN}Dokter {nama} berhasil ditambahkan!{Style.RESET_ALL}")


def edit_dokter():
    print(f"\n{Fore.CYAN}--- EDIT DATA DOKTER ---{Style.RESET_ALL}")
    
    
    tampilkan_dokter()
    
    
    email = input(f"\n{Fore.YELLOW}Masukkan email dokter yang akan diedit: {Style.RESET_ALL}")
    
    
    muat_dokter()
    if email not in daftar_dokter:
        print(f"{Fore.RED}Email tidak terdaftar!{Style.RESET_ALL}")
        return
    
    
    dokter = daftar_dokter[email]
    print(f"\n{Fore.CYAN}Data Lama:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Nama: {dokter['nama']}")
    print(f"ID Spesialisasi: {dokter['id_spesial']}")
    print(f"Telepon: {dokter['telepon']}")
    print(f"Alamat: {dokter['alamat']}{Style.RESET_ALL}")
    
    
    print(f"\n{Fore.YELLOW}Masukkan data baru (kosongkan jika tidak ingin diubah){Style.RESET_ALL}")
    nama_baru = input(f"{Fore.YELLOW}Nama baru: {Style.RESET_ALL}")
    
    
    print(f"\n{Fore.CYAN}Daftar Spesialisasi:{Style.RESET_ALL}")
    spesialis.tampilkan_spesialisasi()
    
    id_spesial_baru = input(f"\n{Fore.YELLOW}ID Spesialisasi baru: {Style.RESET_ALL}")
    telepon_baru = input(f"{Fore.YELLOW}Telepon baru: {Style.RESET_ALL}")
    alamat_baru = input(f"{Fore.YELLOW}Alamat baru: {Style.RESET_ALL}")
    
    
    if nama_baru == "":
        nama_baru = dokter['nama']
    if id_spesial_baru == "":
        id_spesial_baru = dokter['id_spesial']
    if telepon_baru == "":
        telepon_baru = dokter['telepon']
    if alamat_baru == "":
        alamat_baru = dokter['alamat']
    
    
    spesialis.muat_spesialisasi()
    if id_spesial_baru not in spesialis.daftar_spesialisasi:
        print(f"{Fore.RED}ID Spesialisasi tidak valid! Menggunakan ID lama.{Style.RESET_ALL}")
        id_spesial_baru = dokter['id_spesial']
    
    
    daftar_dokter[email] = {
        "nama": nama_baru,
        "id_spesial": id_spesial_baru,
        "telepon": telepon_baru,
        "alamat": alamat_baru
    }
    
    
    file = open(file_dokter, 'w')
    for email_dokter in daftar_dokter:
        dok = daftar_dokter[email_dokter]
        file.write(f"{email_dokter},{dok['nama']},{dok['id_spesial']},{dok['telepon']},{dok['alamat']}\n")
    file.close()
    
    print(f"{Fore.GREEN}Data dokter berhasil diubah!{Style.RESET_ALL}")


def hapus_dokter():
    print(f"\n{Fore.CYAN}--- HAPUS DOKTER ---{Style.RESET_ALL}")
    
    
    tampilkan_dokter()
    
    
    email = input(f"\n{Fore.YELLOW}Masukkan email dokter yang akan dihapus: {Style.RESET_ALL}")
    
    
    muat_dokter()
    if email not in daftar_dokter:
        print(f"{Fore.RED}Email tidak terdaftar!{Style.RESET_ALL}")
        return
    
    
    nama_dokter = daftar_dokter[email]['nama']
    konfirmasi = input(f"{Fore.RED}Yakin hapus dokter {nama_dokter}? (y/n): {Style.RESET_ALL}")
    
    if konfirmasi.lower() != 'y':
        print(f"{Fore.YELLOW}Penghapusan dibatalkan{Style.RESET_ALL}")
        return
    
    
    file = open(file_dokter, 'w')
    for email_dokter in daftar_dokter:
        if email_dokter != email:
            dok = daftar_dokter[email_dokter]
            file.write(f"{email_dokter},{dok['nama']},{dok['id_spesial']},{dok['telepon']},{dok['alamat']}\n")
    file.close()
    
    
    del daftar_dokter[email]
    print(f"{Fore.GREEN}Dokter {nama_dokter} berhasil dihapus{Style.RESET_ALL}")


def cari_dokter_spesialisasi():
    print(f"\n{Fore.CYAN}--- CARI DOKTER BERDASARKAN SPESIALISASI ---{Style.RESET_ALL}")
    
    
    print(f"\n{Fore.CYAN}Daftar spesialisasi:{Style.RESET_ALL}")
    spesialis.tampilkan_spesialisasi()
    
    
    id_spesial = input(f"\n{Fore.YELLOW}Masukkan ID spesialisasi: {Style.RESET_ALL}")
    
    
    spesialis.muat_spesialisasi()
    if id_spesial not in spesialis.daftar_spesialisasi:
        print(f"{Fore.RED}ID Spesialisasi tidak valid!{Style.RESET_ALL}")
        return
    
    
    muat_dokter()
    
    nama_spesial = spesialis.daftar_spesialisasi[id_spesial]['nama']
    print(f"\n{Fore.CYAN}Dokter dengan spesialisasi {nama_spesial}:{Style.RESET_ALL}")
    
    ketemu = False
    for email in daftar_dokter:
        dokter = daftar_dokter[email]
        if dokter['id_spesial'] == id_spesial:
            print(f"\n{Fore.GREEN}Email: {email}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Nama: {dokter['nama']}")
            print(f"Telepon: {dokter['telepon']}")
            print(f"Alamat: {dokter['alamat']}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-' * 30}{Style.RESET_ALL}")
            ketemu = True
    
    if not ketemu:
        print(f"{Fore.RED}Tidak ada dokter dengan spesialisasi {nama_spesial}{Style.RESET_ALL}")


def cari_dokter_nama():
    print(f"\n{Fore.CYAN}--- CARI DOKTER BERDASARKAN NAMA ---{Style.RESET_ALL}")
    
    
    kata_kunci = input(f"{Fore.YELLOW}Masukkan nama dokter (sebagian saja juga bisa): {Style.RESET_ALL}").lower()
    
    
    muat_dokter()
    spesialis.muat_spesialisasi()
    
    print(f"\n{Fore.CYAN}Hasil pencarian:{Style.RESET_ALL}")
    
    ketemu = False
    for email in daftar_dokter:
        dokter = daftar_dokter[email]
        if kata_kunci in dokter['nama'].lower():
            
            nama_spesial = "Tidak diketahui"
            id_spesial = dokter['id_spesial']
            if id_spesial in spesialis.daftar_spesialisasi:
                nama_spesial = spesialis.daftar_spesialisasi[id_spesial]['nama']
                
            print(f"\n{Fore.GREEN}Email: {email}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Nama: {dokter['nama']}")
            print(f"Spesialisasi: {nama_spesial}")
            print(f"Telepon: {dokter['telepon']}")
            print(f"Alamat: {dokter['alamat']}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-' * 30}{Style.RESET_ALL}")
            ketemu = True
    
    if not ketemu:
        print(f"{Fore.RED}Tidak ada dokter dengan nama yang mengandung '{kata_kunci}'{Style.RESET_ALL}")


def menu_dokter():
    while True:
        
        print(f"\n{Fore.CYAN}")
        banner = pyfiglet.figlet_format("DATA DOKTER", font="small")
        print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}========== MENU DOKTER =========={Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Daftar Dokter")
        print(f"2. Tambah Dokter Baru")
        print(f"3. Edit Data Dokter")
        print(f"4. Hapus Dokter")
        print(f"5. Cari Dokter berdasarkan Spesialisasi")
        print(f"6. Cari Dokter berdasarkan Nama")
        print(f"{Fore.RED}0. EXIT{Style.RESET_ALL}")
        
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
            print(f"{Fore.YELLOW}Kembali ke menu utama...{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid!{Style.RESET_ALL}")


if __name__ == "__main__":

    menu_dokter()