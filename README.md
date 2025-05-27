# Proyek Akhir - Mata Kuliah Algoritma dan Struktur Data

## Tema: Jadwal Praktek Dokter Pada Sebuah Klinik

### Kontributor

1. Putra Setyonugroho
2. Muhammad Zahran Rabbani
3. Ananda DSandri Anugrah

### Deskripsi

Program manajemen jadwal dokter di klinik/rumah sakit yang memungkinkan staf mengelola dan mencari jadwal berdasarkan nama atau spesialisasi. Dilengkapi sistem autentikasi untuk keamanan data, program ini dibangun dengan Python menggunakan algoritma dan struktur data yang efisien.

Fitur utama meliputi pencarian jadwal berdasarkan nama atau spesialisasi, pengelolaan jadwal secara fleksibel oleh administrator, serta sistem autentikasi untuk memastikan keamanan dan integritas data.

Program ini dirancang untuk efisiensi dan kemudahan penggunaan, dengan antarmuka yang intuitif serta implementasi algoritma optimal untuk pencarian dan pengelolaan jadwal yang cepat dan akurat.

### Target Pengguna

- Dokter Klinik
- Admin Klinik
- Pasien Klinik

### Dokumentasi

Dokumentasi perancangan aplikasi dapat dilihat [disini](https://app.eraser.io/workspace/MaXHfhE7niFGjTfzbqqg?origin=share).

### Lisensi

Lisensi ini memberikan izin kepada siapa saja untuk menggunakan, menyalin, mengubah, dan mendistribusikan program ini tanpa biaya, dengan ketentuan bahwa program ini harus tetap dilisensikan dengan lisensi yang sama dan memberikan kredit yang sesuai kepada kontributor.

---

1. Dandi (Authentication & Appointment)

   - Authentication: Login/logout menggunakan email & password, validasi pengguna, dan manajemen sesi.
   - Appointment: Mengelola janji temu pasien, mengatur antrean dengan Queue, dan menyimpan data janji temu.

2. Putra (Room & Schedule)

   - Room: Mengelola data ruangan dokter dan memastikan setiap dokter memiliki ruangan yang sesuai.
   - Schedule: CRUD jadwal dokter, pencarian jadwal, dan pengurutan menggunakan Quick Sort.

3. Zahran (Specialization & Doctor)
   - Specialization: Mengelola daftar spesialisasi dokter dan fitur pencarian berdasarkan spesialisasi.
   - Doctor: Menyimpan dan mengelola data dokter serta menghubungkannya dengan jadwal dan janji temu.
