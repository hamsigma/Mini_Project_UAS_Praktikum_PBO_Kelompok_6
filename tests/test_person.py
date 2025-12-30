"""
Unit Testing untuk models/person.py
Testing Class Person, Korban, dan Relawan
"""

import unittest
import sys
import os

# Setup path agar bisa import dari parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os. path.abspath(__file__))))

from datetime import datetime
from models.person import Person, Korban, Relawan


class TestKorban(unittest. TestCase):
    """Test case untuk class Korban"""
    
    def setUp(self):
        """Setup yang dijalankan sebelum setiap test"""
        self.korban = Korban("Budi Santoso", "KRB-001", "Umum", 4)
    
    def test_create_korban_valid(self):
        """Test pembuatan korban dengan data valid"""
        self.assertEqual(self.korban.get_name(), "Budi Santoso")
        self.assertEqual(self.korban.get_id(), "KRB-001")
        self.assertEqual(self.korban.get_kebutuhan_khusus(), "Umum")
        self.assertEqual(self.korban.get_jumlah_tanggungan(), 4)
    
    def test_create_korban_empty_name(self):
        """Test pembuatan korban dengan nama kosong (harus error)"""
        with self. assertRaises(ValueError):
            Korban("", "KRB-002", "Umum", 2)
    
    def test_create_korban_empty_id(self):
        """Test pembuatan korban dengan ID kosong (harus error)"""
        with self.assertRaises(ValueError):
            Korban("Ahmad", "", "Umum", 2)
    
    def test_create_korban_invalid_tanggungan(self):
        """Test pembuatan korban dengan tanggungan invalid (harus error)"""
        with self.assertRaises(ValueError):
            Korban("Siti", "KRB-003", "Umum", 0)
    
    def test_set_jumlah_tanggungan_valid(self):
        """Test mengubah jumlah tanggungan dengan nilai valid"""
        self.korban.set_jumlah_tanggungan(5)
        self.assertEqual(self.korban. get_jumlah_tanggungan(), 5)
    
    def test_set_jumlah_tanggungan_invalid(self):
        """Test mengubah jumlah tanggungan dengan nilai invalid"""
        with self. assertRaises(ValueError):
            self.korban.set_jumlah_tanggungan(0)
    
    def test_set_name_valid(self):
        """Test mengubah nama dengan nilai valid"""
        self. korban.set_name("Budi Wijaya")
        self.assertEqual(self.korban.get_name(), "Budi Wijaya")
    
    def test_set_name_empty(self):
        """Test mengubah nama dengan nilai kosong (harus error)"""
        with self.assertRaises(ValueError):
            self.korban.set_name("")
    
    def test_get_info_format(self):
        """Test format output get_info()"""
        info = self.korban.get_info()
        self.assertIn("[KORBAN]", info)
        self.assertIn("Budi Santoso", info)
        self.assertIn("KRB-001", info)
        self.assertIn("Umum", info)
        self.assertIn("4 orang", info)
    
    def test_registered_date_is_datetime(self):
        """Test bahwa registered_date adalah datetime"""
        self.assertIsInstance(self.korban.get_registered_date(), datetime)
    
    def test_polymorphism_get_info(self):
        """Test polymorphism - Korban dan Relawan punya get_info berbeda"""
        relawan = Relawan("Andi", "REL-001", "Memasak")
        
        korban_info = self.korban.get_info()
        relawan_info = relawan.get_info()
        
        # Keduanya implement get_info() tapi output berbeda
        self.assertIn("[KORBAN]", korban_info)
        self.assertIn("[RELAWAN]", relawan_info)
        self.assertNotEqual(korban_info, relawan_info)


class TestRelawan(unittest.TestCase):
    """Test case untuk class Relawan"""
    
    def setUp(self):
        """Setup yang dijalankan sebelum setiap test"""
        self.relawan = Relawan("Andi Pratama", "REL-001", "Memasak")
    
    def test_create_relawan_valid(self):
        """Test pembuatan relawan dengan data valid"""
        self. assertEqual(self.relawan.get_name(), "Andi Pratama")
        self.assertEqual(self.relawan.get_id(), "REL-001")
        self.assertEqual(self. relawan.get_keahlian(), "Memasak")
        self.assertEqual(self.relawan.get_jam_kerja(), 0)
    
    def test_create_relawan_empty_name(self):
        """Test pembuatan relawan dengan nama kosong"""
        with self.assertRaises(ValueError):
            Relawan("", "REL-002", "Medis")
    
    def test_tambah_jam_kerja_valid(self):
        """Test menambah jam kerja dengan nilai valid"""
        self.relawan. tambah_jam_kerja(8)
        self.assertEqual(self.relawan.get_jam_kerja(), 8)
        
        self.relawan.tambah_jam_kerja(4)
        self.assertEqual(self.relawan.get_jam_kerja(), 12)
    
    def test_tambah_jam_kerja_invalid(self):
        """Test menambah jam kerja dengan nilai negatif (harus error)"""
        with self.assertRaises(ValueError):
            self.relawan.tambah_jam_kerja(-5)
    
    def test_get_info_format(self):
        """Test format output get_info()"""
        self.relawan.tambah_jam_kerja(10)
        info = self.relawan.get_info()
        
        self.assertIn("[RELAWAN]", info)
        self.assertIn("Andi Pratama", info)
        self.assertIn("REL-001", info)
        self.assertIn("Memasak", info)
        self.assertIn("10 jam", info)


if __name__ == '__main__':
    unittest.main()