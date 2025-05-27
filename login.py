import os
import getpass
import hashlib

# Data pengguna
users = {}

# Sesi login saat ini
current_user = None
current_role = None

script_dir = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(script_dir, 'users.txt')

def load_users():
    global users
    users.clear()
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            for line in f:
                try:
                    email, password, role = line.strip().split(',')
                    users[email] = {"password": password, "role": role}
                except ValueError:
                    print(f"Peringatan: Baris data pengguna tidak valid di {USER_FILE}: {line.strip()}")
    else:
        open(USER_FILE, 'w').close()
        print(f"Info: File {USER_FILE} tidak ditemukan, file baru telah dibuat.")

def save_all_users():
    with open(USER_FILE, 'w') as f:
        for email, data in users.items():
            f.write(f"{email},{data['password']},{data['role']}\n")

def save_user(email, password, role):
    users[email] = {"password": password, "role": role}
    with open(USER_FILE, 'a') as f:
        f.write(f"{email},{password},{role}\n")


def register():
    print("\n=== Registrasi Akun Baru ===")
    email = input("Email: ")
    if not email.count('@') == 1:
        print("\nEmail tidak valid.\n")
        return
        
    load_users() 
    if email in users:
        print("\nEmail sudah terdaftar.\n")
        return

    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Konfirmasi Password: ")

    if password != confirm_password:
        print("\nPassword tidak sama.\n")
        return

    # password hash
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    print("Pilih role:")
    print("1. Pasien")
    print("2. Dokter")
    print("3. Admin")
    role_choice = input("Masukkan angka sesuai role (default: Pasien): ")

    if role_choice == '2':
        role = "dokter"
    elif role_choice == '3':
        role = "admin"
    else: 
        role = "pasien"

    save_user(email, password_hash, role) # users[email] akan diupdate, lalu append ke file
    print(f"\nRegistrasi berhasil sebagai {role}!\n")

# Fungsi login
def login_user():
    global current_user, current_role
    load_users() 
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if email in users and users[email]["password"] == password_hash:
        current_user = email
        current_role = users[email]["role"]
        print(f"\nLogin berhasil! Selamat datang, {email} ({current_role}).\n")
    else:
        print("\nEmail atau password salah.\n")
        current_user = None 
        current_role = None

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
    load_users() 
    email_to_delete = input("Masukkan email user yang ingin dihapus: ")
    if email_to_delete == current_user:
        print("\nTidak dapat menghapus diri sendiri.\n")
        return
    if email_to_delete in users:
        if users[email_to_delete]["role"] == "admin" and sum(1 for u in users.values() if u['role'] == 'admin') <=1 :
             print("\nTidak dapat menghapus satu-satunya admin yang tersisa.\n")
             return
        del users[email_to_delete]
        save_all_users() 
        print("\nUser berhasil dihapus.\n")
    else:
        print("\nUser tidak ditemukan.\n")

# Admin: Edit user
def edit_user():
    if current_role != "admin":
        print("\nHanya admin yang dapat mengedit user.\n")
        return
    load_users() 
    email_to_edit = input("Masukkan email user yang ingin diedit passwordnya: ") # Fokus edit password
    if email_to_edit in users:
        new_password = input("Masukkan password baru (kosongkan jika tidak ingin mengganti): ")
        if new_password:
            users[email_to_edit]["password"] = new_password
            save_all_users() 
            print("\nPassword user berhasil diperbarui.\n")
        else:
            print("\nPassword tidak diubah.\n")
    else:
        print("\nUser tidak ditemukan.\n")

# Main menu
def menu():
    load_users() 
    while True:
        print("""
===== Menu Utama Login (Testing) =====
1. Login
2. Register
3. Keluar Program
""")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            login_user()
            if current_user: 
                print(f"Anda login sebagai: {current_user} ({current_role})")
                logout() 
        elif pilihan == '2':
            register()
        elif pilihan == '3':
            print("\nTerima kasih, program selesai.\n")
            break
        else:
            print("\nPilihan tidak valid, coba lagi.\n")

if __name__ == "__main__":
    menu()