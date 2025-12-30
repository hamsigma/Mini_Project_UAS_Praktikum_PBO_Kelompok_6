"""
Module untuk representasi entitas manusia (Korban dan Relawan).
Menerapkan konsep Inheritance dan Polymorphism.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Person(ABC):
    """
    Abstract Base Class untuk representasi manusia.
    
    Attributes:
        __name (str): Nama lengkap person (private)
        __id (str): ID unik person (private)
        __registered_date (datetime): Tanggal registrasi (private)
    """
    
    def __init__(self, name: str, person_id: str):
        """
        Constructor untuk Person.
        
        Args:
            name (str): Nama lengkap
            person_id (str): ID unik
            
        Raises:
            ValueError: Jika name atau person_id kosong
        """
        if not name or not person_id:
            raise ValueError("Name dan ID tidak boleh kosong")
        
        self.__name = name
        self.__id = person_id
        self.__registered_date = datetime.now()
        logger.info(f"Person {name} dengan ID {person_id} berhasil dibuat")
    
    # Getter methods (Enkapsulasi)
    def get_name(self) -> str:
        """Getter untuk nama."""
        return self.__name
    
    def get_id(self) -> str:
        """Getter untuk ID."""
        return self.__id
    
    def get_registered_date(self) -> datetime:
        """Getter untuk tanggal registrasi."""
        return self.__registered_date
    
    # Setter methods dengan validasi
    def set_name(self, name: str) -> None:
        """
        Setter untuk nama dengan validasi.
        
        Args:
            name (str): Nama baru
            
        Raises: 
            ValueError: Jika name kosong
        """
        if not name:
            raise ValueError("Name tidak boleh kosong")
        self.__name = name
        logger.info(f"Nama person ID {self.__id} diubah menjadi {name}")
    
    @abstractmethod
    def get_info(self) -> str:
        """
        Method abstract untuk mendapatkan informasi person.
        Harus diimplementasikan oleh child class (Polymorphism).
        
        Returns:
            str:  Informasi lengkap person
        """
        pass


class Korban(Person):
    """
    Class untuk representasi korban bencana.
    Mewarisi dari Person (Inheritance).
    
    Additional Attributes:
        __kebutuhan_khusus (str): Kebutuhan khusus korban (lansia, bayi, dll)
        __jumlah_tanggungan (int): Jumlah anggota keluarga
    """
    
    def __init__(self, name: str, person_id: str, kebutuhan_khusus: str = "Umum", 
                 jumlah_tanggungan: int = 1):
        """
        Constructor untuk Korban.
        
        Args:
            name (str): Nama korban
            person_id (str): ID korban
            kebutuhan_khusus (str): Kategori kebutuhan (Umum/Lansia/Bayi/Sakit)
            jumlah_tanggungan (int): Jumlah tanggungan
            
        Raises:
            ValueError: Jika jumlah_tanggungan < 1
        """
        super().__init__(name, person_id)  # Memanggil constructor parent
        
        if jumlah_tanggungan < 1:
            raise ValueError("Jumlah tanggungan minimal 1")
        
        self.__kebutuhan_khusus = kebutuhan_khusus
        self.__jumlah_tanggungan = jumlah_tanggungan
        logger.info(f"Korban {name} terdaftar dengan {jumlah_tanggungan} tanggungan")
    
    # Getter dan Setter
    def get_kebutuhan_khusus(self) -> str:
        """Getter untuk kebutuhan khusus."""
        return self.__kebutuhan_khusus
    
    def get_jumlah_tanggungan(self) -> int:
        """Getter untuk jumlah tanggungan."""
        return self.__jumlah_tanggungan
    
    def set_jumlah_tanggungan(self, jumlah: int) -> None:
        """
        Setter untuk jumlah tanggungan dengan validasi.
        
        Args:
            jumlah (int): Jumlah tanggungan baru
            
        Raises:
            ValueError: Jika jumlah < 1
        """
        if jumlah < 1:
            raise ValueError("Jumlah tanggungan minimal 1")
        self.__jumlah_tanggungan = jumlah
        logger.info(f"Tanggungan korban {self. get_id()} diubah menjadi {jumlah}")
    
    # Method Overriding (Polymorphism)
    def get_info(self) -> str:
        """
        Override method get_info() dari parent class.
        
        Returns:
            str: Informasi lengkap korban
        """
        return (f"[KORBAN] {self.get_name()} (ID: {self.get_id()}) | "
                f"Kebutuhan:  {self.__kebutuhan_khusus} | "
                f"Tanggungan: {self.__jumlah_tanggungan} orang | "
                f"Terdaftar: {self.get_registered_date().strftime('%Y-%m-%d %H:%M')}")


class Relawan(Person):
    """
    Class untuk representasi relawan. 
    Mewarisi dari Person (Inheritance).
    
    Additional Attributes:
        __keahlian (str): Keahlian relawan (Memasak/Medis/Logistik)
        __jam_kerja (int): Total jam kerja relawan
    """
    
    def __init__(self, name: str, person_id: str, keahlian: str = "Umum"):
        """
        Constructor untuk Relawan.
        
        Args:
            name (str): Nama relawan
            person_id (str): ID relawan
            keahlian (str): Keahlian relawan
        """
        super().__init__(name, person_id)
        self.__keahlian = keahlian
        self.__jam_kerja = 0
        logger.info(f"Relawan {name} dengan keahlian {keahlian} terdaftar")
    
    def get_keahlian(self) -> str:
        """Getter untuk keahlian."""
        return self.__keahlian
    
    def get_jam_kerja(self) -> int:
        """Getter untuk jam kerja."""
        return self.__jam_kerja
    
    def tambah_jam_kerja(self, jam: int) -> None:
        """
        Menambah jam kerja relawan. 
        
        Args:
            jam (int): Jumlah jam yang ditambahkan
            
        Raises:
            ValueError:  Jika jam negatif
        """
        if jam < 0:
            raise ValueError("Jam kerja tidak boleh negatif")
        self.__jam_kerja += jam
        logger.info(f"Relawan {self.get_id()} menambah {jam} jam kerja")
    
    # Method Overriding (Polymorphism)
    def get_info(self) -> str:
        """
        Override method get_info() dari parent class.
        
        Returns:
            str: Informasi lengkap relawan
        """
        return (f"[RELAWAN] {self.get_name()} (ID: {self.get_id()}) | "
                f"Keahlian: {self.__keahlian} | "
                f"Jam Kerja: {self.__jam_kerja} jam | "
                f"Bergabung: {self.get_registered_date().strftime('%Y-%m-%d')}")