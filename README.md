# 🏕️ Sistem Manajemen Dapur Umum & Gizi Pengungsi

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Academic-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-success)](https://github.com)

Aplikasi berbasis Command Line Interface (CLI) untuk mengelola dapur umum dan kebutuhan gizi pengungsi bencana alam di Indonesia.  Dibangun dengan menerapkan konsep **Object-Oriented Programming (OOP)** dan **Layered Architecture**. 

---

## Kelompok 6 
# Ilham Ramadhani - 2411102441066
# Alil Akbar - 24111102441067 
# Jeremy Christian Thio - 2411102441317
# M. Nabil Syafiq - 2411102441110
# M. Bintang Novariansyah - 2411102441245 
# Fatwa Ikhwan Maulaya - 2411102441063
# M. Zaky Vierrzady - 2411102441166

---

## 📋 **Daftar Isi**

- [Tentang Proyek](#tentang-proyek)
- [Struktur Folder](#struktur-folder)
- [Fitur Utama](#fitur-utama)
- [Arsitektur Sistem](#arsitektur-sistem)
- [Konsep OOP](#konsep-oop-yang-diterapkan)
- [SOLID Principles](#solid-principles)
- [Relasi UML](#relasi-uml)
- [Cara Menggunakan](#cara-menggunakan)
- [Alur Sistem](#alur-sistem)
- [Testing](#testing)
- [Instalasi](#instalasi)
---

## 🎯 **Tentang Proyek**

### **Latar Belakang**

Indonesia sering mengalami bencana alam yang mengakibatkan banyak korban membutuhkan bantuan darurat, khususnya kebutuhan pangan.  Pengelolaan dapur umum yang efektif dan terdata dengan baik sangat penting untuk memastikan distribusi makanan yang merata dan mencukupi kebutuhan gizi pengungsi. Adapun mini project ini untuk menyelesaikan tugas akhir matakuliah Prktikum Pemrograman Berorientasi Objek.

### **Tujuan**

- ✅ Mengelola inventori bahan makanan secara real-time
- ✅ Mencatat data korban dan kebutuhan khusus mereka
- ✅ Melakukan distribusi makanan yang terdata
- ✅ Monitoring status kebutuhan gizi (AMAN/WASPADA/KRITIS)
- ✅ Menghasilkan laporan untuk pengambilan keputusan

### **Teknologi**

- **Bahasa**: Python 3.8+
- **Paradigma**: Object-Oriented Programming (OOP)
- **Arsitektur**: Layered Architecture
- **Testing**: unittest
- **Logging**: logging module

---

UAS_Enviro_Kelompok_6/
│
├── models/                      # DATA LAYER
│   ├── __init__.py
│   ├── person.py                # Person, Korban, Relawan
│   ├── bahan_makanan.py         # BahanMakanan hierarchy
│   └── distribusi.py            # DistribusiMakanan
│
├── repositories/                # DATA ACCESS LAYER
│   ├── __init__.py
│   ├── base_repository.py       # IRepository interface (DIP)
│   ├── korban_repository.py
│   ├── bahan_repository.py
│   └── distribusi_repository.py
│
├── services/                    # BUSINESS LOGIC LAYER
│   ├── __init__.py
│   └── dapur_service.py         # Core business logic
│
├── utils/                       # UTILITY LAYER
│   ├── __init__.py
│   └── formatter.py             # Helper functions
│
├── tests/                       # UNIT TESTING
│   ├── __init__.py
│   ├── test_person.py
│   ├── test_bahan_makanan. py
│   ├── test_repositories.py
│   ├── test_dapur_service.py
│   └── run_all_tests.py
│
├── main.py                      # ENTRY POINT
├── README.md                    # Dokumentasi (file ini)
├── requirements.txt             # Dependencies
├── . gitignore
└── dapur_umum. log              # Log file (auto-generated)

---

## 🚀 **Fitur Utama**

### **1. Manajemen Bahan Makanan** 📦
- Tambah bahan makanan (Pokok, Protein, Sayuran)
- Monitoring stok real-time dengan kalkulasi porsi otomatis
- Alert untuk stok rendah
- Riwayat tanggal masuk bahan

### **2. Manajemen Data Korban** 👥
- Registrasi korban dengan data lengkap
- Kategori kebutuhan khusus (Umum, Lansia, Bayi, Sakit)
- Tracking jumlah tanggungan per keluarga
- Pencarian korban berdasarkan ID

### **3. Distribusi Makanan** 🍽️
- Distribusi makanan dengan validasi stok
- Pencatatan timestamp otomatis
- Riwayat distribusi per korban
- Tracking total porsi terdistribusi

### **4. Laporan & Statistik** 📊
- Laporan stok bahan makanan
- Laporan data korban dan tanggungan
- Laporan distribusi makanan
- Dashboard lengkap

### **5. Analisis Status Gizi** ⚕️
- Kalkulasi kebutuhan harian (3x makan/hari)
- Estimasi berapa hari stok bertahan
- Status:  AMAN (≥7 hari) | WASPADA (3-6 hari) | KRITIS (<3 hari)
- Rekomendasi tindakan otomatis

---

## 🏗️ **Arsitektur Sistem**

Sistem menggunakan **Layered Architecture** dengan pemisahan tanggung jawab yang jelas:

PRESENTATION LAYER (main.py) - Menu navigation - User input handling - Output formatting | v BUSINESS LOGIC LAYER (services/) - DapurService - Business rules & validations - Orchestration | v DATA ACCESS LAYER (repositories/) - IRepository (Interface) - KorbanRepository - BahanRepository - DistribusiRepository | v DATA LAYER (models/) - Person, Korban, Relawan - BahanMakanan, BahanPokok, BahanProtein, BahanSayuran - DistribusiMakanan

### **Penjelasan Layer**

| Layer | Tanggung Jawab | File/Folder |
|-------|---------------|-------------|
| **Presentation** | UI/CLI, input/output | `main.py` |
| **Business Logic** | Logika bisnis, validasi | `services/` |
| **Data Access** | CRUD operations | `repositories/` |
| **Data** | Entitas, enkapsulasi | `models/` |
| **Utility** | Helper functions | `utils/` |

---

## 🎓 **Konsep OOP yang Diterapkan**

### **1. Class & Object**
Representasi entitas nyata (Korban, BahanMakanan, Distribusi) menjadi class dengan atribut dan method yang relevan.

### **2. Enkapsulasi**
- Semua atribut vital bersifat **private** (`__nama`, `__jumlah`)
- Akses melalui **getter/setter** dengan validasi
- Melindungi integritas data dari perubahan tidak sah

### **3. Inheritance**
- Hubungan **"is-a"**
- Menghindari duplikasi kode

**Hirarki:**
Person ---> Korban ---> Relawan
BahanMakanan ---> BahanPokok ---> BahanProtein ---> BahanSayuran
Person (Abstract) |---> Korban (Inheritance) |---> Relawan (Inheritance)
BahanMakanan (Abstract) |---> BahanPokok (Inheritance) |---> BahanProtein (Inheritance) |---> BahanSayuran (Inheritance)
IRepository<T> (Interface) |---> KorbanRepository (Realization) |---> BahanRepository (Realization) |---> DistribusiRepository (Realization)
DapurService |---> IRepository<BahanMakanan> (Composition) |---> IRepository<Korban> (Composition) |---> IRepository<DistribusiMakanan> (Composition)


### **Jenis Relasi**

| Relasi | Symbol | Contoh |
|--------|--------|--------|
| **Inheritance** | ---> | Person ---> Korban |
| **Composition** | ---> | DapurService ---> Repository |
| **Dependency** | ---> | DapurService ---> Models |
| **Realization** | ---> | IRepository ---> KorbanRepository |

---

## 🔄 **Alur Sistem**

### **1. Alur Umum Aplikasi**
START | |---> main.py (Inisialisasi) | | | |---> Buat Repositories | |---> Buat DapurService (inject repositories) | |---> Load data dummy | |---> Tampilkan Menu Utama | |---> User Input Pilihan Menu | | | |---> [1] Manajemen Bahan ---> menu_manajemen_bahan() | |---> [2] Manajemen Korban ---> menu_manajemen_korban() | |---> [3] Distribusi ---> menu_distribusi() | |---> [4] Laporan ---> menu_laporan() | |---> [5] Cek Gizi ---> menu_cek_gizi() | |---> [0] Keluar ---> EXIT | |---> Proses Menu yang Dipilih |---> Kembali ke Menu Utama | END

### **2. Alur Tambah Bahan Makanan**
User pilih menu "Tambah Bahan Pokok" | |---> main.py._tambah_bahan_pokok() | | | |---> Input: nama bahan | |---> Input: jumlah (kg) | |---> Input: gram per porsi | | | |---> Validasi input (utils.validasi_input_angka) | | | |---> Buat object BahanPokok | |---> DapurService. tambah_bahan(bahan) | | | |---> Validasi: jumlah > 0? | | |---> Jika TIDAK ---> raise ValueError | | |---> Jika YA ---> lanjut | | | |---> BahanRepository.add(bahan) | | | | | |---> Cek: bahan sudah ada? | | | |---> Jika YA ---> tambah stok | | | |---> Jika TIDAK ---> simpan baru | | | |---> Logging: "Bahan X berhasil ditambahkan" | | | |---> Check: stok < 20? | |---> Jika YA ---> Warning log | |---> Tampilkan konfirmasi ke user | | | |---> "✅ Bahan X berhasil ditambahkan!" | |---> "Dapat membuat: Y porsi" | |---> Kembali ke menu

### **3. Alur Registrasi Korban**
User pilih menu "Registrasi Korban Baru" | |---> main.py._registrasi_korban() | | | |---> Input: nama lengkap | |---> Input: ID korban | |---> Pilih: kebutuhan khusus (1-4) | |---> Input: jumlah tanggungan | | | |---> Validasi input (utils.validasi_input_integer) | | | |---> Buat object Korban | |---> DapurService.registrasi_korban(korban) | | | |---> Validasi: ID sudah ada? | | |---> Jika YA ---> raise ValueError | | |---> Jika TIDAK ---> lanjut | | | |---> KorbanRepository.add(korban) | | | | | |---> Simpan ke storage (dictionary) | | | |---> Logging: "Korban X berhasil diregistrasi" | |---> Tampilkan konfirmasi ke user | | | |---> "✅ Korban X berhasil diregistrasi!" | |---> "ID: KRB-XXX" | |---> "Kebutuhan: Umum" | |---> "Tanggungan: 4 orang" | |---> Kembali ke menu

### **4. Alur Distribusi Makanan**
User pilih menu "Distribusi Makanan ke Korban" | |---> main.py._distribusi_makanan() | | | |---> Tampilkan daftar korban | |---> Input: ID korban | |---> Tampilkan porsi tersedia | |---> Input: jumlah porsi | |---> DapurService.distribusi_makanan(id_korban, jumlah_porsi) | | | |---> Step 1: Validasi korban ada? | | | | | |---> KorbanRepository.get_by_id(id) | | |---> Jika TIDAK ada ---> raise ValueError | | | |---> Step 2: Hitung porsi tersedia | | | | | |---> DapurService.hitung_total_porsi_tersedia() | | | | | | | |---> BahanRepository.get_all() | | | |---> Loop setiap bahan: | | | | |---> bahan.hitung_porsi() (POLYMORPHISM) | | | |---> Return min(porsi_list) | | | | | |---> Validasi: porsi diminta > tersedia? | | |---> Jika YA ---> raise ValueError | | | |---> Step 3: Kurangi stok bahan | | | | | |---> Cari BahanPokok | | |---> Hitung kebutuhan (porsi × 0.25 kg) | | |---> bahan.kurangi_stok(jumlah) | | | |---> Step 4: Buat distribusi | | | | | |---> Generate ID: "DIST-timestamp-id_korban" | | |---> Buat object DistribusiMakanan | | |---> DistribusiRepository.add(distribusi) | | | |---> Logging: "Distribusi berhasil" | | | |---> Return object distribusi | |---> Tampilkan konfirmasi ke user | | | |---> "✅ Distribusi berhasil!" | |---> "ID Distribusi: DIST-XXX" | |---> "Korban: KRB-001" | |---> "Porsi: 10" | |---> "Waktu: 2025-12-30 12:30" | |---> Kembali ke menu

### **5. Alur Cek Status Gizi**
User pilih menu "Cek Status Gizi" | |---> main.py. menu_cek_gizi() | | | |---> DapurService.cek_kebutuhan_gizi() | |---> DapurService.cek_kebutuhan_gizi() | | | |---> Step 1: Ambil total tanggungan | | |---> KorbanRepository.get_total_tanggungan() | | | |---> Step 2: Hitung porsi tersedia | | |---> DapurService.hitung_total_porsi_tersedia() | | | |---> Step 3: Kalkulasi kebutuhan | | |---> kebutuhan_harian = tanggungan × 3 | | |---> estimasi_hari = porsi_tersedia ÷ kebutuhan_harian | | | |---> Step 4: Tentukan status | | |---> Jika hari ≥ 7 ---> Status = "AMAN" | | |---> Jika hari 3-6 ---> Status = "WASPADA" | | |---> Jika hari < 3 ---> Status = "KRITIS" | | | |---> Return dictionary hasil | |---> Format output (utils.format_status_gizi) | | | |---> Tampilkan laporan dengan color coding | |---> Tampilkan rekomendasi berdasarkan status | |---> Kembali ke menu

### **6. Alur Lihat Semua Bahan (Polymorphism in Action)**
User pilih menu "Lihat Semua Bahan" | |---> main.py._lihat_semua_bahan() | | | |---> BahanRepository.get_all() | | | | | |---> Return list semua bahan | | | |---> Loop setiap bahan: | | | | | |---> bahan.get_info() ---> tampilkan info | | |---> bahan.hitung_porsi() ---> POLYMORPHISM! | | | | | |---> Jika BahanPokok: | | | |---> Konversi kg ke gram | | | |---> Bagi dengan gram_per_porsi | | | | | |---> Jika BahanProtein: | | | |---> Bagi langsung dengan unit_per_porsi | | | | | |---> Jika BahanSayuran: | | |---> Bagi langsung dengan kg_per_porsi | | | |---> DapurService.hitung_total_porsi_tersedia() | | | | | |---> Return minimum porsi (bottleneck) | | | |---> Tampilkan summary | |---> Kembali ke menu

### **7. Alur Laporan Lengkap**
User pilih menu "Laporan Lengkap" | |---> main.py._laporan_lengkap() | | | |---> DapurService.get_laporan_stok() | | |---> Aggregate data bahan | | |---> Hitung total porsi | | |---> Check stok rendah | | | |---> DapurService.get_laporan_korban() | | |---> Aggregate data korban | | |---> Hitung total tanggungan | | | |---> DapurService.get_laporan_distribusi() | | |---> Aggregate data distribusi | | |---> Hitung total porsi terdistribusi | | | |---> DapurService.cek_kebutuhan_gizi() | | |---> Kalkulasi status gizi | | | |---> Format dan tampilkan semua data | |---> Kembali ke menu

---

### **Langkah Instalasi**
Sistem dilengkapi dengan 40+ unit tests untuk memastikan reliability.

# Run semua tests
python tests/run_all_tests.py

# Run test spesifik
python -m unittest tests.test_person
python -m unittest tests.test_bahan_makanan
python -m unittest tests.test_repositories
python -m unittest tests.test_dapur_service

# Run dengan verbose
python -m unittest tests. test_person -v
---
## 💻 **Instalasi**

### **Prerequisites**

- Python 3.8 atau lebih baru
- pip (Python package manager)
- Git (optional)

### **Langkah Instalasi**

```bash
# 1. Clone repository
git clone https://github.com/username/UAS_Enviro_Kelompok_6.git
cd UAS_Enviro_Kelompok_6

# 2. (Optional) Buat virtual environment
python -m venv venv

# Activate di Windows
venv\Scripts\activate

# Activate di Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
# Note: Project ini hanya menggunakan Python standard library

---

