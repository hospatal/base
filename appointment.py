import os
import login 
import doctor 
import schedule 
import room
from colorama import Fore, Style, init 

init(autoreset=True) 

script_dir = os.path.dirname(os.path.abspath(__file__))
APPOINTMENT_FILE = os.path.join(script_dir, 'appointments.txt')

appointments = {} 

def load_appointments():
    global appointments
    appointments.clear()
    if os.path.exists(APPOINTMENT_FILE):
        with open(APPOINTMENT_FILE, 'r') as f:
            for line in f:
                try:
                    app_id, patient_email, doctor_email, schedule_id, status = line.strip().split(',')
                    appointments[app_id] = {
                        "patient_email": patient_email,
                        "doctor_email": doctor_email,
                        "schedule_id": schedule_id,
                        "status": status
                    }
                except ValueError:
                    print(f"{Fore.YELLOW}Peringatan: Baris data appointment tidak valid: {line.strip()}{Style.RESET_ALL}")
    else:
        open(APPOINTMENT_FILE, 'w').close()

def _save_all_appointments():
    try:
        with open(APPOINTMENT_FILE, 'w') as f:
            for app_id, data in appointments.items():
                f.write(f"{app_id},{data['patient_email']},{data['doctor_email']},{data['schedule_id']},{data['status']}\n")
        return True
    except IOError:
        print(f"{Fore.RED}Gagal menyimpan semua data janji temu ke file.{Style.RESET_ALL}")
        return False

def _generate_appointment_id():
    load_appointments() 
    if not appointments:
        return "A1"
    max_id = 0
    for app_id_str in appointments.keys():
        try:
            num_id = int(app_id_str[1:]) 
            if num_id > max_id:
                max_id = num_id
        except ValueError:
            continue 
    return f"A{max_id + 1}"

def book_appointment(patient_email):
    """Memungkinkan pasien untuk membuat janji temu dengan memasukkan NAMA dokter."""
    print(f"\n{Fore.CYAN}--- BUAT JANJI TEMU BARU ---{Style.RESET_ALL}")
    doctor.muat_dokter()
    schedule.load_schedules()
    room.load_rooms() # Muat data ruangan untuk info jadwal

    if not doctor.daftar_dokter:
        print(f"{Fore.YELLOW}Maaf, belum ada dokter yang terdaftar.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}Daftar Dokter Tersedia:{Style.RESET_ALL}")
    doctor.tampilkan_dokter()
    
    chosen_doctor_name = input(f"{Fore.YELLOW}Masukkan NAMA dokter yang ingin Anda temui: {Style.RESET_ALL}").strip()
    found_doctor_email = None
    
    for email, details in doctor.daftar_dokter.items():
        if details['nama'].lower() == chosen_doctor_name.lower():
            found_doctor_email = email
            break 

    if not found_doctor_email:
        print(f"{Fore.RED}Dokter dengan nama '{chosen_doctor_name}' tidak ditemukan.{Style.RESET_ALL}")
        return
    
    chosen_doctor_email = found_doctor_email

    print(f"\n{Fore.CYAN}Jadwal Tersedia untuk Dr. {doctor.daftar_dokter[chosen_doctor_email]['nama']}:{Style.RESET_ALL}")
    available_schedules_for_doctor = {}
    schedule_found_for_doctor = False
    load_appointments() 

    for sch_id, sch_details in schedule.schedules.items():
        if sch_details['doctor_email'] == chosen_doctor_email:
            is_booked = False
            for app_data in appointments.values():
                if app_data['schedule_id'] == sch_id and app_data['status'] == "Booked":
                    is_booked = True
                    break
            
            if not is_booked:
                room_name = room.rooms.get(sch_details['room_id'], {}).get('name', f"ID: {sch_details['room_id']}")
                print(f"{Fore.GREEN}ID Jadwal: {sch_id}{Style.RESET_ALL}, Hari: {sch_details['day']}, Waktu: {sch_details['start_hour']}-{sch_details['end_hour']}, Ruang: {room_name}")
                available_schedules_for_doctor[sch_id] = sch_details
                schedule_found_for_doctor = True

    if not schedule_found_for_doctor:
        print(f"{Fore.YELLOW}Tidak ada jadwal tersedia untuk dokter ini atau semua jadwal sudah dibooking.{Style.RESET_ALL}")
        return

    chosen_schedule_id = input(f"{Fore.YELLOW}Masukkan ID Jadwal yang ingin Anda pilih: {Style.RESET_ALL}")
    if chosen_schedule_id not in available_schedules_for_doctor:
        print(f"{Fore.RED}ID Jadwal tidak valid atau tidak tersedia untuk dokter ini.{Style.RESET_ALL}")
        return
            
    app_id = _generate_appointment_id()
    status = "Booked"
    
    appointments[app_id] = {
        "patient_email": patient_email,
        "doctor_email": chosen_doctor_email,
        "schedule_id": chosen_schedule_id,
        "status": status
    }
    if _save_all_appointments(): 
        print(f"{Fore.GREEN}\nJanji temu berhasil dibuat! ID Janji Temu Anda: {app_id}{Style.RESET_ALL}")
    else:
        load_appointments() 


