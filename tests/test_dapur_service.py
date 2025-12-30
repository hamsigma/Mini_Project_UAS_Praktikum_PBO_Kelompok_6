"""
Unit Testing untuk services/dapur_service. py
Testing Business Logic Layer
"""

import unittest
from services.dapur_service import DapurService
from repositories.bahan_repository import BahanRepository
from repositories.korban_repository import KorbanRepository
from repositories.distribusi_repository import DistribusiRepository
from models.bahan_makanan import BahanPokok, BahanProtein
from models.person import Korban


class TestDapurService(unittest.TestCase):
    """Test case untuk DapurService"""
    
    def setUp(self):
        """Setup service dengan dependencies"""
        self.bahan_repo = BahanRepository()
        self.korban_repo = KorbanRepository()
        self.distribusi_repo = DistribusiRepository()
        
        self.service = DapurService(
            self.bahan_repo,
            self.korban_repo,
            self.distribusi_repo
        )
    
    def test_tambah_bahan_valid(self):
        """Test menambah bahan melalui service"""
        beras = BahanPokok("Beras", 100.0, "kg", 250.0)
        self.service.tambah_bahan(beras)
        
        retrieved = self.bahan_repo.get_by_id("Beras")
        self.assertIsNotNone(retrieved)
    
    def test_tambah_bahan_invalid_jumlah(self):
        """Test menambah bahan dengan jumlah invalid"""
        beras = BahanPokok("Beras", 0.0, "kg", 250.0)
        
        with self.assertRaises(ValueError):
            self.service. tambah_bahan(beras)
    
    def test_registrasi_korban_valid(self):
        """Test registrasi korban"""
        korban = Korban("Budi", "KRB-001", "Umum", 4)
        self.service.registrasi_korban(korban)
        
        retrieved = self.korban_repo.get_by_id("KRB-001")
        self.assertIsNotNone(retrieved)
    
    def test_registrasi_korban_duplicate(self):
        """Test registrasi korban dengan ID duplikat"""
        korban = Korban("Budi", "KRB-001", "Umum", 4)
        self.service.registrasi_korban(korban)
        
        with self.assertRaises(ValueError):
            self.service.registrasi_korban(korban)
    
    def test_hitung_total_porsi_tersedia(self):
        """Test kalkulasi porsi tersedia (Polymorphism)"""
        beras = BahanPokok("Beras", 100.0, "kg", 250.0)  # 400 porsi
        ayam = BahanProtein("Ayam", 50.0, "kg", 0.15)   # 333 porsi
        
        self.service.tambah_bahan(beras)
        self.service.tambah_bahan(ayam)
        
        total_porsi = self.service.hitung_total_porsi_tersedia()
        # Harus ambil minimum = 333
        self.assertEqual(total_porsi, 333)
    
    def test_distribusi_makanan_valid(self):
        """Test distribusi makanan"""
        # Setup: tambah bahan dan korban
        beras = BahanPokok("Beras", 100.0, "kg", 250.0)
        self.service.tambah_bahan(beras)
        
        korban = Korban("Budi", "KRB-001", "Umum", 4)
        self.service. registrasi_korban(korban)
        
        # Distribusi
        distribusi = self.service.distribusi_makanan("KRB-001", 10)
        
        self.assertIsNotNone(distribusi)
        self.assertEqual(distribusi.get_jumlah_porsi(), 10)
    
    def test_distribusi_makanan_korban_not_found(self):
        """Test distribusi ke korban yang tidak ada"""
        beras = BahanPokok("Beras", 100.0, "kg", 250.0)
        self.service.tambah_bahan(beras)
        
        with self.assertRaises(ValueError):
            self.service.distribusi_makanan("KRB-999", 10)
    
    def test_distribusi_makanan_stok_tidak_cukup(self):
        """Test distribusi melebihi stok tersedia"""
        beras = BahanPokok("Beras", 1.0, "kg", 250.0)  # Hanya 4 porsi
        self.service.tambah_bahan(beras)
        
        korban = Korban("Budi", "KRB-001", "Umum", 4)
        self.service.registrasi_korban(korban)
        
        with self. assertRaises(ValueError):
            self.service.distribusi_makanan("KRB-001", 100)  # Minta 100 porsi
    
    def test_get_laporan_stok(self):
        """Test generate laporan stok"""
        beras = BahanPokok("Beras", 100.0, "kg", 250.0)
        self.service.tambah_bahan(beras)
        
        laporan = self.service.get_laporan_stok()
        
        self.assertEqual(laporan['total_jenis_bahan'], 1)
        self.assertGreater(laporan['total_porsi_tersedia'], 0)
    
    def test_cek_kebutuhan_gizi(self):
        """Test analisis kebutuhan gizi"""
        beras = BahanPokok("Beras", 100.0, "kg", 250.0)  # 400 porsi
        self.service.tambah_bahan(beras)
        
        korban = Korban("Budi", "KRB-001", "Umum", 4)  # 4 orang
        self.service.registrasi_korban(korban)
        
        status = self.service.cek_kebutuhan_gizi()
        
        self.assertEqual(status['total_tanggungan'], 4)
        self.assertEqual(status['kebutuhan_harian'], 12)  # 4 * 3
        self.assertIn(status['status'], ['AMAN', 'WASPADA', 'KRITIS'])


if __name__ == '__main__':
    unittest.main()