"""
Main Application - Entry Point untuk Sistem Manajemen Dapur Umum.
Orchestrator yang menghubungkan semua layer (Models, Repositories, Services).
"""

import logging
from datetime import datetime

# Import repositories
from repositories.bahan_repository import BahanRepository
from repositories.korban_repository import KorbanRepository
from repositories.distribusi_repository import DistribusiRepository

# Import services
from services.dapur_service import DapurService

# Import models
from models. bahan_makanan import BahanPokok, BahanProtein, BahanSayuran
from models.person import Korban, Relawan

# Import utils
from utils.formatter import (
    format_laporan_tabel, format_status_gizi, 
    validasi_input_angka, validasi_input_integer, buat_id_unik
)


# Setup logging (Modul 12)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging. FileHandler('dapur_umum.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class DapurUmumApp:
    """
    Main Application Class - Orchestrator untuk seluruh sistem.
    Menerapkan Layered Architecture dan Dependency Injection.
    """
    
    def __init__(self):
        """Constructor - inisialisasi semua dependencies."""
        logger.info("="*60)
        logger.info("Sistem Manajemen Dapur Umum & Gizi Pengungsi DIMULAI")
        logger.info("="*60)
        
        # Inisialisasi Repositories (Data Layer)
        self.bahan_repo = BahanRepository()
        self.korban_repo = KorbanRepository()
        self.distribusi_repo = DistribusiRepository()
        
        # Inisialisasi Service dengan Dependency Injection (DIP)
        self.dapur_service = DapurService(
            self.bahan_repo,
            self.korban_repo,
            self.distribusi_repo
        )
        
        # Load data dummy untuk testing
        self._load_data_dummy()
    
    def _load_data_dummy(self):
        """Load data dummy untuk keperluan demo."""
        logger.info("Loading data dummy...")
        
        try:
            # Tambah bahan makanan dummy
            beras = BahanPokok("Beras", 100.0, "kg", 250.0)
            ayam = BahanProtein("Ayam", 50.0, "kg", 0.15)
            sayur = BahanSayuran("Sayur Kangkung", 30.0, "kg", 0.1)
            
            self.dapur_service.tambah_bahan(beras)
            self.dapur_service.tambah_bahan(ayam)
            self.dapur_service. tambah_bahan(sayur)
            
            # Registrasi korban dummy
            korban1 = Korban("Budi Santoso", "KRB-001", "Umum", 4)
            korban2 = Korban("Siti Aminah", "KRB-002", "Lansia", 2)
            korban3 = Korban("Ahmad Yani", "KRB-003", "Bayi", 3)
            
            self.dapur_service.registrasi_korban(korban1)
            self.dapur_service. registrasi_korban(korban2)
            self.dapur_service.registrasi_korban(korban3)
            
            logger.info("Data dummy berhasil dimuat")
        except Exception as e:
            logger.error(f"Error loading data dummy: {e}")
    
    def tampilkan_menu_utama(self):
        """Menampilkan menu utama aplikasi."""
        print("\n" + "="*60)
        print("  SISTEM MANAJEMEN DAPUR UMUM & GIZI PENGUNGSI". center(60))
        print("="*60)
        print("1. 📦 Manajemen Bahan Makanan")
        print("2. 👥 Manajemen Data Korban")
        print("3. 🍽️  Distribusi Makanan")
        print("4. 📊 Laporan & Statistik")
        print("5. ⚕️  Cek Status Gizi")
        print("0. 🚪 Keluar")
        print("="*60)
    
    def menu_manajemen_bahan(self):
        """Menu untuk manajemen bahan makanan."""
        while True:
            print("\n" + "="*60)
            print("MANAJEMEN BAHAN MAKANAN".center(60))
            print("="*60)
            print("1. Tambah Bahan Pokok")
            print("2. Tambah Bahan Protein")
            print("3. Tambah Bahan Sayuran")
            print("4. Lihat Semua Bahan")
            print("5. Lihat Bahan Stok Rendah")
            print("0. Kembali")
            print("="*60)
            
            pilihan = input("Pilih menu:  ")
            
            if pilihan == "1":
                self._tambah_bahan_pokok()
            elif pilihan == "2":
                self._tambah_bahan_protein()
            elif pilihan == "3": 
                self._tambah_bahan_sayuran()
            elif pilihan == "4":
                self._lihat_semua_bahan()
            elif pilihan == "5":
                self._lihat_stok_rendah()
            elif pilihan == "0":
                break
            else:
                print("❌ Pilihan tidak valid!")
    
    def _tambah_bahan_pokok(self):
        """Menambah bahan pokok."""
        try:
            print("\n--- Tambah Bahan Pokok ---")
            nama = input("Nama bahan (misal: Beras, Mie Instan): ")
            jumlah = validasi_input_angka("Jumlah (kg): ", 0.1)
            gram_per_porsi = validasi_input_angka("Gram per porsi (default 250g): ", 50)
            
            bahan = BahanPokok(nama, jumlah, "kg", gram_per_porsi)
            self.dapur_service.tambah_bahan(bahan)
            
            print(f"✅ Bahan {nama} berhasil ditambahkan!")
            print(f"   Dapat membuat:  {bahan.hitung_porsi()} porsi")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error tambah bahan pokok: {e}")
    
    def _tambah_bahan_protein(self):
        """Menambah bahan protein."""
        try:
            print("\n--- Tambah Bahan Protein ---")
            nama = input("Nama bahan (misal: Ayam, Telur, Ikan): ")
            jumlah = validasi_input_angka("Jumlah (kg): ", 0.1)
            kg_per_porsi = validasi_input_angka("Kg per porsi (default 0.15): ", 0.05)
            
            bahan = BahanProtein(nama, jumlah, "kg", kg_per_porsi)
            self.dapur_service.tambah_bahan(bahan)
            
            print(f"✅ Bahan {nama} berhasil ditambahkan!")
            print(f"   Dapat membuat: {bahan.hitung_porsi()} porsi")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error tambah bahan protein: {e}")
    
    def _tambah_bahan_sayuran(self):
        """Menambah bahan sayuran."""
        try:
            print("\n--- Tambah Bahan Sayuran ---")
            nama = input("Nama bahan (misal: Kangkung, Bayam): ")
            jumlah = validasi_input_angka("Jumlah (kg): ", 0.1)
            kg_per_porsi = validasi_input_angka("Kg per porsi (default 0.1): ", 0.05)
            
            bahan = BahanSayuran(nama, jumlah, "kg", kg_per_porsi)
            self.dapur_service.tambah_bahan(bahan)
            
            print(f"✅ Bahan {nama} berhasil ditambahkan!")
            print(f"   Dapat membuat: {bahan.hitung_porsi()} porsi")
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error tambah bahan sayuran: {e}")
    
    def _lihat_semua_bahan(self):
        """Menampilkan semua bahan."""
        bahan_list = self.bahan_repo.get_all()
        
        if not bahan_list:
            print("\n⚠️  Belum ada bahan makanan terdaftar.")
            return
        
        data = [b.get_info() for b in bahan_list]
        print(format_laporan_tabel(data, "DAFTAR BAHAN MAKANAN"))
        
        # Tampilkan total porsi (Polymorphism in action!)
        total_porsi = self.dapur_service.hitung_total_porsi_tersedia()
        print(f"\n📊 Total Porsi yang Dapat Dibuat: {total_porsi} porsi\n")
    
    def _lihat_stok_rendah(self):
        """Menampilkan bahan dengan stok rendah."""
        stok_rendah = self.bahan_repo.get_stok_rendah(15.0)
        
        if not stok_rendah:
            print("\n✅ Semua bahan memiliki stok yang cukup!")
            return
        
        data = [b. get_info() for b in stok_rendah]
        print(format_laporan_tabel(data, "⚠️  BAHAN DENGAN STOK RENDAH"))
    
    def menu_manajemen_korban(self):
        """Menu untuk manajemen data korban."""
        while True:
            print("\n" + "="*60)
            print("MANAJEMEN DATA KORBAN".center(60))
            print("="*60)
            