def admin_book_appointment():
    """Memungkinkan admin untuk membuat janji temu untuk seorang pasien dengan memasukkan NAMA dokter."""
    print(f"\n{Fore.CYAN}--- BUAT JANJI TEMU BARU OLEH ADMIN ---{Style.RESET_ALL}")
    
    patient_email = input(f"{Fore.YELLOW}Masukkan email pasien: {Style.RESET_ALL}")
    login.load_users() 
    if patient_email not in login.users:
        print(f"{Fore.RED}Email pasien '{patient_email}' tidak ditemukan dalam sistem pengguna.{Style.RESET_ALL}")
        return
    if login.users[patient_email]['role'] != 'pasien':
         print(f"{Fore.RED}Pengguna '{patient_email}' bukan pasien (Peran: {login.users[patient_email]['role']}).{Style.RESET_ALL}")
         return

    doctor.muat_dokter() 
    schedule.load_schedules() 
    room.load_rooms() # Muat data ruangan

    if not doctor.daftar_dokter:
        print(f"{Fore.YELLOW}Maaf, belum ada dokter yang terdaftar.{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}Daftar Dokter Tersedia:{Style.RESET_ALL}")
    doctor.tampilkan_dokter() 
    
    chosen_doctor_name = input(f"{Fore.YELLOW}Masukkan NAMA dokter yang akan ditemui: {Style.RESET_ALL}").strip()
    found_doctor_email = None

    for email, details in doctor.daftar_dokter.items():
        if details['nama'].lower() == chosen_doctor_name.lower():
            found_doctor_email = email
            break 

    if not found_doctor_email:
        print(f"{Fore.RED}Dokter dengan nama '{chosen_doctor_name}' tidak ditemukan.{Style.RESET_ALL}")
        return
        
    chosen_doctor_email = found_doctor_email

    print(f"\n{Fore.CYAN}Jadwal Tersedia untuk Dr. {doctor.daftar_dokter[chosen_doctor_email]['nama']}:{Style.RESET_ALL}")
    available_schedules_for_doctor = {}
    schedule_found_for_doctor = False
    load_appointments()

    for sch_id, sch_details in schedule.schedules.items(): 
        if sch_details['doctor_email'] == chosen_doctor_email:
            is_booked = False
            for app_data in appointments.values():
                if app_data['schedule_id'] == sch_id and app_data['status'] == "Booked":
                    is_booked = True
                    break
            
            if not is_booked:
                room_name = room.rooms.get(sch_details['room_id'], {}).get('name', f"ID: {sch_details['room_id']}")
                print(f"{Fore.GREEN}ID Jadwal: {sch_id}{Style.RESET_ALL}, Hari: {sch_details['day']}, Waktu: {sch_details['start_hour']}-{sch_details['end_hour']}, Ruang: {room_name}")
                available_schedules_for_doctor[sch_id] = sch_details
                schedule_found_for_doctor = True

    if not schedule_found_for_doctor:
        print(f"{Fore.YELLOW}Tidak ada jadwal tersedia untuk dokter ini atau semua jadwal sudah dibooking.{Style.RESET_ALL}")
        return

    chosen_schedule_id = input(f"{Fore.YELLOW}Masukkan ID Jadwal yang ingin dipilih: {Style.RESET_ALL}")
    if chosen_schedule_id not in available_schedules_for_doctor:
        print(f"{Fore.RED}ID Jadwal tidak valid atau tidak tersedia untuk dokter ini.{Style.RESET_ALL}")
        return
            
    app_id = _generate_appointment_id() 
    status = "Booked"
    
    appointments[app_id] = {
        "patient_email": patient_email, 
        "doctor_email": chosen_doctor_email,
        "schedule_id": chosen_schedule_id,
        "status": status
    }
    if _save_all_appointments():
        print(f"{Fore.GREEN}\nJanji temu untuk pasien {patient_email} berhasil dibuat! ID Janji Temu: {app_id}{Style.RESET_ALL}")
    else:
        load_appointments()

