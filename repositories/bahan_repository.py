"""
Module untuk Repository Bahan Makanan.
Implementasi konkret dari IRepository (DIP).
"""

from typing import List, Optional, Dict
from repositories.base_repository import IRepository
from models.bahan_makanan import BahanMakanan
import logging

logger = logging.getLogger(__name__)


class BahanRepository(IRepository[BahanMakanan]):
    """
    Repository untuk mengelola data Bahan Makanan.
    Implementasi IRepository (Dependency Inversion Principle).
    Menerapkan Single Responsibility Principle. 
    """
    
    def __init__(self):
        """Constructor - inisialisasi storage dictionary."""
        self.__storage: Dict[str, BahanMakanan] = {}
        logger. info("BahanRepository diinisialisasi")
    
    def add(self, entity: BahanMakanan) -> None:
        """
        Menambah bahan makanan baru atau update jika sudah ada.
        
        Args:
            entity (BahanMakanan): Bahan yang akan ditambahkan
        """
        nama = entity.get_nama()
        if nama in self.__storage:
            # Jika sudah ada, tambahkan stoknya
            self.__storage[nama].tambah_stok(entity.get_jumlah())
            logger.info(f"Stok {nama} ditambahkan")
        else:
            self.__storage[nama] = entity
            logger.info(f"Bahan {nama} ditambahkan ke repository")
    
    def get_by_id(self, entity_id: str) -> Optional[BahanMakanan]: 
        """
        Mengambil bahan berdasarkan nama (sebagai ID).
        
        Args:
            entity_id (str): Nama bahan
            
        Returns:
            Optional[BahanMakanan]: Bahan jika ditemukan
        """
        return self.__storage.get(entity_id)
    
    def get_all(self) -> List[BahanMakanan]:
        """
        Mengambil semua bahan. 
        
        Returns:
            List[BahanMakanan]:  List semua bahan
        """
        return list(self.__storage.values())
    
    def update(self, entity: BahanMakanan) -> bool:
        """
        Memperbarui data bahan. 
        
        Args:
            entity (BahanMakanan): Bahan yang diperbarui
            
        Returns: 
            bool: True jika berhasil
        """
        nama = entity.get_nama()
        if nama not in self.__storage:
            logger.warning(f"Bahan {nama} tidak ditemukan untuk update")
            return False
        self.__storage[nama] = entity
        logger.info(f"Bahan {nama} diperbarui")
        return True
    
    def delete(self, entity_id: str) -> bool:
        """
        Menghapus bahan.
        
        Args:
            entity_id (str): Nama bahan
            
        Returns:
            bool: True jika berhasil
        """
        if entity_id in self.__storage:
            del self.__storage[entity_id]
            logger. info(f"Bahan {entity_id} dihapus")
            return True
        logger.warning(f"Bahan {entity_id} tidak ditemukan untuk dihapus")
        return False
    
    def get_stok_rendah(self, threshold: float = 10.0) -> List[BahanMakanan]: 
        """
        Mendapatkan bahan dengan stok rendah.
        
        Args:
            threshold (float): Batas stok rendah
            
        Returns:
            List[BahanMakanan]:  List bahan dengan stok rendah
        """
        return [b for b in self.__storage.values() if b.get_jumlah() < threshold]