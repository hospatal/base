import os
from colorama import Fore, Style, init 

init(autoreset=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
ROOM_FILE = os.path.join(script_dir, 'rooms.txt') 

rooms = {}

def load_rooms():
    global rooms
    rooms.clear()
    if os.path.exists(ROOM_FILE):
        with open(ROOM_FILE, 'r') as f:
            for line in f:
                try:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        room_id = parts[0]
                        name = parts[1]
                        desc = ",".join(parts[2:]) 
                        rooms[room_id] = {"name": name, "desc": desc.strip()}
                    else:
                        print(f"Peringatan: Baris data ruangan tidak valid (kurang dari 3 field): {line.strip()}")
                except IndexError:
                    print(f"Peringatan: Error memproses baris data ruangan: {line.strip()}")

    else:
        with open(ROOM_FILE, 'w') as f:
            f.write("1,Ruangan Umum,adalah ruangan penanganan pasien keluhan umum\n")
            f.write("2,Ruangan IGD,adalah ruangan yang digunakan untuk pasien darurat\n")
        load_rooms()


def _save_all_rooms():
    """Menyimpan semua data ruangan dari dictionary ke file (overwrite)."""
    try:
        with open(ROOM_FILE, 'w') as f:
            for room_id, data in rooms.items():
                f.write(f"{room_id},{data['name']},{data['desc']}\n")
        return True
    except IOError:
        print(f"{Fore.RED}Gagal menyimpan semua data ruangan ke file.{Style.RESET_ALL}")
        return False

def get_rooms():
    load_rooms()
    print(f"\n{Fore.CYAN}--- DAFTAR RUANGAN ---{Style.RESET_ALL}")
    if not rooms:
        print(f"{Fore.YELLOW}Belum ada data ruangan.{Style.RESET_ALL}")
    else:
        for room_id, room_data in rooms.items():
            print(f"{Fore.GREEN}{room_id}. {room_data['name']}{Style.RESET_ALL} - {room_data['desc']}")
      
def get_last_room_id():
    load_rooms()
    last_id = 0
    if not rooms:
        return "1" 
    for room_id in rooms.keys():
        try:
            if int(room_id) > last_id:
                last_id = int(room_id)
        except ValueError:
            continue 
    return str(last_id + 1)
   
def add_room():
    print(f"\n{Fore.CYAN}--- TAMBAH RUANGAN BARU ---{Style.RESET_ALL}")
    new_id = get_last_room_id()
    name = input(f"{Fore.YELLOW}Nama Ruangan: {Style.RESET_ALL}")
    desc = input(f"{Fore.YELLOW}Deskripsi Ruangan: {Style.RESET_ALL}")
    
    rooms[new_id] = {"name": name, "desc": desc}
    if _save_all_rooms():
        print(f"{Fore.GREEN}\nRuangan '{name}' berhasil ditambahkan dengan ID {new_id}.{Style.RESET_ALL}")
    else:
        load_rooms()
   
def edit_room():
    print(f"\n{Fore.CYAN}--- EDIT RUANGAN ---{Style.RESET_ALL}")
    get_rooms()
    id_target = input(f"{Fore.YELLOW}Masukkan ID Ruangan yang akan diedit: {Style.RESET_ALL}")
    
    load_rooms() 
    if id_target not in rooms:
        print(f"{Fore.RED}\nRuangan dengan ID '{id_target}' tidak ditemukan.{Style.RESET_ALL}")
        return

    data_lama = rooms[id_target]
    print(f"{Fore.BLUE}Data lama: ID: {id_target}, Nama: {data_lama['name']}, Deskripsi: {data_lama['desc']}{Style.RESET_ALL}")
    
    name_baru = input(f"{Fore.YELLOW}Nama Ruangan baru (kosongkan jika tidak diubah): {Style.RESET_ALL}") or data_lama['name']
    desc_baru = input(f"{Fore.YELLOW}Deskripsi Ruangan baru (kosongkan jika tidak diubah): {Style.RESET_ALL}") or data_lama['desc']
   
    rooms[id_target] = {"name": name_baru, "desc": desc_baru}
    
    if _save_all_rooms():
        print(f"{Fore.GREEN}\nRuangan berhasil diubah.{Style.RESET_ALL}")
    else:
        load_rooms()

def delete_room():
    print(f"\n{Fore.CYAN}--- HAPUS RUANGAN ---{Style.RESET_ALL}")
    get_rooms()
    id_target = input(f"{Fore.YELLOW}Masukkan ID Ruangan yang akan dihapus: {Style.RESET_ALL}")

    load_rooms()
    if id_target not in rooms:
        print(f"{Fore.RED}\nRuangan dengan ID '{id_target}' tidak ditemukan.{Style.RESET_ALL}")
        return
    
    nama_ruangan = rooms[id_target]['name']
    konfirmasi = input(f"{Fore.RED}Yakin ingin menghapus ruangan '{nama_ruangan}' (ID: {id_target})? (y/n): {Style.RESET_ALL}")
    if konfirmasi.lower() != 'y':
        print(f"{Fore.YELLOW}Penghapusan ruangan dibatalkan.{Style.RESET_ALL}")
        return
    
    # Hapus dari memori
    del rooms[id_target]
    
    if _save_all_rooms():
        print(f"{Fore.GREEN}\nRuangan berhasil dihapus.{Style.RESET_ALL}")
    else:
        load_rooms() 
  
def cari_ruangan():
    print(f"\n{Fore.CYAN}--- CARI RUANGAN ---{Style.RESET_ALL}")
    keyword = input(f"{Fore.YELLOW}Masukkan kata kunci yang akan dicari: {Style.RESET_ALL}")
    load_rooms()
    found = False
    for room_id, room_data in rooms.items():
        if keyword.lower() in room_data['name'].lower() or keyword.lower() in room_data['desc'].lower():
            print(f"{Fore.GREEN}{room_id}. {room_data['name']}{Style.RESET_ALL} - {room_data['desc']}")
            found = True
    if not found:
        print(f"{Fore.RED}\nRuangan dengan kata kunci '{keyword}' tidak ditemukan.{Style.RESET_ALL}")
   
def room_menu():
    while True:
        print(f"\n{Fore.CYAN}--- MENU RUANGAN (Admin) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Tampilkan Daftar Ruangan")
        print("2. Tambah Ruangan Baru")
        print("3. Edit Data Ruangan")
        print("4. Hapus Ruangan")
        print("5. Cari Ruangan")
        print(f"{Fore.RED}0. Kembali ke Menu Admin Utama{Style.RESET_ALL}")
        pilihan = input(f"{Fore.GREEN}Pilih menu: {Style.RESET_ALL}")
      
        if pilihan == '1':
            get_rooms()
        elif pilihan == '2':
            add_room()
        elif pilihan == '3':
            edit_room()
        elif pilihan == '4':
            delete_room()
        elif pilihan == '5':
            cari_ruangan()
        elif pilihan == '0': 
            break
        else:
            print(f"{Fore.RED}\nPilihan tidak valid, coba lagi.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}") # Tambah pause
         
if __name__ == "__main__":
    room_menu()