"""
Module untuk representasi bahan makanan.
Menerapkan konsep Inheritance dan Polymorphism.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BahanMakanan(ABC):
    """
    Abstract Base Class untuk bahan makanan.
    
    Attributes:
        __nama (str): Nama bahan makanan (private)
        __jumlah (float): Jumlah stok (private)
        __satuan (str): Satuan (kg, liter, porsi) (private)
        __tanggal_masuk (datetime): Waktu bahan masuk (private)
    """
    
    def __init__(self, nama: str, jumlah: float, satuan:  str):
        """
        Constructor untuk BahanMakanan. 
        
        Args:
            nama (str): Nama bahan
            jumlah (float): Jumlah stok
            satuan (str): Satuan pengukuran
            
        Raises:
            ValueError: Jika jumlah negatif atau nama kosong
        """
        if not nama: 
            raise ValueError("Nama bahan tidak boleh kosong")
        if jumlah < 0:
            raise ValueError("Jumlah tidak boleh negatif")
        
        self.__nama = nama
        self.__jumlah = jumlah
        self.__satuan = satuan
        self.__tanggal_masuk = datetime. now()
        logger.info(f"Bahan {nama} sebanyak {jumlah} {satuan} ditambahkan")
    
    # Getter methods
    def get_nama(self) -> str:
        """Getter untuk nama bahan."""
        return self.__nama
    
    def get_jumlah(self) -> float:
        """Getter untuk jumlah stok."""
        return self.__jumlah
    
    def get_satuan(self) -> str:
        """Getter untuk satuan."""
        return self.__satuan
    
    def get_tanggal_masuk(self) -> datetime:
        """Getter untuk tanggal masuk."""
        return self.__tanggal_masuk
    
    # Setter methods dengan validasi
    def tambah_stok(self, jumlah:  float) -> None:
        """
        Menambah stok bahan dengan validasi.
        
        Args:
            jumlah (float): Jumlah yang ditambahkan
            
        Raises:
            ValueError:  Jika jumlah negatif
        """
        if jumlah < 0:
            raise ValueError("Jumlah tambahan tidak boleh negatif")
        self.__jumlah += jumlah
        logger.info(f"Stok {self.__nama} bertambah {jumlah} {self.__satuan}")
    
    def kurangi_stok(self, jumlah: float) -> None:
        """
        Mengurangi stok bahan dengan validasi.
        
        Args:
            jumlah (float): Jumlah yang dikurangi
            
        Raises:
            ValueError: Jika jumlah negatif atau melebihi stok
        """
        if jumlah < 0:
            raise ValueError("Jumlah pengurangan tidak boleh negatif")
        if jumlah > self.__jumlah:
            raise ValueError(f"Stok tidak cukup.  Tersedia:  {self.__jumlah} {self.__satuan}")
        self.__jumlah -= jumlah
        logger.info(f"Stok {self.__nama} berkurang {jumlah} {self.__satuan}")
    
    @abstractmethod
    def hitung_porsi(self) -> int:
        """
        Method abstract untuk menghitung jumlah porsi yang bisa dibuat.
        Harus diimplementasikan oleh child class (Polymorphism).
        
        Returns:
            int: Jumlah porsi yang bisa dibuat
        """
        pass
    
    def get_info(self) -> str:
        """
        Mendapatkan informasi bahan. 
        
        Returns:
            str: Informasi lengkap bahan
        """
        return (f"{self.__nama}:  {self.__jumlah:. 2f} {self.__satuan} | "
                f"Masuk: {self.__tanggal_masuk.strftime('%Y-%m-%d %H:%M')}")


class BahanPokok(BahanMakanan):
    """
    Class untuk bahan makanan pokok (beras, mie, dll).
    Mewarisi dari BahanMakanan (Inheritance).
    
    Additional Attributes:
        __gram_per_porsi (float): Gram per porsi standar
    """
    
    def __init__(self, nama: str, jumlah: float, satuan: str = "kg", 
                 gram_per_porsi: float = 250.0):
        """
        Constructor untuk BahanPokok. 
        
        Args:
            nama (str): Nama bahan pokok
            jumlah (float): Jumlah stok dalam kg
            satuan (str): Satuan (default: kg)
            gram_per_porsi (float): Gram per porsi (default: 250g)
        """
        super().__init__(nama, jumlah, satuan)
        self.__gram_per_porsi = gram_per_porsi
    
    def get_gram_per_porsi(self) -> float:
        """Getter untuk gram per porsi."""
        return self.__gram_per_porsi
    
    # Method Overriding (Polymorphism)
    def hitung_porsi(self) -> int:
        """
        Override method untuk menghitung porsi bahan pokok.
        
        Returns:
            int: Jumlah porsi yang bisa dibuat
        """
        # Konversi kg ke gram
        total_gram = self. get_jumlah() * 1000
        porsi = int(total_gram / self.__gram_per_porsi)
        return porsi


class BahanProtein(BahanMakanan):
    """
    Class untuk bahan protein (ayam, telur, ikan, dll).
    Mewarisi dari BahanMakanan (Inheritance).
    
    Additional Attributes:
        __unit_per_porsi (float): Unit per porsi (misal: 2 telur/porsi)
    """
    
    def __init__(self, nama: str, jumlah:  float, satuan: str = "kg", 
                 unit_per_porsi: float = 0.15):
        """
        Constructor untuk BahanProtein.
        
        Args:
            nama (str): Nama bahan protein
            jumlah (float): Jumlah stok
            satuan (str): Satuan
            unit_per_porsi (float): Unit per porsi (default: 0.15 kg = 150g)
        """
        super().__init__(nama, jumlah, satuan)
        self.__unit_per_porsi = unit_per_porsi
    
    def get_unit_per_porsi(self) -> float:
        """Getter untuk unit per porsi."""
        return self.__unit_per_porsi
    
    # Method Overriding (Polymorphism)
    def hitung_porsi(self) -> int:
        """
        Override method untuk menghitung porsi bahan protein.
        
        Returns:
            int: Jumlah porsi yang bisa dibuat
        """
        porsi = int(self.get_jumlah() / self.__unit_per_porsi)
        return porsi


class BahanSayuran(BahanMakanan):
    """
    Class untuk bahan sayuran. 
    Mewarisi dari BahanMakanan (Inheritance).
    """
    
    def __init__(self, nama: str, jumlah: float, satuan: str = "kg", 
                 kg_per_porsi: float = 0.1):
        """
        Constructor untuk BahanSayuran. 
        
        Args:
            nama (str): Nama sayuran
            jumlah (float): Jumlah stok
            satuan (str): Satuan
            kg_per_porsi (float): Kg per porsi (default: 0.1 kg = 100g)
        """
        super().__init__(nama, jumlah, satuan)
        self.__kg_per_porsi = kg_per_porsi
    
    def get_kg_per_porsi(self) -> float:
        """Getter untuk kg per porsi."""
        return self.__kg_per_porsi
    
    # Method Overriding (Polymorphism)
    def hitung_porsi(self) -> int:
        """
        Override method untuk menghitung porsi sayuran.
        
        Returns:
            int: Jumlah porsi yang bisa dibuat
        """
        porsi = int(self.get_jumlah() / self.__kg_per_porsi)
        return porsi