"""
Module untuk Repository Korban.
Implementasi konkret dari IRepository (DIP).
"""

from typing import List, Optional, Dict
from repositories.base_repository import IRepository
from models.person import Korban
import logging

logger = logging.getLogger(__name__)


class KorbanRepository(IRepository[Korban]):
    """
    Repository untuk mengelola data Korban.
    Implementasi IRepository (Dependency Inversion Principle).
    Menerapkan Single Responsibility Principle - hanya mengurus penyimpanan data.
    """
    
    def __init__(self):
        """Constructor - inisialisasi storage dictionary."""
        self.__storage: Dict[str, Korban] = {}
        logger.info("KorbanRepository diinisialisasi")
    
    def add(self, entity: Korban) -> None:
        """
        Menambah korban baru.
        
        Args:
            entity (Korban): Korban yang akan ditambahkan
            
        Raises:
            ValueError: Jika ID sudah ada
        """
        if entity.get_id() in self.__storage:
            raise ValueError(f"Korban dengan ID {entity.get_id()} sudah ada")
        self.__storage[entity. get_id()] = entity
        logger.info(f"Korban {entity.get_id()} ditambahkan ke repository")
    
    def get_by_id(self, entity_id: str) -> Optional[Korban]:
        """
        Mengambil korban berdasarkan ID.
        
        Args:
            entity_id (str): ID korban
            
        Returns:
            Optional[Korban]: Korban jika ditemukan
        """
        return self.__storage.get(entity_id)
    
    def get_all(self) -> List[Korban]:
        """
        Mengambil semua korban. 
        
        Returns:
            List[Korban]: List semua korban
        """
        return list(self.__storage.values())
    
    def update(self, entity: Korban) -> bool:
        """
        Memperbarui data korban.
        
        Args:
            entity (Korban): Korban yang diperbarui
            
        Returns: 
            bool: True jika berhasil
        """
        if entity.get_id() not in self.__storage:
            logger.warning(f"Korban {entity.get_id()} tidak ditemukan untuk update")
            return False
        self.__storage[entity.get_id()] = entity
        logger. info(f"Korban {entity.get_id()} diperbarui")
        return True
    
    def delete(self, entity_id: str) -> bool:
        """
        Menghapus korban. 
        
        Args:
            entity_id (str): ID korban
            
        Returns:
            bool: True jika berhasil
        """
        if entity_id in self.__storage:
            del self.__storage[entity_id]
            logger.info(f"Korban {entity_id} dihapus")
            return True
        logger.warning(f"Korban {entity_id} tidak ditemukan untuk dihapus")
        return False
    
    def get_by_kebutuhan(self, kebutuhan:  str) -> List[Korban]:
        """
        Mengambil korban berdasarkan kebutuhan khusus.
        
        Args:
            kebutuhan (str): Jenis kebutuhan khusus
            
        Returns: 
            List[Korban]:  List korban dengan kebutuhan tertentu
        """
        return [k for k in self.__storage.values() 
                if k.get_kebutuhan_khusus() == kebutuhan]
    
    def get_total_tanggungan(self) -> int:
        """
        Menghitung total tanggungan semua korban.
        
        Returns:
            int: Total tanggungan
        """
        return sum(k.get_jumlah_tanggungan() for k in self.__storage.values())