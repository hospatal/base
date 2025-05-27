import login
import doctor
import spesialis
import schedule
import room
import appointment 
import os
from colorama import Fore, Style, init 

init(autoreset=True)

def view_own_profile_doctor():
    """Menampilkan profil dokter yang sedang login."""
    if login.current_user and login.current_role == "dokter":
        doctor.muat_dokter()  
        spesialis.muat_spesialisasi() 
        user_email = login.current_user
        if user_email in doctor.daftar_dokter:
            doc_info = doctor.daftar_dokter[user_email]
            nama_spesial = "Tidak diketahui"
            id_spesial = doc_info['id_spesial']
            if id_spesial in spesialis.daftar_spesialisasi:
                nama_spesial = spesialis.daftar_spesialisasi[id_spesial]['nama']
            
            print(f"\n{Fore.CYAN}--- PROFIL DOKTER: {doc_info['nama']} ---{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Email: {user_email}")
            print(f"Spesialisasi: {nama_spesial}")
            print(f"Telepon: {doc_info['telepon']}")
            print(f"Alamat: {doc_info['alamat']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}\nProfil detail dokter untuk {user_email} tidak ditemukan (mungkin belum dibuat oleh admin).{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}\nTidak ada dokter yang login atau peran tidak sesuai.{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Tekan Enter untuk kembali ke menu dokter...{Style.RESET_ALL}")

def view_own_schedule_doctor():
    """Menampilkan jadwal untuk dokter yang sedang login."""
    if login.current_user and login.current_role == "dokter":
        schedule.load_schedules()
        doctor.muat_dokter()
        room.load_rooms()

        found_schedule_entries = False
        print(f"\n{Fore.CYAN}--- JADWAL ANDA ({doctor.daftar_dokter.get(login.current_user, {}).get('nama', login.current_user)}) ---{Style.RESET_ALL}")
        
      
        for id_jadwal, detail_jadwal in schedule.schedules.items():
            if detail_jadwal['doctor_email'] == login.current_user:
                room_name = room.rooms.get(detail_jadwal['room_id'], {}).get('name', f"ID Ruang: {detail_jadwal['room_id']}")
                print(f"{Fore.GREEN}{id_jadwal}. {detail_jadwal['day']}, {detail_jadwal['start_hour']}-{detail_jadwal['end_hour']} di Ruang {room_name}{Style.RESET_ALL}")
                found_schedule_entries = True
        if not found_schedule_entries:
            print(f"{Fore.YELLOW}Anda belum memiliki jadwal.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}\nTidak ada dokter yang login atau peran tidak sesuai.{Style.RESET_ALL}")
    input(f"\n{Fore.CYAN}Tekan Enter untuk kembali ke menu dokter...{Style.RESET_ALL}")

def admin_user_management_menu():
    """Menampilkan menu manajemen pengguna untuk admin."""
    while True:
        print(f"\n{Fore.CYAN}--- MANAJEMEN PENGGUNA (Admin) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Hapus Pengguna")
        print("2. Edit Password Pengguna")
        print(f"{Fore.RED}0. Kembali ke Menu Admin{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")

        if choice == '1':
            login.hapus_user() 
        elif choice == '2':
            login.edit_user() 
        elif choice == '0':
            break
        else:
            print(f"{Fore.RED}\nPilihan tidak valid.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")


def admin_menu():
    """Menampilkan menu untuk pengguna dengan peran admin."""
    while True:
        print(f"\n{Fore.CYAN}--- MENU ADMIN ({login.current_user}) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Manajemen Dokter")
        print("2. Manajemen Spesialisasi")
        print("3. Manajemen Ruangan")
        print("4. Manajemen Jadwal")
        print("5. Manajemen Pengguna")
        print("6. Manajemen Semua Janji Temu")
        print(f"{Fore.RED}0. Logout{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")

        if choice == '1':
            doctor.menu_dokter() 
        elif choice == '2':
            spesialis.menu_spesialisasi()
        elif choice == '3':
            room.room_menu() 
        elif choice == '4':
            schedule.schedule_menu() 
        elif choice == '5':
            admin_user_management_menu()
        elif choice == '6': 
            appointment.appointment_menu_admin()
        elif choice == '0':
            login.logout() 
            break
        else:
            print(f"{Fore.RED}\nPilihan tidak valid.{Style.RESET_ALL}")

