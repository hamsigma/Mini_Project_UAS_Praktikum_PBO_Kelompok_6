"""
Main Application - Entry Point untuk Sistem Manajemen Dapur Umum. 
Orchestrator yang menghubungkan semua layer (Models, Repositories, Services).
"""

import logging
from datetime import datetime
import sys
import os

# Import repositories
from repositories.bahan_repository import BahanRepository
from repositories.korban_repository import KorbanRepository
from repositories.distribusi_repository import DistribusiRepository

# Import services
from services.dapur_service import DapurService

# Import models
from models.bahan_makanan import BahanPokok, BahanProtein, BahanSayuran
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
        logging.FileHandler('dapur_umum.log'),
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
        print("\n" + "="*60)
        print("🔄 LOADING DATA DUMMY... ". center(60))
        print("="*60)
        logger.info("Loading data dummy...")
        
        try:
            # BAHAN MAKANAN DUMMY
            print("\n📦 Menambahkan Bahan Makanan...")
            
            # 1. Beras
            print("   ⏳ Membuat object Beras...")
            beras = BahanPokok("Beras", 100.0, "kg", 250.0)
            print(f"   ✅ Object created:  {beras. get_nama()}, {beras.get_jumlah()} kg")
            
            print("   ⏳ Menambahkan Beras ke service...")
            self.dapur_service.tambah_bahan(beras)
            print(f"   ✅ Beras ditambahkan! Porsi: {beras.hitung_porsi()}")
            
            # 2. Ayam
            print("   ⏳ Membuat object Ayam...")
            ayam = BahanProtein("Ayam", 50.0, "kg", 0.15)
            print(f"   ✅ Object created: {ayam. get_nama()}, {ayam.get_jumlah()} kg")
            
            print("   ⏳ Menambahkan Ayam ke service...")
            self.dapur_service.tambah_bahan(ayam)
            print(f"   ✅ Ayam ditambahkan! Porsi: {ayam.hitung_porsi()}")
            
            # 3. Sayur
            print("   ⏳ Membuat object Sayur Kangkung...")
            sayur = BahanSayuran("Sayur Kangkung", 30.0, "kg", 0.1)
            print(f"   ✅ Object created: {sayur.get_nama()}, {sayur.get_jumlah()} kg")
            
            print("   ⏳ Menambahkan Sayur ke service...")
            self.dapur_service.tambah_bahan(sayur)
            print(f"   ✅ Sayur ditambahkan!  Porsi: {sayur.hitung_porsi()}")
            
            # Verifikasi
            print("\n🔍 Verifikasi Data Bahan...")
            total_bahan = len(self.bahan_repo. get_all())
            print(f"   📊 Total bahan di repository: {total_bahan}")
            
            if total_bahan == 0:
                print("   ⚠️ WARNING: Repository masih kosong!")
            else:
                print(f"   ✅ Bahan berhasil disimpan!")
                for bahan in self.bahan_repo.get_all():
                    print(f"      - {bahan.get_nama()}: {bahan.get_jumlah()} {bahan.get_satuan()}")
            
            # KORBAN DUMMY
            print("\n👥 Menambahkan Korban...")
            
            korban1 = Korban("Budi Santoso", "KRB-001", "Umum", 4)
            self.dapur_service.registrasi_korban(korban1)
            print(f"   ✅ {korban1.get_name()} terdaftar")
            
            korban2 = Korban("Siti Aminah", "KRB-002", "Lansia", 2)
            self.dapur_service.registrasi_korban(korban2)
            print(f"   ✅ {korban2.get_name()} terdaftar")
            
            korban3 = Korban("Ahmad Yani", "KRB-003", "Bayi", 3)
            self.dapur_service.registrasi_korban(korban3)
            print(f"   ✅ {korban3.get_name()} terdaftar")
            
            # Verifikasi korban
            total_korban = len(self. korban_repo.get_all())
            print(f"\n🔍 Verifikasi Data Korban...")
            print(f"   📊 Total korban di repository: {total_korban}")
            
            print("\n" + "="*60)
            print("✅ DATA DUMMY BERHASIL DIMUAT! ".center(60))
            print("="*60)
            logger.info("Data dummy berhasil dimuat")
            
        except Exception as e:
            print(f"\n❌ ERROR saat loading data dummy!")
            print(f"   Error: {e}")
            print(f"   Type: {type(e).__name__}")
            logger.error(f"Error loading data dummy:  {e}", exc_info=True)
            
            import traceback
            print("\n📋 Traceback:")
            traceback.print_exc()
    
    def tampilkan_menu_utama(self):
        """Menampilkan menu utama aplikasi."""
        print("\n" + "="*60)
        print("  SISTEM MANAJEMEN DAPUR UMUM & GIZI PENGUNGSI". center(60))
        print("="*60)
        print("1. 📦 Manajemen Bahan Makanan")
        print("2. 👥 Manajemen Data Korban")
        print("3. 🍽️ Distribusi Makanan")
        print("4. 📊 Laporan & Statistik")
        print("5. ⚕️ Cek Status Gizi")
        print("9. 🔧 Debug & Verifikasi Data")
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
            print(f"❌ Error:  {e}")
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
        print("\n🔍 Mengambil data bahan dari repository...")
        
        try:
            bahan_list = self.bahan_repo. get_all()
            print(f"   📊 Jumlah bahan ditemukan: {len(bahan_list)}")
            
            if not bahan_list: 
                print("\n" + "="*60)
                print("⚠️ BELUM ADA BAHAN MAKANAN TERDAFTAR")
                print("="*60)
                print("\n💡 Tips:")
                print("   - Silakan tambah bahan melalui menu 1, 2, atau 3")
                print("   - Data dummy seharusnya sudah dimuat saat startup")
                print("\n🔍 Debug:  Coba restart aplikasi atau tambah manual")
                return
            
            print(f"\n✅ Ditemukan {len(bahan_list)} bahan makanan:")
            data = [b.get_info() for b in bahan_list]
            print(format_laporan_tabel(data, "DAFTAR BAHAN MAKANAN"))
            
            # Tampilkan total porsi (Polymorphism in action!)
            print("🔄 Menghitung total porsi...")
            total_porsi = self.dapur_service.hitung_total_porsi_tersedia()
            print(f"\n📊 Total Porsi yang Dapat Dibuat: {total_porsi} porsi")
            
            # Detail per bahan
            print("\n📋 Detail Porsi Per Bahan:")
            for i, bahan in enumerate(bahan_list, 1):
                porsi = bahan.hitung_porsi()
                print(f"   {i}. {bahan.get_nama()}: {porsi} porsi")
            
            print()
            
        except Exception as e:
            print(f"\n❌ Error saat menampilkan bahan: {e}")
            logger.error(f"Error _lihat_semua_bahan: {e}", exc_info=True)
            import traceback
            traceback.print_exc()
    
    def _lihat_stok_rendah(self):
        """Menampilkan bahan dengan stok rendah."""
        stok_rendah = self.bahan_repo.get_stok_rendah(15.0)
        
        if not stok_rendah:
            print("\n✅ Semua bahan memiliki stok yang cukup!")
            return
        
        data = [b.get_info() for b in stok_rendah]
        print(format_laporan_tabel(data, "⚠️ BAHAN DENGAN STOK RENDAH"))
    
    def menu_manajemen_korban(self):
        """Menu untuk manajemen data korban."""
        while True:
            print("\n" + "="*60)
            print("MANAJEMEN DATA KORBAN".center(60))
            print("="*60)
            print("1. Registrasi Korban Baru")
            print("2. Lihat Semua Korban")
            print("3. Cari Korban by ID")
            print("4. Update Jumlah Tanggungan")
            print("0. Kembali")
            print("="*60)
            
            pilihan = input("Pilih menu: ")
            
            if pilihan == "1": 
                self._registrasi_korban()
            elif pilihan == "2":
                self._lihat_semua_korban()
            elif pilihan == "3":
                self._cari_korban()
            elif pilihan == "4":
                self._update_tanggungan()
            elif pilihan == "0":
                break
            else:
                print("❌ Pilihan tidak valid!")
    
    def _registrasi_korban(self):
        """Registrasi korban baru."""
        try:
            print("\n--- Registrasi Korban Baru ---")
            nama = input("Nama lengkap: ")
            id_korban = input("ID Korban (misal: KRB-004): ")
            
            print("\nKebutuhan Khusus:")
            print("1. Umum")
            print("2. Lansia")
            print("3. Bayi")
            print("4. Sakit")
            pilihan_kebutuhan = input("Pilih (1-4): ")
            
            kebutuhan_map = {"1": "Umum", "2": "Lansia", "3": "Bayi", "4": "Sakit"}
            kebutuhan = kebutuhan_map.get(pilihan_kebutuhan, "Umum")
            
            tanggungan = validasi_input_integer("Jumlah tanggungan (termasuk diri sendiri): ", 1)
            
            korban = Korban(nama, id_korban, kebutuhan, tanggungan)
            self.dapur_service.registrasi_korban(korban)
            
            print(f"✅ Korban {nama} berhasil diregistrasi!")
            print(f"   ID: {id_korban}")
            print(f"   Kebutuhan: {kebutuhan}")
            print(f"   Tanggungan: {tanggungan} orang")
        except Exception as e:
            print(f"❌ Error:  {e}")
            logger.error(f"Error registrasi korban: {e}")
    
    def _lihat_semua_korban(self):
        """Menampilkan semua korban."""
        korban_list = self.korban_repo.get_all()
        
        if not korban_list:
            print("\n⚠️ Belum ada korban terdaftar.")
            return
        
        data = [k.get_info() for k in korban_list]
        print(format_laporan_tabel(data, "DAFTAR KORBAN TERDAFTAR"))
        
        total_tanggungan = self.korban_repo.get_total_tanggungan()
        print(f"\n📊 Total Tanggungan: {total_tanggungan} orang\n")
    
    def _cari_korban(self):
        """Mencari korban berdasarkan ID."""
        try:
            id_korban = input("\nMasukkan ID Korban: ")
            korban = self.korban_repo. get_by_id(id_korban)
            
            if korban:
                print("\n" + "="*60)
                print("DATA KORBAN DITEMUKAN".center(60))
                print("="*60)
                print(korban.get_info())
                print("="*60)
            else:
                print(f"❌ Korban dengan ID {id_korban} tidak ditemukan.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _update_tanggungan(self):
        """Update jumlah tanggungan korban."""
        try:
            id_korban = input("\nMasukkan ID Korban: ")
            korban = self.korban_repo.get_by_id(id_korban)
            
            if not korban:
                print(f"❌ Korban dengan ID {id_korban} tidak ditemukan.")
                return
            
            print(f"\nKorban:  {korban.get_name()}")
            print(f"Tanggungan saat ini: {korban.get_jumlah_tanggungan()} orang")
            
            tanggungan_baru = validasi_input_integer("Jumlah tanggungan baru: ", 1)
            korban.set_jumlah_tanggungan(tanggungan_baru)
            
            print(f"✅ Tanggungan berhasil diupdate menjadi {tanggungan_baru} orang")
        except Exception as e:
            print(f"❌ Error:  {e}")
    
    def menu_distribusi(self):
        """Menu untuk distribusi makanan."""
        while True:
            print("\n" + "="*60)
            print("DISTRIBUSI MAKANAN".center(60))
            print("="*60)
            print("1. Distribusi Makanan ke Korban")
            print("2. Lihat Riwayat Distribusi")
            print("3. Lihat Riwayat Distribusi per Korban")
            print("0. Kembali")
            print("="*60)
            
            pilihan = input("Pilih menu: ")
            
            if pilihan == "1": 
                self._distribusi_makanan()
            elif pilihan == "2":
                self._lihat_riwayat_distribusi()
            elif pilihan == "3":
                self._lihat_riwayat_per_korban()
            elif pilihan == "0":
                break
            else:
                print("❌ Pilihan tidak valid!")
    
    def _distribusi_makanan(self):
        """Melakukan distribusi makanan."""
        try:
            print("\n--- Distribusi Makanan ---")
            
            # Tampilkan daftar korban
            korban_list = self.korban_repo.get_all()
            if not korban_list: 
                print("❌ Belum ada korban terdaftar!")
                return
            
            print("\nDaftar Korban:")
            for i, k in enumerate(korban_list, 1):
                print(f"{i}. {k.get_id()} - {k.get_name()} ({k.get_jumlah_tanggungan()} orang)")
            
            id_korban = input("\nMasukkan ID Korban: ")
            
            # Cek porsi tersedia
            porsi_tersedia = self.dapur_service. hitung_total_porsi_tersedia()
            print(f"\n📦 Porsi tersedia: {porsi_tersedia} porsi")
            
            jumlah_porsi = validasi_input_integer("Jumlah porsi yang akan didistribusikan: ", 1)
            
            # Distribusi
            distribusi = self.dapur_service.distribusi_makanan(id_korban, jumlah_porsi)
            
            print(f"\n✅ Distribusi berhasil!")
            print(f"   ID Distribusi: {distribusi.get_id_distribusi()}")
            print(f"   Korban: {id_korban}")
            print(f"   Porsi: {jumlah_porsi}")
            print(f"   Waktu: {distribusi.get_waktu_distribusi().strftime('%Y-%m-%d %H:%M')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            logger.error(f"Error distribusi:  {e}")
    
    def _lihat_riwayat_distribusi(self):
        """Menampilkan semua riwayat distribusi."""
        distribusi_list = self.distribusi_repo.get_all()
        
        if not distribusi_list:
            print("\n⚠️ Belum ada distribusi dilakukan.")
            return
        
        data = [d.get_info() for d in distribusi_list]
        print(format_laporan_tabel(data, "RIWAYAT DISTRIBUSI MAKANAN"))
        
        total_porsi = self.distribusi_repo.get_total_porsi_terdistribusi()
        print(f"\n📊 Total Porsi Terdistribusi: {total_porsi} porsi\n")
    
    def _lihat_riwayat_per_korban(self):
        """Menampilkan riwayat distribusi per korban."""
        try:
            id_korban = input("\nMasukkan ID Korban: ")
            riwayat = self.distribusi_repo.get_by_korban(id_korban)
            
            if not riwayat: 
                print(f"⚠️ Belum ada distribusi untuk korban {id_korban}")
                return
            
            data = [d.get_info() for d in riwayat]
            print(format_laporan_tabel(data, f"RIWAYAT DISTRIBUSI - {id_korban}"))
            
            total = sum(d.get_jumlah_porsi() for d in riwayat)
            print(f"\n📊 Total Porsi Diterima: {total} porsi\n")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def menu_laporan(self):
        """Menu untuk laporan dan statistik."""
        while True:
            print("\n" + "="*60)
            print("LAPORAN & STATISTIK".center(60))
            print("="*60)
            print("1. Laporan Stok Bahan")
            print("2. Laporan Data Korban")
            print("3. Laporan Distribusi")
            print("4. Laporan Lengkap (All-in-One)")
            print("0. Kembali")
            print("="*60)
            
            pilihan = input("Pilih menu: ")
            
            if pilihan == "1": 
                self._laporan_stok()
            elif pilihan == "2":
                self._laporan_korban()
            elif pilihan == "3":
                self._laporan_distribusi()
            elif pilihan == "4": 
                self._laporan_lengkap()
            elif pilihan == "0":
                break
            else:
                print("❌ Pilihan tidak valid!")
    
    def _laporan_stok(self):
        """Menampilkan laporan stok bahan."""
        laporan = self.dapur_service.get_laporan_stok()
        
        print("\n" + "="*60)
        print("LAPORAN STOK BAHAN MAKANAN".center(60))
        print("="*60)
        print(f"Total Jenis Bahan     : {laporan['total_jenis_bahan']}")
        print(f"Total Porsi Tersedia  : {laporan['total_porsi_tersedia']} porsi")
        print(f"Bahan Stok Rendah     : {laporan['bahan_stok_rendah']}")
        print("="*60)
        
        if laporan['detail_bahan']: 
            print("\nDetail Bahan:")
            for i, detail in enumerate(laporan['detail_bahan'], 1):
                print(f"{i}. {detail}")
        
        if laporan['warning_stok_rendah']:
            print("\n⚠️ WARNING - Stok Rendah:")
            for nama in laporan['warning_stok_rendah']:
                print(f"   - {nama}")
        
        print()
    
    def _laporan_korban(self):
        """Menampilkan laporan data korban."""
        laporan = self.dapur_service. get_laporan_korban()
        
        print("\n" + "="*60)
        print("LAPORAN DATA KORBAN".center(60))
        print("="*60)
        print(f"Total Korban Terdaftar : {laporan['total_korban']} orang")
        print(f"Total Tanggungan       : {laporan['total_tanggungan']} orang")
        print("="*60)
        
        if laporan['detail_korban']:
            print("\nDetail Korban:")
            for i, detail in enumerate(laporan['detail_korban'], 1):
                print(f"{i}.  {detail}")
        
        print()
    
    def _laporan_distribusi(self):
        """Menampilkan laporan distribusi."""
        laporan = self.dapur_service. get_laporan_distribusi()
        
        print("\n" + "="*60)
        print("LAPORAN DISTRIBUSI MAKANAN".center(60))
        print("="*60)
        print(f"Total Distribusi      : {laporan['total_distribusi']} kali")
        print(f"Total Porsi Tersalur  : {laporan['total_porsi_terdistribusi']} porsi")
        print("="*60)
        
        if laporan['detail_distribusi']:
            print("\nDetail Distribusi:")
            for i, detail in enumerate(laporan['detail_distribusi'], 1):
                print(f"{i}.  {detail}")
        
        print()
    
    def _laporan_lengkap(self):
        """Menampilkan laporan lengkap."""
        print("\n" + "="*70)
        print("LAPORAN LENGKAP SISTEM DAPUR UMUM".center(70))
        print("="*70)
        
        # Laporan Stok
        laporan_stok = self.dapur_service.get_laporan_stok()
        print("\n📦 STOK BAHAN MAKANAN")
        print("-" * 70)
        print(f"  Total Jenis Bahan    : {laporan_stok['total_jenis_bahan']}")
        print(f"  Total Porsi Tersedia :  {laporan_stok['total_porsi_tersedia']} porsi")
        print(f"  Bahan Stok Rendah    : {laporan_stok['bahan_stok_rendah']}")
        
        # Laporan Korban
        laporan_korban = self.dapur_service.get_laporan_korban()
        print("\n👥 DATA KORBAN")
        print("-" * 70)
        print(f"  Total Korban         : {laporan_korban['total_korban']} orang")
        print(f"  Total Tanggungan     : {laporan_korban['total_tanggungan']} orang")
        
        # Laporan Distribusi
        laporan_dist = self.dapur_service. get_laporan_distribusi()
        print("\n🍽️ DISTRIBUSI MAKANAN")
        print("-" * 70)
        print(f"  Total Distribusi     :  {laporan_dist['total_distribusi']} kali")
        print(f"  Total Porsi Tersalur : {laporan_dist['total_porsi_terdistribusi']} porsi")
        
        # Status Gizi
        status = self.dapur_service.cek_kebutuhan_gizi()
        print("\n⚕️ STATUS KEBUTUHAN GIZI")
        print("-" * 70)
        print(f"  Kebutuhan Harian     : {status['kebutuhan_harian']} porsi")
        print(f"  Estimasi Bertahan    : {status['estimasi_hari']} hari")
        print(f"  Status               : {status['status']}")
        
        print("="*70)
        print()
    
    def menu_cek_gizi(self):
        """Menu untuk cek status kebutuhan gizi."""
        print("\n")
        status = self.dapur_service. cek_kebutuhan_gizi()
        print(format_status_gizi(status))
        
        # Rekomendasi berdasarkan status
        if status['status'] == 'KRITIS':
            print("⚠️ REKOMENDASI:")
            print("   - Segera lakukan pengadaan bahan makanan!")
            print("   - Hubungi tim logistik untuk bantuan tambahan")
            print("   - Prioritaskan distribusi untuk kebutuhan khusus (lansia, bayi)")
        elif status['status'] == 'WASPADA':
            print("⚠️ REKOMENDASI:")
            print("   - Rencanakan pengadaan dalam 2-3 hari ke depan")
            print("   - Monitor konsumsi harian")
        else:
            print("✅ Status AMAN - Stok mencukupi untuk saat ini")
        
        input("\nTekan Enter untuk kembali...")
    
    def menu_debug(self):
        """Menu debug untuk troubleshooting."""
        print("\n" + "="*60)
        print("DEBUG & VERIFIKASI DATA".center(60))
        print("="*60)
        
        try:
            # 1. Cek bahan
            print("\n📦 STATUS BAHAN MAKANAN:")
            all_bahan = self.bahan_repo.get_all()
            print(f"   Total bahan: {len(all_bahan)}")
            
            if all_bahan:
                for i, b in enumerate(all_bahan, 1):
                    print(f"   {i}. {b. get_nama()}:  {b.get_jumlah()} {b.get_satuan()} → {b.hitung_porsi()} porsi")
            else:
                print("   ⚠️ Repository kosong!")
            
            # 2. Cek korban
            print("\n👥 STATUS KORBAN:")
            all_korban = self.korban_repo.get_all()
            print(f"   Total korban: {len(all_korban)}")
            
            if all_korban:
                for i, k in enumerate(all_korban, 1):
                    print(f"   {i}. {k.get_id()}: {k.get_name()} ({k.get_jumlah_tanggungan()} orang)")
            else:
                print("   ⚠️ Repository kosong!")
            
            # 3. Cek distribusi
            print("\n🍽️ STATUS DISTRIBUSI:")
            all_dist = self.distribusi_repo.get_all()
            print(f"   Total distribusi:  {len(all_dist)}")
            
            # 4. Test tambah bahan manual
            print("\n🧪 TEST:  Tambah Bahan Manual")
            test_choice = input("Mau coba tambah bahan test? (y/n): ")
            
            if test_choice.lower() == 'y':
                test_bahan = BahanPokok("Test Beras", 10.0, "kg", 250.0)
                print(f"   Object created: {test_bahan. get_nama()}")
                
                self.dapur_service.tambah_bahan(test_bahan)
                print(f"   ✅ Berhasil ditambahkan!")
                
                # Verifikasi
                verify = self.bahan_repo.get_by_id("Test Beras")
                if verify:
                    print(f"   ✅ Verifikasi OK: {verify.get_nama()} ada di repository")
                else: 
                    print(f"   ❌ Verifikasi GAGAL: tidak ditemukan di repository")
            
            print("\n" + "="*60)
            
        except Exception as e:
            print(f"❌ Error di debug menu: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nTekan Enter untuk kembali...")
    
    def run(self):
        """Main loop aplikasi."""
        print("\n")
        print("="*60)
        print("🏕️ SELAMAT DATANG". center(60))
        print("SISTEM MANAJEMEN DAPUR UMUM & GIZI PENGUNGSI". center(60))
        print("="*60)
        print("\n✅ Sistem berhasil diinisialisasi")
        print("✅ Data dummy telah dimuat")
        print("\nTekan Enter untuk melanjutkan...")
        input()
        
        while True: 
            try:
                self.tampilkan_menu_utama()
                pilihan = input("\nPilih menu (0-5, 9): ")
                
                if pilihan == "1":
                    self.menu_manajemen_bahan()
                elif pilihan == "2":
                    self. menu_manajemen_korban()
                elif pilihan == "3":
                    self.menu_distribusi()
                elif pilihan == "4":
                    self. menu_laporan()
                elif pilihan == "5":
                    self. menu_cek_gizi()
                elif pilihan == "9":
                    self.menu_debug()
                elif pilihan == "0":
                    print("\n" + "="*60)
                    print("Terima kasih telah menggunakan sistem! ".center(60))
                    print("Program selesai. ".center(60))
                    print("="*60)
                    logger.info("Sistem ditutup oleh user")
                    break
                else:
                    print("\n❌ Pilihan tidak valid!  Silakan pilih 0-5 atau 9.")
                    input("Tekan Enter untuk melanjutkan...")
            
            except KeyboardInterrupt: 
                print("\n\n⚠️ Program dihentikan oleh user (Ctrl+C)")
                logger.warning("Program dihentikan dengan Ctrl+C")
                break
            except Exception as e:
                print(f"\n❌ Terjadi error: {e}")
                logger.error(f"Error di main loop: {e}", exc_info=True)
                import traceback
                traceback.print_exc()
                input("Tekan Enter untuk melanjutkan...")


def main():
    """Entry point utama aplikasi."""
    try:
        app = DapurUmumApp()
        app.run()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        logger.critical(f"Fatal error saat startup: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()