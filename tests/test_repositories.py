"""
Unit Testing untuk repositories
Testing KorbanRepository, BahanRepository, DistribusiRepository
"""

import unittest
from repositories.korban_repository import KorbanRepository
from repositories.bahan_repository import BahanRepository
from repositories.distribusi_repository import DistribusiRepository
from models.person import Korban
from models.bahan_makanan import BahanPokok
from models.distribusi import DistribusiMakanan


class TestKorbanRepository(unittest.TestCase):
    """Test case untuk KorbanRepository"""
    
    def setUp(self):
        """Setup repository baru sebelum setiap test"""
        self.repo = KorbanRepository()
        self.korban1 = Korban("Budi", "KRB-001", "Umum", 4)
        self.korban2 = Korban("Siti", "KRB-002", "Lansia", 2)
    
    def test_add_korban(self):
        """Test menambah korban ke repository"""
        self.repo. add(self.korban1)
        retrieved = self.repo.get_by_id("KRB-001")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.get_name(), "Budi")
    
    def test_add_duplicate_id(self):
        """Test menambah korban dengan ID duplikat (harus error)"""
        self.repo.add(self.korban1)
        
        with self.assertRaises(ValueError):
            self.repo. add(self.korban1)  # ID sama
    
    def test_get_by_id_found(self):
        """Test mengambil korban yang ada"""
        self.repo.add(self.korban1)
        korban = self.repo.get_by_id("KRB-001")
        
        self. assertIsNotNone(korban)
        self.assertEqual(korban.get_id(), "KRB-001")
    
    def test_get_by_id_not_found(self):
        """Test mengambil korban yang tidak ada (return None)"""
        korban = self.repo.get_by_id("KRB-999")
        self.assertIsNone(korban)
    
    def test_get_all(self):
        """Test mengambil semua korban"""
        self.repo.add(self. korban1)
        self.repo.add(self.korban2)
        
        all_korban = self.repo.get_all()
        self.assertEqual(len(all_korban), 2)
    
    def test_update_korban(self):
        """Test update data korban"""
        self.repo.add(self.korban1)
        self.korban1.set_name("Budi Updated")
        
        success = self.repo.update(self.korban1)
        self.assertTrue(success)
        
        updated = self.repo.get_by_id("KRB-001")
        self.assertEqual(updated.get_name(), "Budi Updated")
    
    def test_update_not_found(self):
        """Test update korban yang tidak ada"""
        success = self.repo.update(self.korban1)
        self.assertFalse(success)
    
    def test_delete_korban(self):
        """Test menghapus korban"""
        self.repo.add(self. korban1)
        success = self.repo.delete("KRB-001")
        
        self.assertTrue(success)
        self.assertIsNone(self. repo.get_by_id("KRB-001"))
    
    def test_delete_not_found(self):
        """Test menghapus korban yang tidak ada"""
        success = self.repo.delete("KRB-999")
        self.assertFalse(success)
    
    def test_get_by_kebutuhan(self):
        """Test filter korban berdasarkan kebutuhan khusus"""
        self.repo.add(self.korban1)  # Umum
        self.repo.add(self.korban2)  # Lansia
        
        lansia_list = self.repo.get_by_kebutuhan("Lansia")
        self.assertEqual(len(lansia_list), 1)
        self.assertEqual(lansia_list[0].get_name(), "Siti")
    
    def test_get_total_tanggungan(self):
        """Test agregasi total tanggungan"""
        self.repo.add(self.korban1)  # 4 tanggungan
        self.repo. add(self.korban2)  # 2 tanggungan
        
        total = self. repo.get_total_tanggungan()
        self.assertEqual(total, 6)


class TestBahanRepository(unittest.TestCase):
    """Test case untuk BahanRepository"""
    
    def setUp(self):
        """Setup repository baru sebelum setiap test"""
        self.repo = BahanRepository()
        self.beras = BahanPokok("Beras", 100.0, "kg", 250.0)
    
    def test_add_bahan_baru(self):
        """Test menambah bahan baru"""
        self.repo.add(self.beras)
        retrieved = self.repo.get_by_id("Beras")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.get_jumlah(), 100.0)
    
    def test_add_bahan_existing_aggregates(self):
        """Test menambah bahan yang sudah ada (harus aggregate stok)"""
        self.repo.add(self.beras)
        
        beras_baru = BahanPokok("Beras", 50.0, "kg", 250.0)
        self.repo.add(beras_baru)
        
        retrieved = self.repo.get_by_id("Beras")
        # Stok harus bertambah:  100 + 50 = 150
        self.assertEqual(retrieved. get_jumlah(), 150.0)
    
    def test_get_stok_rendah(self):
        """Test filter bahan dengan stok rendah"""
        beras = BahanPokok("Beras", 100.0, "kg", 250.0)
        gula = BahanPokok("Gula", 5.0, "kg", 50.0)  # Stok rendah
        
        self.repo.add(beras)
        self.repo.add(gula)
        
        stok_rendah = self. repo.get_stok_rendah(10.0)
        self.assertEqual(len(stok_rendah), 1)
        self.assertEqual(stok_rendah[0].get_nama(), "Gula")


class TestDistribusiRepository(unittest.TestCase):
    """Test case untuk DistribusiRepository"""
    
    def setUp(self):
        """Setup repository baru sebelum setiap test"""
        self.repo = DistribusiRepository()
        self.dist1 = DistribusiMakanan("DIST-001", "KRB-001", 10)
        self.dist2 = DistribusiMakanan("DIST-002", "KRB-001", 15)
    
    def test_add_distribusi(self):
        """Test menambah distribusi"""
        self.repo.add(self.dist1)
        retrieved = self.repo.get_by_id("DIST-001")
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.get_jumlah_porsi(), 10)
    
    def test_get_by_korban(self):
        """Test mengambil riwayat distribusi per korban"""
        self.repo.add(self.dist1)
        self.repo.add(self.dist2)
        
        riwayat = self.repo. get_by_korban("KRB-001")
        self.assertEqual(len(riwayat), 2)
    
    def test_get_total_porsi_terdistribusi(self):
        """Test agregasi total porsi terdistribusi"""
        self.repo.add(self.dist1)  # 10 porsi
        self.repo.add(self. dist2)  # 15 porsi
        
        total = self.repo.get_total_porsi_terdistribusi()
        self.assertEqual(total, 25)


if __name__ == '__main__':
    unittest.main()