def doctor_menu():
    """Menampilkan menu untuk pengguna dengan peran dokter."""
    while True:
        print(f"\n{Fore.CYAN}--- MENU DOKTER ({login.current_user}) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Semua Jadwal")
        print("2. Lihat Jadwal Saya")
        print("3. Lihat Profil Saya")
        print("4. Edit Profil Saya")      
        print("5. Manajemen Janji Temu Saya") 
        print(f"{Fore.RED}0. Logout{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")

        if choice == '1':
            schedule.get_schedules() 
            input(f"\n{Fore.CYAN}Tekan Enter untuk kembali...{Style.RESET_ALL}")
        elif choice == '2':
            view_own_schedule_doctor()
        elif choice == '3':
            view_own_profile_doctor() 
        elif choice == '4':            
            doctor.edit_own_profile(login.current_user) 
        elif choice == '5':          
            appointment.appointment_menu_doctor(login.current_user)
        elif choice == '0':
            login.logout() 
            break
        else:
            print(f"{Fore.RED}\nPilihan tidak valid.{Style.RESET_ALL}")

def patient_menu():
    """Menampilkan menu untuk pengguna dengan peran pasien."""
    while True:
        print(f"\n{Fore.CYAN}--- MENU PASIEN ({login.current_user}) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Daftar Dokter Keseluruhan")
        print("2. Cari Dokter berdasarkan Spesialisasi")
        print("3. Cari Dokter berdasarkan Nama")
        print("4. Lihat Daftar Spesialisasi")
        print("5. Lihat Semua Jadwal Dokter")
        print("6. Manajemen Janji Temu Saya")
        print(f"{Fore.RED}0. Logout{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")

        action_taken = True
        if choice == '1':
            doctor.tampilkan_dokter() 
        elif choice == '2':
            doctor.cari_dokter_spesialisasi() 
        elif choice == '3':
            doctor.cari_dokter_nama() 
        elif choice == '4':
            spesialis.tampilkan_spesialisasi() 
        elif choice == '5':
            schedule.get_schedules() 
        elif choice == '6': 
            appointment.appointment_menu_patient(login.current_user)
            action_taken = False 
        elif choice == '0':
            login.logout() 
            action_taken = False
            break
        else:
            print(f"{Fore.RED}\nPilihan tidak valid.{Style.RESET_ALL}")
            action_taken = False
        
        if action_taken: 
             input(f"\n{Fore.CYAN}Tekan Enter untuk kembali ke menu pasien...{Style.RESET_ALL}")


def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    login.load_users() 

    while True:
        if login.current_user is None: 
            print(f"\n{Fore.MAGENTA}===== SISTEM INFORMASI KLINIK ====={Style.RESET_ALL}")
            print(f"{Fore.WHITE}1. Login")
            print("2. Register")
            print(f"{Fore.RED}3. Keluar Program{Style.RESET_ALL}")
            main_choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")

            if main_choice == '1':
                login.login_user() 
            elif main_choice == '2':
                login.register() 
            elif main_choice == '3':
                print(f"\n{Fore.YELLOW}Terima kasih, program selesai.{Style.RESET_ALL}\n")
                break
            else:
                print(f"{Fore.RED}\nPilihan tidak valid.{Style.RESET_ALL}")
            
            if main_choice != '3' and login.current_user is None:
                 input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

        else:
            print(f"\n{Fore.GREEN}Selamat datang, {login.current_user} (Peran: {login.current_role})!{Style.RESET_ALL}") 
            if login.current_role == "admin": 
                admin_menu()
            elif login.current_role == "dokter": 
                doctor_menu()
            elif login.current_role == "pasien": 
                patient_menu()
            else:
                print(f"{Fore.RED}Peran tidak diketahui. Logout otomatis.{Style.RESET_ALL}")
                login.logout() 
        
if __name__ == "__main__":
    main()