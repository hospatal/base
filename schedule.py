import os
import doctor
import room  
from colorama import Fore, Style, init 

init(autoreset=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
SCHEDULE_FILE = os.path.join(script_dir, 'schedules.txt')

schedules = {}

def load_schedules():
    global schedules
    schedules.clear()
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r') as f:
            for line in f:
                try:
                    parts = line.strip().split(',')
                    if len(parts) == 6:
                        sch_id, day, start_hour, end_hour, room_id_val, doctor_email_val = parts
                        schedules[sch_id] = {
                            "day": day, 
                            "start_hour": start_hour, 
                            "end_hour": end_hour, 
                            "room_id": room_id_val, 
                            "doctor_email": doctor_email_val
                        }
                    else:
                        print(f"Peringatan: Baris data jadwal tidak valid (jumlah field tidak 6): {line.strip()}")
                except ValueError:
                    print(f"Peringatan: Error memproses baris data jadwal: {line.strip()}")
    else:
        open(SCHEDULE_FILE, 'w').close()
      
def get_schedules():
    load_schedules()
    print(f"\n{Fore.CYAN}--- DAFTAR SEMUA JADWAL ---{Style.RESET_ALL}")
    if not schedules:
        print(f"{Fore.YELLOW}Belum ada data jadwal.{Style.RESET_ALL}")
    else:
        doctor.muat_dokter()
        room.load_rooms()
        for sch_id, schedule_data in schedules.items():
            doc_name = doctor.daftar_dokter.get(schedule_data['doctor_email'], {}).get('nama', schedule_data['doctor_email'])
            room_name = room.rooms.get(schedule_data['room_id'], {}).get('name', f"ID: {schedule_data['room_id']}")
            print(f"{Fore.GREEN}{sch_id}. Hari: {schedule_data['day']}, Jam: {schedule_data['start_hour']}-{schedule_data['end_hour']}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   Dokter: {doc_name}")
            print(f"   Ruangan: {room_name}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-'*20}{Style.RESET_ALL}")
            
def get_last_schedule_id():
    load_schedules()
    last_id = 0
    if not schedules:
        return "1"
    for sch_id_str in schedules.keys():
        try:
            if int(sch_id_str) > last_id:
                last_id = int(sch_id_str)
        except ValueError:
            continue 
    return str(last_id + 1)

def _save_all_schedules():
    """Menyimpan semua data jadwal dari dictionary ke file (overwrite)."""
    try:
        with open(SCHEDULE_FILE, 'w') as f:
            for sch_id, data in schedules.items():
                f.write(f"{sch_id},{data['day']},{data['start_hour']},{data['end_hour']},{data['room_id']},{data['doctor_email']}\n")
        return True
    except IOError:
        print(f"{Fore.RED}Gagal menyimpan semua data jadwal ke file.{Style.RESET_ALL}")
        return False

def add_schedule():
    print(f"\n{Fore.CYAN}--- TAMBAH JADWAL BARU (Admin) ---{Style.RESET_ALL}")

    doctor.muat_dokter() 
    if not doctor.daftar_dokter:
        print(f"{Fore.RED}Tidak ada data dokter. Tambahkan dokter terlebih dahulu.{Style.RESET_ALL}")
        return
    print(f"\n{Fore.CYAN}Daftar Dokter Tersedia:{Style.RESET_ALL}")
    for email_d, detail_d in doctor.daftar_dokter.items():
        print(f"- {email_d} (Nama: {detail_d['nama']})")
    doctor_email_input = input(f"{Fore.YELLOW}Email Dokter: {Style.RESET_ALL}")
    if doctor_email_input not in doctor.daftar_dokter:
        print(f"{Fore.RED}Email dokter '{doctor_email_input}' tidak ditemukan.{Style.RESET_ALL}")
        return

    room.load_rooms() 
    if not room.rooms:
        print(f"{Fore.RED}Tidak ada data ruangan. Tambahkan ruangan terlebih dahulu.{Style.RESET_ALL}")
        return
    print(f"\n{Fore.CYAN}Daftar Ruangan Tersedia:{Style.RESET_ALL}")
    for id_r, detail_r in room.rooms.items():
        print(f"- ID: {id_r} (Nama: {detail_r['name']})")
    room_id_input = input(f"{Fore.YELLOW}ID Ruangan: {Style.RESET_ALL}")
    if room_id_input not in room.rooms:
        print(f"{Fore.RED}ID Ruangan '{room_id_input}' tidak ditemukan.{Style.RESET_ALL}")
        return

    new_id = get_last_schedule_id()
    day_input = input(f"{Fore.YELLOW}Hari (e.g., Senin, Selasa): {Style.RESET_ALL}")
    start_hour_input = input(f"{Fore.YELLOW}Jam Mulai (HH:MM): {Style.RESET_ALL}") 
    end_hour_input = input(f"{Fore.YELLOW}Jam Selesai (HH:MM): {Style.RESET_ALL}") 
    
    schedules[new_id] = {
        "day": day_input, 
        "start_hour": start_hour_input, 
        "end_hour": end_hour_input, 
        "room_id": room_id_input, 
        "doctor_email": doctor_email_input
    }
    
    if _save_all_schedules():
        print(f"{Fore.GREEN}\nJadwal berhasil ditambahkan dengan ID {new_id}.{Style.RESET_ALL}")
    else:
        load_schedules() 

def edit_schedule():
    print(f"\n{Fore.CYAN}--- EDIT JADWAL (Admin) ---{Style.RESET_ALL}")
    get_schedules() 
    id_target = input(f"{Fore.YELLOW}Masukkan ID Jadwal yang akan diedit: {Style.RESET_ALL}")
    
    load_schedules() 
    if id_target not in schedules:
        print(f"{Fore.RED}\nJadwal dengan ID '{id_target}' tidak ditemukan.{Style.RESET_ALL}")
        return

    data_lama = schedules[id_target]
    print(f"{Fore.BLUE}Data lama: Hari: {data_lama['day']}, Jam: {data_lama['start_hour']}-{data_lama['end_hour']}, Ruang ID: {data_lama['room_id']}, Dokter: {data_lama['doctor_email']}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}Masukkan data baru (kosongkan jika tidak diubah):{Style.RESET_ALL}")
    day_baru = input(f"{Fore.YELLOW}Hari baru: {Style.RESET_ALL}") or data_lama['day']
    start_hour_baru = input(f"{Fore.YELLOW}Jam Mulai baru (HH:MM): {Style.RESET_ALL}") or data_lama['start_hour']
    end_hour_baru = input(f"{Fore.YELLOW}Jam Selesai baru (HH:MM): {Style.RESET_ALL}") or data_lama['end_hour']
    
    doctor.muat_dokter()
    print(f"\n{Fore.CYAN}Daftar Dokter Tersedia (untuk email dokter baru):{Style.RESET_ALL}")
    for email_d, detail_d in doctor.daftar_dokter.items():
        print(f"- {email_d} (Nama: {detail_d['nama']})")
    doctor_email_baru = input(f"{Fore.YELLOW}Email Dokter baru: {Style.RESET_ALL}") or data_lama['doctor_email']
    if doctor_email_baru not in doctor.daftar_dokter:
        print(f"{Fore.RED}Email dokter '{doctor_email_baru}' tidak valid! Menggunakan email lama.{Style.RESET_ALL}")
        doctor_email_baru = data_lama['doctor_email']

    room.load_rooms()
    print(f"\n{Fore.CYAN}Daftar Ruangan Tersedia (untuk ID ruangan baru):{Style.RESET_ALL}")
    for id_r, detail_r in room.rooms.items():
        print(f"- ID: {id_r} (Nama: {detail_r['name']})")
    room_id_baru = input(f"{Fore.YELLOW}ID Ruangan baru: {Style.RESET_ALL}") or data_lama['room_id']
    if room_id_baru not in room.rooms:
        print(f"{Fore.RED}ID Ruangan '{room_id_baru}' tidak valid! Menggunakan ID lama.{Style.RESET_ALL}")
        room_id_baru = data_lama['room_id']

    schedules[id_target] = {
        "day": day_baru, 
        "start_hour": start_hour_baru, 
        "end_hour": end_hour_baru, 
        "room_id": room_id_baru, 
        "doctor_email": doctor_email_baru
    }
   
    if _save_all_schedules():
        print(f"{Fore.GREEN}\nJadwal berhasil diubah.{Style.RESET_ALL}")
    else:
        load_schedules()

def delete_schedule():
    print(f"\n{Fore.CYAN}--- HAPUS JADWAL (Admin) ---{Style.RESET_ALL}")
    get_schedules()
    id_target = input(f"{Fore.YELLOW}Masukkan ID Jadwal yang akan dihapus: {Style.RESET_ALL}")

    load_schedules()
    if id_target not in schedules:
        print(f"{Fore.RED}\nJadwal dengan ID '{id_target}' tidak ditemukan.{Style.RESET_ALL}")
        return
    
    # PERINGATAN: Tambahkan pengecekan apakah jadwal ini sudah di-book di appointments
    # Jika iya, mungkin tidak boleh dihapus atau berikan peringatan.
    konfirmasi = input(f"{Fore.RED}Yakin ingin menghapus jadwal ID '{id_target}'? (y/n): {Style.RESET_ALL}")
    if konfirmasi.lower() != 'y':
        print(f"{Fore.YELLOW}Penghapusan jadwal dibatalkan.{Style.RESET_ALL}")
        return
        
   
    del schedules[id_target]
    
    if _save_all_schedules():
        print(f"{Fore.GREEN}\nJadwal berhasil dihapus.{Style.RESET_ALL}")
    else:
        load_schedules()
   
def schedule_menu():
    while True:
        print(f"\n{Fore.CYAN}--- MENU JADWAL (Admin) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Semua Jadwal")
        print("2. Tambah Jadwal Baru")
        print("3. Edit Jadwal")
        print("4. Hapus Jadwal")
        print(f"{Fore.RED}0. Kembali ke Menu Admin Utama{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")
        if choice == "1":
            get_schedules()
        elif choice == "2":
            add_schedule()
        elif choice == "3":
            edit_schedule()
        elif choice == "4":
            delete_schedule()
        elif choice == "0":
            break
        else:
            print(f"{Fore.RED}\nPilihan tidak valid, coba lagi.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
         
if __name__ == "__main__":
    schedule_menu()