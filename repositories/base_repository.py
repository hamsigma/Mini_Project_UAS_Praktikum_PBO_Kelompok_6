"""
Module untuk Abstract Base Class Repository.
Menerapkan Dependency Inversion Principle (SOLID).
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """
    Interface untuk Repository pattern.
    Menerapkan DIP - high-level modules bergantung pada abstraksi ini.
    
    Type Parameters:
        T: Tipe entitas yang disimpan
    """
    
    @abstractmethod
    def add(self, entity: T) -> None:
        """
        Menambah entitas baru. 
        
        Args:
            entity (T): Entitas yang akan ditambahkan
        """
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Mengambil entitas berdasarkan ID.
        
        Args:
            entity_id (str): ID entitas
            
        Returns:
            Optional[T]:  Entitas jika ditemukan, None jika tidak
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """
        Mengambil semua entitas. 
        
        Returns:
            List[T]: List semua entitas
        """
        pass
    
    @abstractmethod
    def update(self, entity: T) -> bool:
        """
        Memperbarui entitas.
        
        Args:
            entity (T): Entitas yang diperbarui
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Menghapus entitas.
        
        Args:
            entity_id (str): ID entitas yang dihapus
            
        Returns:
            bool: True jika berhasil, False jika gagal
        """
        pass