import os

rooms = {}

ROOM_FILE = 'rooms.txt'

def load_rooms():
   global rooms
   rooms.clear()
   if os.path.exists(ROOM_FILE):
      with open(ROOM_FILE, 'r') as f:
         for line in f:
            rooms[line.split(',')[0]] = {"name": line.split(',')[1], "desc": line.split(',')[2].strip()}
   else:
      with open(ROOM_FILE, 'w') as f:
         f.write("1,Ruangan Umum,adalah ruangan penanganan pasien keluhan umum\n")
      rooms["1"] = {"name": "Ruangan Umum", "desc": "adalah ruangan penanganan pasien keluhan umum"}

def get_rooms():
   load_rooms()
   for id, room in rooms.items():
      print(f"{id}. {room['name']} - {room['desc']}")
      
def get_room_by_name(name):
   load_rooms()
   for id, room in rooms.items():
      if room['name'] == name:
         return id

def get_last_room_id():
   load_rooms()
   last_id = 0
   for id, room in rooms.items():
      if int(id) > last_id:
         last_id = int(id)
   return str(last_id + 1)
   
def save_room(id, name, desc):
   with open(ROOM_FILE, 'a') as f:
      f.write(f"{id},{name},{desc}\n")
           
def add_room():
   print("\n=== Tambah Ruangan Baru ===")
   id = get_last_room_id()
   name = input("Nama Ruangan: ")
   desc = input("Deskripsi Ruangan: ")
   save_room(id, name, desc)
   str_id = str(id)
   rooms[str_id] = {"name": name, "desc": desc}
   print("\nRuangan berhasil ditambahkan.\n")
   
def edit_room():
   print("\n=== Edit Ruangan ===")
   id = input("ID Ruangan: ")
   if id not in rooms:
      print("\nRuangan tidak ditemukan.\n")
      return
   name = input("Nama Ruangan: ")
   desc = input("Deskripsi Ruangan: ")
   with open(ROOM_FILE, 'w') as f:
      for id, room in rooms.items():
         if id == id:
            f.write(f"{id},{name},{desc}\n")
         else:
            f.write(f"{id},{room['name']},{room['desc']}\n")
   print("\nRuangan berhasil diubah.\n")

def delete_room():
   print("\n=== Hapus Ruangan ===")
   id = input("ID Ruangan: ")
   if id not in rooms:
      print("\nRuangan tidak ditemukan.\n")
      return
   with open(ROOM_FILE, 'w') as f:
      for id, room in rooms.items():
         if id == id:
            continue
         f.write(f"{id},{room['name']},{room['desc']}\n")
      del rooms[id]
   print("\nRuangan berhasil dihapus.\n")
   
def room_menu():
   while True:
      print("\n=== Menu Ruangan ===")
      print("1. Tampilkan Ruangan")
      print("2. Tambah Ruangan")
      print("3. Edit Ruangan")
      print("4. Hapus Ruangan")
      print("5. Kembali")
      pilihan = input("Pilih menu: ")
      
      if pilihan == '1':
         get_rooms()
      elif pilihan == '2':
         add_room()
      elif pilihan == '3':
         edit_room()
      elif pilihan == '4':
         delete_room()
      elif pilihan == '5':
         break
      else:
         print("\nPilihan tidak valid, coba lagi.\n")
         
room_menu()