def view_appointments(user_email, user_role):
    load_appointments()
    doctor.muat_dokter() 
    schedule.load_schedules() 
    room.load_rooms() 

    if not appointments:
        print(f"\n{Fore.YELLOW}Belum ada janji temu.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.CYAN}--- DAFTAR JANJI TEMU ---{Style.RESET_ALL}")
    found_any = False
    sorted_appointments = sorted(appointments.items()) 

    for app_id, data in sorted_appointments:
        display_appointment = False
        if user_role == "pasien" and data['patient_email'] == user_email:
            display_appointment = True
        elif user_role == "dokter" and data['doctor_email'] == user_email:
            display_appointment = True
        elif user_role == "admin":
            display_appointment = True

        if display_appointment:
            found_any = True
            doc_name = doctor.daftar_dokter.get(data['doctor_email'], {}).get('nama', data['doctor_email'])
            sch_detail = schedule.schedules.get(data['schedule_id'])
            if sch_detail:
                room_name = room.rooms.get(sch_detail['room_id'], {}).get('name', f"ID Ruang: {sch_detail['room_id']}")
                sch_info = f"Hari: {sch_detail['day']}, Waktu: {sch_detail['start_hour']}-{sch_detail['end_hour']}, Ruang: {room_name}"
            else:
                sch_info = "Detail Jadwal Tidak Ditemukan"

            status_colored = data['status']
            if data['status'] == "Booked":
                status_colored = f"{Fore.GREEN}{data['status']}{Style.RESET_ALL}"
            elif data['status'] == "Cancelled":
                status_colored = f"{Fore.RED}{data['status']}{Style.RESET_ALL}"

            print(f"\n{Fore.WHITE}ID Janji: {app_id}{Style.RESET_ALL}")
            print(f"  Pasien: {data['patient_email']}")
            print(f"  Dokter: {doc_name}")
            print(f"  Jadwal (ID: {data['schedule_id']}): {sch_info}")
            print(f"  Status: {status_colored}")
    
    if not found_any:
        if user_role == "pasien" or user_role == "dokter":
            print(f"\n{Fore.YELLOW}Anda tidak memiliki janji temu.{Style.RESET_ALL}")
        elif user_role == "admin":
             print(f"\n{Fore.YELLOW}Tidak ada janji temu dalam sistem.{Style.RESET_ALL}")

