
"""
Script untuk menjalankan semua unit tests
"""

import unittest
import sys
import os

# Tambahkan parent directory ke sys.path
sys.path. insert(0, os.path. abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import semua test modules
from tests.test_person import TestKorban, TestRelawan
from tests.test_bahan_makanan import TestBahanPokok, TestBahanProtein, TestBahanSayuran
from tests.test_repositories import TestKorbanRepository, TestBahanRepository, TestDistribusiRepository
from tests.test_dapur_service import TestDapurService


def run_tests():
    """Menjalankan semua test suite"""
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestKorban))
    suite.addTests(loader. loadTestsFromTestCase(TestRelawan))
    suite.addTests(loader.loadTestsFromTestCase(TestBahanPokok))
    suite.addTests(loader.loadTestsFromTestCase(TestBahanProtein))
    suite.addTests(loader.loadTestsFromTestCase(TestBahanSayuran))
    suite.addTests(loader.loadTestsFromTestCase(TestKorbanRepository))
    suite.addTests(loader.loadTestsFromTestCase(TestBahanRepository))
    suite.addTests(loader.loadTestsFromTestCase(TestDistribusiRepository))
    suite.addTests(loader.loadTestsFromTestCase(TestDapurService))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY". center(70))
    print("="*70)
    print(f"Total Tests Run    : {result.testsRun}")
    print(f"Successes          : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures           : {len(result.failures)}")
    print(f"Errors             : {len(result. errors)}")
    print("="*70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__': 
    sys.exit(run_tests())