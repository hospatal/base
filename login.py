import json
import queue
import os

# Data pengguna
users = {}

# Sesi login saat ini
current_user = None
current_role = None

# File penyimpanan pengguna
USER_FILE = 'users.txt'

# Load users dari file
def load_users():
    global users
    users.clear()
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            for line in f:
                email, password, role = line.strip().split(',')
                users[email] = {"password": password, "role": role}
    else:
        # Jika file tidak ada, buat admin default
        with open(USER_FILE, 'w') as f:
            f.write("admin@example.com,admin123,admin\n")
        users["admin@example.com"] = {"password": "admin123", "role": "admin"}

# Simpan semua users ke file
def save_all_users():
    with open(USER_FILE, 'w') as f:
        for email, data in users.items():
            f.write(f"{email},{data['password']},{data['role']}\n")

# Simpan user baru ke file
def save_user(email, password, role):
    with open(USER_FILE, 'a') as f:
        f.write(f"{email},{password},{role}\n")

# Fungsi registrasi akun baru
def register():
    print("\n=== Registrasi Akun Baru ===")
    email = input("Email: ")
    if email in users:
        print("\nEmail sudah terdaftar.\n")
        return
    password = input("Password: ")
    role = "pasien"  # Registrasi hanya untuk pasien
    users[email] = {"password": password, "role": role}
    save_user(email, password, role)
    print("\nRegistrasi berhasil!\n")

# Fungsi login
def login():
    global current_user, current_role
    email = input("Email: ")
    password = input("Password: ")
    if email in users and users[email]["password"] == password:
        current_user = email
        current_role = users[email]["role"]
        print(f"\nLogin berhasil! Selamat datang, {email} ({current_role}).\n")
    else:
        print("\nEmail atau password salah.\n")

# Fungsi logout
def logout():
    global current_user, current_role
    if current_user:
        print(f"\n{current_user} berhasil logout.\n")
        current_user = None
        current_role = None
    else:
        print("\nBelum login.\n")

# Admin: Hapus user
def hapus_user():
    if current_role != "admin":
        print("\nHanya admin yang dapat menghapus user.\n")
        return
    email = input("Masukkan email user yang ingin dihapus: ")
    if email in users:
        if users[email]["role"] == "admin":
            print("\nTidak dapat menghapus sesama admin.\n")
            return
        del users[email]
        save_all_users()
        print("\nUser berhasil dihapus.\n")
    else:
        print("\nUser tidak ditemukan.\n")

# Admin: Edit user
def edit_user():
    if current_role != "admin":
        print("\nHanya admin yang dapat mengedit user.\n")
        return
    email = input("Masukkan email user yang ingin diedit: ")
    if email in users:
        new_password = input("Masukkan password baru (kosongkan jika tidak ingin mengganti): ")
        if new_password:
            users[email]["password"] = new_password
        save_all_users()
        print("\nUser berhasil diperbarui.\n")
    else:
        print("\nUser tidak ditemukan.\n")

# Main menu
def menu():
    load_users()
    while True:
        print("""
===== Menu =====
1. Login
2. Register (Pasien saja)
3. Logout
4. Hapus User (Admin)
5. Edit User (Admin)
6. Keluar
""")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            login()
        elif pilihan == '2':
            register()
        elif pilihan == '3':
            logout()
        elif pilihan == '4':
            hapus_user()
        elif pilihan == '5':
            edit_user()
        elif pilihan == '6':
            print("\nTerima kasih, program selesai.\n")
            break
        else:
            print("\nPilihan tidak valid, coba lagi.\n")

if __name__ == "__main__":
    menu()