def cancel_appointment(user_email, user_role):
    print(f"\n{Fore.CYAN}--- BATALKAN JANJI TEMU ---{Style.RESET_ALL}")
    view_appointments(user_email, user_role) 
    
    if not appointments: 
        return

    app_id_to_cancel = input(f"{Fore.YELLOW}Masukkan ID Janji Temu yang ingin dibatalkan: {Style.RESET_ALL}")
    
    load_appointments() 
    if app_id_to_cancel not in appointments:
        print(f"{Fore.RED}ID Janji Temu tidak ditemukan.{Style.RESET_ALL}")
        return

    appointment_data = appointments[app_id_to_cancel]
    
    can_cancel = False
    if user_role == "pasien" and appointment_data['patient_email'] == user_email:
        can_cancel = True
    elif user_role == "dokter" and appointment_data['doctor_email'] == user_email:
        can_cancel = True 
    elif user_role == "admin":
        can_cancel = True

    if not can_cancel:
        print(f"{Fore.RED}Anda tidak memiliki izin untuk membatalkan janji temu ini.{Style.RESET_ALL}")
        return

    if appointment_data['status'] == "Cancelled":
        print(f"{Fore.YELLOW}Janji temu ini sudah dibatalkan sebelumnya.{Style.RESET_ALL}")
        return
    
    if appointment_data['status'] == "Completed": 
        print(f"{Fore.YELLOW}Janji temu yang sudah selesai tidak dapat dibatalkan.{Style.RESET_ALL}")
        return

    konfirmasi = input(f"{Fore.RED}Apakah Anda yakin ingin membatalkan janji temu {app_id_to_cancel}? (y/n): {Style.RESET_ALL}").lower()
    if konfirmasi == 'y':
        appointments[app_id_to_cancel]['status'] = "Cancelled"
        if _save_all_appointments(): 
            print(f"{Fore.GREEN}Janji temu berhasil dibatalkan.{Style.RESET_ALL}")
        else:
            load_appointments() 
    else:
        print(f"{Fore.YELLOW}Pembatalan janji temu dibatalkan.{Style.RESET_ALL}")

# --- Menu Functions ---
def appointment_menu_patient(patient_email):
    while True:
        print(f"\n{Fore.CYAN}--- MANAJEMEN JANJI TEMU (Pasien) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Buat Janji Temu Baru")
        print("2. Lihat Janji Temu Saya")
        print("3. Batalkan Janji Temu Saya")
        print(f"{Fore.RED}0. Kembali ke Menu Utama Pasien{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")

        if choice == '1':
            book_appointment(patient_email)
        elif choice == '2':
            view_appointments(patient_email, "pasien")
        elif choice == '3':
            cancel_appointment(patient_email, "pasien")
        elif choice == '0':
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

def appointment_menu_doctor(doctor_email):
    while True:
        print(f"\n{Fore.CYAN}--- MANAJEMEN JANJI TEMU (Dokter) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Janji Temu Saya")
        print("2. Batalkan Janji Temu Pasien")
        print(f"{Fore.RED}0. Kembali ke Menu Utama Dokter{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")

        if choice == '1':
            view_appointments(doctor_email, "dokter")
        elif choice == '2':
            cancel_appointment(doctor_email, "dokter") 
        elif choice == '0':
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

def appointment_menu_admin():
    while True:
        print(f"\n{Fore.CYAN}--- MANAJEMEN SEMUA JANJI TEMU (Admin) ---{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Lihat Semua Janji Temu")
        print("2. Batalkan Janji Temu (berdasarkan ID)")
        print("3. Buat Janji Temu untuk Pasien") 
        print(f"{Fore.RED}0. Kembali ke Menu Utama Admin{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}Pilihan: {Style.RESET_ALL}")

        if choice == '1':
            view_appointments(login.current_user, "admin") 
        elif choice == '2':
            cancel_appointment(login.current_user, "admin") 
        elif choice == '3': 
            admin_book_appointment() 
        elif choice == '0':
            break
        else:
            print(f"{Fore.RED}Pilihan tidak valid.{Style.RESET_ALL}")
        input(f"\n{Fore.CYAN}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

if __name__ == "__main__":
    print("Ini adalah modul appointment. Jalankan melalui main.py")