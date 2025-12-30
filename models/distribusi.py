"""
Module untuk representasi distribusi makanan.
Menerapkan konsep Enkapsulasi dan Object Composition.
"""

from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DistribusiMakanan:
    """
    Class untuk merepresentasikan distribusi makanan kepada korban.
    
    Attributes:
        __id_distribusi (str): ID unik distribusi (private)
        __id_korban (str): ID korban penerima (private)
        __jumlah_porsi (int): Jumlah porsi yang didistribusikan (private)
        __waktu_distribusi (datetime): Waktu distribusi (private)
        __catatan (str): Catatan tambahan (private)
    """
    
    def __init__(self, id_distribusi: str, id_korban: str, jumlah_porsi: int, 
                 catatan: str = ""):
        """
        Constructor untuk DistribusiMakanan.
        
        Args:
            id_distribusi (str): ID unik distribusi
            id_korban (str): ID korban penerima
            jumlah_porsi (int): Jumlah porsi
            catatan (str): Catatan tambahan
            
        Raises:
            ValueError: Jika jumlah_porsi < 1
        """
        if jumlah_porsi < 1:
            raise ValueError("Jumlah porsi minimal 1")
        
        self.__id_distribusi = id_distribusi
        self.__id_korban = id_korban
        self.__jumlah_porsi = jumlah_porsi
        self.__waktu_distribusi = datetime.now()
        self.__catatan = catatan
        logger.info(f"Distribusi {id_distribusi}:  {jumlah_porsi} porsi ke korban {id_korban}")
    
    # Getter methods (Enkapsulasi)
    def get_id_distribusi(self) -> str:
        """Getter untuk ID distribusi."""
        return self.__id_distribusi
    
    def get_id_korban(self) -> str:
        """Getter untuk ID korban."""
        return self.__id_korban
    
    def get_jumlah_porsi(self) -> int:
        """Getter untuk jumlah porsi."""
        return self.__jumlah_porsi
    
    def get_waktu_distribusi(self) -> datetime:
        """Getter untuk waktu distribusi."""
        return self.__waktu_distribusi
    
    def get_catatan(self) -> str:
        """Getter untuk catatan."""
        return self.__catatan
    
    def set_catatan(self, catatan: str) -> None:
        """
        Setter untuk catatan. 
        
        Args:
            catatan (str): Catatan baru
        """
        self.__catatan = catatan
        logger.info(f"Catatan distribusi {self.__id_distribusi} diperbarui")
    
    def get_info(self) -> str:
        """
        Mendapatkan informasi distribusi. 
        
        Returns:
            str: Informasi lengkap distribusi
        """
        info = (f"Distribusi {self.__id_distribusi} | "
                f"Korban: {self.__id_korban} | "
                f"Porsi: {self.__jumlah_porsi} | "
                f"Waktu: {self.__waktu_distribusi.strftime('%Y-%m-%d %H:%M')}")
        if self.__catatan:
            info += f" | Catatan:  {self.__catatan}"
        return info