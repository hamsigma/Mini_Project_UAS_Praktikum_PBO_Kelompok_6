"""
Module untuk fungsi-fungsi helper/utility. 
Menerapkan SRP - fokus pada formatting dan helper functions.
"""

from datetime import datetime
from typing import Dict, List


def format_tanggal(dt: datetime) -> str:
    """
    Format datetime ke string yang readable.
    
    Args:
        dt:  Datetime object
        
    Returns: 
        str:  Tanggal terformat
    """
    return dt.strftime("%d %B %Y, %H:%M")


def format_laporan_tabel(data: List[str], header: str) -> str:
    """
    Format data menjadi tabel sederhana untuk CLI.
    
    Args:
        data: List data string
        header: Header tabel
        
    Returns:
        str: Tabel terformat
    """
    width = 80
    separator = "=" * width
    
    output = f"\n{separator}\n"
    output += f"{header. center(width)}\n"
    output += f"{separator}\n"
    
    for i, item in enumerate(data, 1):
        output += f"{i}. {item}\n"
    
    output += f"{separator}\n"
    return output


def format_status_gizi(status_dict: Dict) -> str:
    """
    Format laporan status gizi.
    
    Args:
        status_dict: Dictionary status gizi
        
    Returns:
        str:  Laporan terformat
    """
    status = status_dict['status']
    
    # Warna status (untuk terminal yang support ANSI)
    color_code = {
        'AMAN': '\033[92m',      # Green
        'WASPADA': '\033[93m',   # Yellow
        'KRITIS': '\033[91m'     # Red
    }
    reset = '\033[0m'
    
    output = "\n" + "="*60 + "\n"
    output += "          LAPORAN STATUS KEBUTUHAN GIZI\n"
    output += "="*60 + "\n"
    output += f"Total Tanggungan      : {status_dict['total_tanggungan']} orang\n"
    output += f"Porsi Tersedia        : {status_dict['porsi_tersedia']} porsi\n"
    output += f"Kebutuhan Harian      : {status_dict['kebutuhan_harian']} porsi\n"
    output += f"Estimasi Bertahan     : {status_dict['estimasi_hari']} hari\n"
    output += f"Status                : {color_code. get(status, '')}{status}{reset}\n"
    output += "="*60 + "\n"
    
    return output


def validasi_input_angka(prompt: str, min_value: float = 0) -> float:
    """
    Validasi input angka dari user.
    
    Args:
        prompt: Pesan prompt
        min_value:  Nilai minimum yang diperbolehkan
        
    Returns:
        float:  Nilai yang valid
    """
    while True:
        try:
            value = float(input(prompt))
            if value < min_value: 
                print(f"❌ Nilai harus >= {min_value}")
                continue
            return value
        except ValueError:
            print("❌ Input harus berupa angka!")


def validasi_input_integer(prompt: str, min_value:  int = 0) -> int:
    """
    Validasi input integer dari user.
    
    Args:
        prompt:  Pesan prompt
        min_value: Nilai minimum yang diperbolehkan
        
    Returns: 
        int: Nilai integer yang valid
    """
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"❌ Nilai harus >= {min_value}")
                continue
            return value
        except ValueError: 
            print("❌ Input harus berupa bilangan bulat!")


def buat_id_unik(prefix: str) -> str:
    """
    Membuat ID unik dengan timestamp.
    
    Args:
        prefix: Prefix ID (misal: KRB untuk korban)
        
    Returns:
        str: ID unik
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}-{timestamp}"