"""
Module untuk Service Layer Dapur Umum.
Menerapkan Business Logic dan SOLID Principles.
"""

from typing import List, Dict, Optional
from repositories.base_repository import IRepository
from repositories.bahan_repository import BahanRepository
from repositories.korban_repository import KorbanRepository
from repositories.distribusi_repository import DistribusiRepository
from models.bahan_makanan import BahanMakanan, BahanPokok, BahanProtein
from models.person import Korban
from models. distribusi import DistribusiMakanan
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DapurService:
    """
    Service untuk mengelola logika bisnis Dapur Umum.
    Menerapkan: 
    - SRP:  Fokus pada logika bisnis dapur
    - DIP: Bergantung pada IRepository (abstraksi), bukan implementasi konkret
    - OCP:  Terbuka untuk extension melalui dependency injection
    """
    
    def __init__(self, 
                 bahan_repo: IRepository[BahanMakanan],
                 korban_repo: IRepository[Korban],
                 distribusi_repo: IRepository[DistribusiMakanan]):
        """
        Constructor dengan Dependency Injection (DIP).
        
        Args:
            bahan_repo:  Repository untuk bahan makanan
            korban_repo: Repository untuk korban
            distribusi_repo: Repository untuk distribusi
        """
        self.__bahan_repo = bahan_repo
        self.__korban_repo = korban_repo
        self.__distribusi_repo = distribusi_repo
        logger.info("DapurService diinisialisasi dengan dependency injection")
    
    def tambah_bahan(self, bahan: BahanMakanan) -> None:
        """
        Menambah bahan makanan ke inventori. 
        
        Args:
            bahan:  Bahan makanan yang ditambahkan
            
        Raises:
            ValueError: Jika validasi gagal
        """
        if bahan.get_jumlah() <= 0:
            raise ValueError("Jumlah bahan harus positif")
        
        self.__bahan_repo.add(bahan)
        logger.info(f"Bahan {bahan.get_nama()} berhasil ditambahkan")
        
        # Warning jika stok masih rendah
        if bahan.get_jumlah() < 20:
            logger.warning(f"Stok {bahan. get_nama()} masih rendah:  {bahan.get_jumlah()}")
    
    def registrasi_korban(self, korban: Korban) -> None:
        """
        Meregistrasi korban baru.
        
        Args:
            korban: Korban yang diregistrasi
            
        Raises:
            ValueError: Jika validasi gagal
        """
        # Cek duplikasi
        if self.__korban_repo.get_by_id(korban.get_id()) is not None:
            raise ValueError(f"Korban dengan ID {korban.get_id()} sudah terdaftar")
        
        self.__korban_repo.add(korban)
        logger.info(f"Korban {korban.get_name()} berhasil diregistrasi")
    
    def distribusi_makanan(self, id_korban: str, jumlah_porsi: int) -> DistribusiMakanan: 
        """
        Mendistribusikan makanan kepada korban.
        
        Args:
            id_korban: ID korban penerima
            jumlah_porsi: Jumlah porsi yang didistribusikan
            
        Returns:
            DistribusiMakanan: Object distribusi yang dibuat
            
        Raises:
            ValueError: Jika korban tidak ditemukan atau stok tidak cukup
        """
        # Validasi korban
        korban = self.__korban_repo.get_by_id(id_korban)
        if korban is None:
            raise ValueError(f"Korban dengan ID {id_korban} tidak ditemukan")
        
        # Validasi ketersediaan porsi
        porsi_tersedia = self. hitung_total_porsi_tersedia()
        if jumlah_porsi > porsi_tersedia: 
            raise ValueError(f"Porsi tidak cukup.  Tersedia:  {porsi_tersedia}, Diminta: {jumlah_porsi}")
        
        # Kurangi stok bahan (simplified - ambil dari bahan pokok)
        bahan_list = self.__bahan_repo.get_all()
        for bahan in bahan_list: 
            if isinstance(bahan, BahanPokok):
                # Hitung kebutuhan bahan
                kg_dibutuhkan = (jumlah_porsi * 0.25)  # 250g per porsi
                if bahan.get_jumlah() >= kg_dibutuhkan:
                    bahan.kurangi_stok(kg_dibutuhkan)
                    break
        
        # Buat distribusi
        id_distribusi = f"DIST-{datetime.now().strftime('%Y%m%d%H%M%S')}-{id_korban}"
        distribusi = DistribusiMakanan(id_distribusi, id_korban, jumlah_porsi)
        self.__distribusi_repo.add(distribusi)
        
        logger.info(f"Distribusi {jumlah_porsi} porsi ke {korban.get_name()} berhasil")
        return distribusi
    
    def hitung_total_porsi_tersedia(self) -> int:
        """
        Menghitung total porsi yang bisa dibuat dari semua bahan.
        Menerapkan Polymorphism - memanggil hitung_porsi() yang berbeda untuk setiap jenis bahan. 
        
        Returns:
            int: Total porsi minimum yang bisa dibuat
        """
        bahan_list = self.__bahan_repo.get_all()
        
        if not bahan_list:
            return 0
        
        # Hitung porsi minimum dari semua bahan (bottleneck)
        porsi_list = [bahan.hitung_porsi() for bahan in bahan_list]
        return min(porsi_list) if porsi_list else 0
    
    def get_laporan_stok(self) -> Dict[str, any]:
        """
        Mendapatkan laporan lengkap stok bahan. 
        
        Returns:
            Dict:  Laporan stok
        """
        bahan_list = self.__bahan_repo.get_all()
        total_porsi = self.hitung_total_porsi_tersedia()
        stok_rendah = self.__bahan_repo.get_stok_rendah(15.0)
        
        return {
            'total_jenis_bahan': len(bahan_list),
            'total_porsi_tersedia': total_porsi,
            'bahan_stok_rendah': len(stok_rendah),
            'detail_bahan': [b.get_info() for b in bahan_list],
            'warning_stok_rendah': [b.get_nama() for b in stok_rendah]
        }
    
    def get_laporan_korban(self) -> Dict[str, any]:
        """
        Mendapatkan laporan data korban.
        
        Returns:
            Dict: Laporan korban
        """
        korban_list = self.__korban_repo.get_all()
        total_tanggungan = self.__korban_repo.get_total_tanggungan()
        
        return {
            'total_korban': len(korban_list),
            'total_tanggungan': total_tanggungan,
            'detail_korban':  [k.get_info() for k in korban_list]
        }
    
    def get_laporan_distribusi(self) -> Dict[str, any]:
        """
        Mendapatkan laporan distribusi makanan.
        
        Returns:
            Dict: Laporan distribusi
        """
        distribusi_list = self.__distribusi_repo.get_all()
        total_porsi = self.__distribusi_repo.get_total_porsi_terdistribusi()
        
        return {
            'total_distribusi':  len(distribusi_list),
            'total_porsi_terdistribusi': total_porsi,
            'detail_distribusi': [d.get_info() for d in distribusi_list]
        }
    
    def cek_kebutuhan_gizi(self) -> Dict[str, str]:
        """
        Mengecek kecukupan gizi berdasarkan jumlah korban dan stok.
        
        Returns:
            Dict: Status kebutuhan gizi
        """
        total_tanggungan = self.__korban_repo.get_total_tanggungan()
        porsi_tersedia = self.hitung_total_porsi_tersedia()
        
        # Asumsi: 3 kali makan per hari
        kebutuhan_harian = total_tanggungan * 3
        hari_bertahan = porsi_tersedia // kebutuhan_harian if kebutuhan_harian > 0 else 0
        
        if hari_bertahan >= 7:
            status = "AMAN"
        elif hari_bertahan >= 3:
            status = "WASPADA"
        else: 
            status = "KRITIS"
        
        return {
            'total_tanggungan': total_tanggungan,
            'porsi_tersedia':  porsi_tersedia,
            'kebutuhan_harian':  kebutuhan_harian,
            'estimasi_hari':  hari_bertahan,
            'status': status
        }