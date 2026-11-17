from abc import ABC, abstractmethod
from menu import Menu, Keranjang, StokTidakCukupError
from pesanan import Pesanan, StatusPesanan


class User(ABC):
    """Class induk abstrak untuk semua jenis pengguna."""

    def __init__(self, id_pengguna, nama):
        if not str(nama).strip():
            raise ValueError("Nama pengguna tidak boleh kosong.")
        self._id_pengguna = id_pengguna
        self._nama = nama.strip()

    @property
    def id_pengguna(self):
        return self._id_pengguna

    @property
    def nama(self):
        return self._nama

    @abstractmethod
    def tampilkan_info(self):
        """Setiap turunan wajib mengimplementasikan (polimorfisme)."""


class Pelanggan(User):
    def __init__(self, id_pengguna, nama):
        super().__init__(id_pengguna, nama)
        self._keranjang = Keranjang()
        self._riwayat_pesanan = []

    @property
    def keranjang(self):
        return self._keranjang

    @property
    def riwayat_pesanan(self):
        return list(self._riwayat_pesanan)

    def tambah_ke_keranjang(self, menu, jumlah):
        self._keranjang.tambah_item(menu, jumlah)

    def buat_pesanan(self):
        """Ubah isi keranjang menjadi Pesanan, kurangi stok, kosongkan keranjang."""
        if self._keranjang.kosong():
            raise ValueError("Keranjang masih kosong.")
        items = self._keranjang.daftar_item
        # validasi semua dulu agar tidak ada stok yang terpotong setengah
        for item in items:
            if not item.menu.tersedia(item.jumlah):
                raise StokTidakCukupError(
                    f"Stok '{item.menu.nama}' tidak cukup (sisa {item.menu.stok})."
                )
        for item in items:
            item.menu.kurangi_stok(item.jumlah)
        pesanan = Pesanan(self, items)
        self._riwayat_pesanan.append(pesanan)
        self._keranjang.kosongkan()
        return pesanan

    def tampilkan_info(self):
        return (f"[Pelanggan] {self._id_pengguna} - {self._nama} | "
                f"Pesanan: {len(self._riwayat_pesanan)}")


class Penjual(User):
    def __init__(self, id_pengguna, nama, nama_kios):
        super().__init__(id_pengguna, nama)
        self._nama_kios = nama_kios
        self._daftar_menu = []

    @property
    def nama_kios(self):
        return self._nama_kios

    @property
    def daftar_menu(self):
        return list(self._daftar_menu)

    def tambah_menu(self, menu):
        if not isinstance(menu, Menu):
            raise TypeError("Yang ditambahkan harus objek Menu.")
        if any(m.nama.lower() == menu.nama.lower() for m in self._daftar_menu):
            raise ValueError(f"Menu '{menu.nama}' sudah ada.")
        self._daftar_menu.append(menu)

    def ubah_status_pesanan(self, pesanan, status_baru):
        pesanan.ubah_status(status_baru)

    def tampilkan_info(self):
        return (f"[Penjual] {self._id_pengguna} - {self._nama} | "
                f"Kios: {self._nama_kios} | Menu: {len(self._daftar_menu)}")