"""
Module untuk Repository Distribusi Makanan.
"""

from typing import List, Optional, Dict
from repositories.base_repository import IRepository
from models.distribusi import DistribusiMakanan
import logging

logger = logging.getLogger(__name__)


class DistribusiRepository(IRepository[DistribusiMakanan]):
    """
    Repository untuk mengelola data Distribusi Makanan.
    Implementasi IRepository (Dependency Inversion Principle).
    """
    
    def __init__(self):
        """Constructor - inisialisasi storage dictionary."""
        self.__storage: Dict[str, DistribusiMakanan] = {}
        logger.info("DistribusiRepository diinisialisasi")
    
    def add(self, entity: DistribusiMakanan) -> None:
        """
        Menambah distribusi baru. 
        
        Args:
            entity (DistribusiMakanan): Distribusi yang akan ditambahkan
            
        Raises:
            ValueError: Jika ID sudah ada
        """
        if entity. get_id_distribusi() in self.__storage:
            raise ValueError(f"Distribusi {entity.get_id_distribusi()} sudah ada")
        self.__storage[entity.get_id_distribusi()] = entity
        logger.info(f"Distribusi {entity.get_id_distribusi()} ditambahkan")
    
    def get_by_id(self, entity_id: str) -> Optional[DistribusiMakanan]:
        """
        Mengambil distribusi berdasarkan ID.
        
        Args:
            entity_id (str): ID distribusi
            
        Returns:
            Optional[DistribusiMakanan]: Distribusi jika ditemukan
        """
        return self.__storage.get(entity_id)
    
    def get_all(self) -> List[DistribusiMakanan]:
        """
        Mengambil semua distribusi.
        
        Returns:
            List[DistribusiMakanan]: List semua distribusi
        """
        return list(self.__storage.values())
    
    def update(self, entity: DistribusiMakanan) -> bool:
        """
        Memperbarui distribusi.
        
        Args:
            entity (DistribusiMakanan): Distribusi yang diperbarui
            
        Returns:
            bool: True jika berhasil
        """
        if entity.get_id_distribusi() not in self.__storage:
            return False
        self.__storage[entity.get_id_distribusi()] = entity
        return True
    
    def delete(self, entity_id: str) -> bool:
        """
        Menghapus distribusi. 
        
        Args:
            entity_id (str): ID distribusi
            
        Returns: 
            bool: True jika berhasil
        """
        if entity_id in self.__storage:
            del self.__storage[entity_id]
            logger.info(f"Distribusi {entity_id} dihapus")
            return True
        return False
    
    def get_by_korban(self, id_korban: str) -> List[DistribusiMakanan]:
        """
        Mengambil riwayat distribusi untuk korban tertentu.
        
        Args:
            id_korban (str): ID korban
            
        Returns:
            List[DistribusiMakanan]: List distribusi untuk korban
        """
        return [d for d in self.__storage.values() 
                if d.get_id_korban() == id_korban]
    
    def get_total_porsi_terdistribusi(self) -> int:
        """
        Menghitung total porsi yang sudah didistribusikan.
        
        Returns:
            int: Total porsi
        """
        return sum(d.get_jumlah_porsi() for d in self.__storage.values())