"""
Script untuk menjalankan semua unit tests
"""

import unittest
import sys
import os

# Tambahkan parent directory ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_tests():
    """Menjalankan semua test suite"""
    
    # Create test suite
    loader = unittest. TestLoader()
    suite = unittest.TestSuite()
    
    # Discover dan load semua tests dari folder tests/
    # Ini akan otomatis menemukan semua file test_*.py
    start_dir = os.path.dirname(__file__)
    tests = loader.discover(start_dir, pattern='test_*.py')
    suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY". center(70))
    print("="*70)
    print(f"Total Tests Run    : {result.testsRun}")
    print(f"Successes          : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures           : {len(result. failures)}")
    print(f"Errors             : {len(result.errors)}")
    print("="*70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__': 
    sys.exit(run_tests())