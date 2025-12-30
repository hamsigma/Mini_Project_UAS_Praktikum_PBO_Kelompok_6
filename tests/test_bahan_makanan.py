"""
Unit Testing untuk models/bahan_makanan.py
Testing Class BahanPokok, BahanProtein, BahanSayuran
"""

import unittest
from models.bahan_makanan import BahanPokok, BahanProtein, BahanSayuran


class TestBahanPokok(unittest.TestCase):
    """Test case untuk class BahanPokok"""
    
    def setUp(self):
        """Setup yang dijalankan sebelum setiap test"""
        self.beras = BahanPokok("Beras", 100.0, "kg", 250.0)
    
    def test_create_bahan_pokok_valid(self):
        """Test pembuatan bahan pokok dengan data valid"""
        self.assertEqual(self.beras. get_nama(), "Beras")
        self.assertEqual(self.beras.get_jumlah(), 100.0)
        self.assertEqual(self. beras.get_satuan(), "kg")
        self.assertEqual(self.beras. get_gram_per_porsi(), 250.0)
    
    def test_create_bahan_empty_name(self):
        """Test pembuatan bahan dengan nama kosong (harus error)"""
        with self.assertRaises(ValueError):
            BahanPokok("", 50.0, "kg", 250.0)
    
    def test_create_bahan_negative_jumlah(self):
        """Test pembuatan bahan dengan jumlah negatif (harus error)"""
        with self.assertRaises(ValueError):
            BahanPokok("Beras", -10.0, "kg", 250.0)
    
    def test_hitung_porsi_bahan_pokok(self):
        """Test kalkulasi porsi untuk bahan pokok"""
        # 100 kg = 100,000 gram
        # 100,000 / 250 = 400 porsi
        porsi = self.beras.hitung_porsi()
        self.assertEqual(porsi, 400)
    
    def test_tambah_stok_valid(self):
        """Test menambah stok dengan nilai valid"""
        self.beras.tambah_stok(50.0)
        self.assertEqual(self.beras.get_jumlah(), 150.0)
        
        # Porsi harus bertambah juga
        self.assertEqual(self.beras.hitung_porsi(), 600)
    
    def test_tambah_stok_invalid(self):
        """Test menambah stok dengan nilai negatif (harus error)"""
        with self.assertRaises(ValueError):
            self.beras.tambah_stok(-10.0)
    
    def test_kurangi_stok_valid(self):
        """Test mengurangi stok dengan nilai valid"""
        self.beras.kurangi_stok(30.0)
        self.assertEqual(self.beras.get_jumlah(), 70.0)
        self.assertEqual(self.beras. hitung_porsi(), 280)
    
    def test_kurangi_stok_invalid_negative(self):
        """Test mengurangi stok dengan nilai negatif"""
        with self.assertRaises(ValueError):
            self.beras.kurangi_stok(-10.0)
    
    def test_kurangi_stok_melebihi_tersedia(self):
        """Test mengurangi stok melebihi yang tersedia (harus error)"""
        with self.assertRaises(ValueError):
            self.beras.kurangi_stok(150.0)  # Hanya ada 100 kg
    
    def test_get_info_format(self):
        """Test format output get_info()"""
        info = self.beras.get_info()
        self.assertIn("Beras", info)
        self.assertIn("100.00", info)
        self.assertIn("kg", info)


class TestBahanProtein(unittest.TestCase):
    """Test case untuk class BahanProtein"""
    
    def setUp(self):
        """Setup yang dijalankan sebelum setiap test"""
        self. ayam = BahanProtein("Ayam", 50.0, "kg", 0.15)
    
    def test_create_bahan_protein_valid(self):
        """Test pembuatan bahan protein dengan data valid"""
        self.assertEqual(self.ayam.get_nama(), "Ayam")
        self.assertEqual(self.ayam. get_jumlah(), 50.0)
        self.assertEqual(self.ayam.get_unit_per_porsi(), 0.15)
    
    def test_hitung_porsi_bahan_protein(self):
        """Test kalkulasi porsi untuk bahan protein"""
        # 50 kg / 0.15 kg per porsi = 333 porsi
        porsi = self.ayam.hitung_porsi()
        self.assertEqual(porsi, 333)
    
    def test_polymorphism_hitung_porsi(self):
        """Test bahwa hitung_porsi() berbeda antara Pokok dan Protein"""
        beras = BahanPokok("Beras", 50.0, "kg", 250.0)
        ayam = BahanProtein("Ayam", 50.0, "kg", 0.15)
        
        # Jumlah sama (50 kg) tapi porsi berbeda karena logika berbeda
        porsi_beras = beras.hitung_porsi()  # 50*1000/250 = 200
        porsi_ayam = ayam. hitung_porsi()    # 50/0.15 = 333
        
        self.assertEqual(porsi_beras, 200)
        self.assertEqual(porsi_ayam, 333)
        self.assertNotEqual(porsi_beras, porsi_ayam)


class TestBahanSayuran(unittest.TestCase):
    """Test case untuk class BahanSayuran"""
    
    def setUp(self):
        """Setup yang dijalankan sebelum setiap test"""
        self.kangkung = BahanSayuran("Kangkung", 30.0, "kg", 0.1)
    
    def test_create_bahan_sayuran_valid(self):
        """Test pembuatan bahan sayuran dengan data valid"""
        self.assertEqual(self.kangkung.get_nama(), "Kangkung")
        self.assertEqual(self.kangkung.get_jumlah(), 30.0)
        self.assertEqual(self.kangkung.get_kg_per_porsi(), 0.1)
    
    def test_hitung_porsi_bahan_sayuran(self):
        """Test kalkulasi porsi untuk bahan sayuran"""
        # 30 kg / 0.1 kg per porsi = 300 porsi
        porsi = self.kangkung. hitung_porsi()
        self.assertEqual(porsi, 300)


if __name__ == '__main__':
    unittest.main()