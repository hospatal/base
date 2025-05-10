import os

schedules = {}

SCHEDULE_FILE = 'schedules.txt'

def load_schedules():
   global schedules
   schedules.clear()
   if os.path.exists(SCHEDULE_FILE):
      with open(SCHEDULE_FILE, 'r') as f:
         for line in f:
            id, day, start_hour, end_hour, room_id, doctor_email = line.strip().split(',')
            schedules[id] = {"day": day, "start_hour": start_hour, "end_hour": end_hour, "room_id": room_id, "doctor_email": doctor_email}
   # else:
   #    with open(SCHEDULE_FILE, 'w') as f:
   #       f.write("1,Senin,08:00,09:00,1,admin@example.com\n")
   #    schedules["1"] = {"day": "Senin", "start_hour": "08:00", "end_hour": "09:00", "room_id": "1", "doctor_email": "admin@example.com"}
      
def get_schedules():
   load_schedules()
   for id, schedule in schedules.items():
      print(f"{id}. {schedule['day']} - {schedule['start_hour']} - {schedule['end_hour']} - {schedule['room_id']} - {schedule['doctor_email']}")
      
def get_last_schedule_id():
   load_schedules()
   last_id = 0
   for id, schedule in schedules.items():
      if int(id) > last_id:
         last_id = int(id)
   return str(last_id + 1)

def save_schedule(id, day, start_hour, end_hour, room_id, doctor_email):
   with open(SCHEDULE_FILE, 'a') as f:
      f.write(f"{id},{day},{start_hour},{end_hour},{room_id},{doctor_email}\n")
      
   schedules[id] = {"day": day, "start_hour": start_hour, "end_hour": end_hour, "room_id": room_id, "doctor_email": doctor_email}
   
def add_schedule():
   print("\n=== Tambah Jadwal Baru ===")
   id = get_last_schedule_id()
   day = input("Hari: ")
   start_hour = input("Jam Mulai: ")
   end_hour = input("Jam Selesai: ")
   room_id = input("ID Ruangan: ")
   doctor_email = input("Email Dokter: ")
   save_schedule(id, day, start_hour, end_hour, room_id, doctor_email)
   print("\nJadwal berhasil ditambahkan.\n")
   
def edit_schedule():
   print("\n=== Edit Jadwal ===")
   id = input("ID Jadwal: ")
   if id not in schedules:
      print("\nJadwal tidak ditemukan.\n")
      return
   day = input("Hari: ")
   start_hour = input("Jam Mulai: ")
   end_hour = input("Jam Selesai: ")
   room_id = input("ID Ruangan: ")
   doctor_email = input("Email Dokter: ")
   with open(SCHEDULE_FILE, 'w') as f:
      for id, schedule in schedules.items():
         if id == id:
            f.write(f"{id},{day},{start_hour},{end_hour},{room_id},{doctor_email}\n")
         else:
            f.write(f"{id},{schedule['day']},{schedule['start_hour']},{schedule['end_hour']},{schedule['room_id']},{schedule['doctor_email']}\n")
   print("\nJadwal berhasil diubah.\n")

def delete_schedule():
   print("\n=== Hapus Jadwal ===")
   id = input("ID Jadwal: ")
   if id not in schedules:
      print("\nJadwal tidak ditemukan.\n")
      return
   with open(SCHEDULE_FILE, 'w') as f:
      for id, schedule in schedules.items():
         if id == id:
            continue
         f.write(f"{id},{schedule['day']},{schedule['start_hour']},{schedule['end_hour']},{schedule['room_id']},{schedule['doctor_email']}\n")
      del schedules[id]
   print("\nJadwal berhasil dihapus.\n")
   
def schedule_menu():
   while True:
      print("\n=== Menu Jadwal ===")
      print("1. Lihat Jadwal")
      print("2. Tambah Jadwal")
      print("3. Edit Jadwal")
      print("4. Hapus Jadwal")
      print("5. Kembali")
      choice = input("Pilihan: ")
      if choice == "1":
         get_schedules()
      elif choice == "2":
         add_schedule()
      elif choice == "3":
         edit_schedule()
      elif choice == "4":
         delete_schedule()
      elif choice == "5":
         break
      else:
         print("\nPilihan tidak valid, coba lagi.\n")
         
   print("\nTerima kasih, program selesai.\n")
   
   
schedule_menu()