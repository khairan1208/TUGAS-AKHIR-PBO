from enum import Enum
from itertools import count
from menu import ItemPesanan


class StatusPesanan(Enum):
    MENUNGGU_PEMBAYARAN = "Menunggu Pembayaran"
    DIPROSES = "Diproses"
    SIAP_DIAMBIL = "Siap Diambil"
    SELESAI = "Selesai"
    DIBATALKAN = "Dibatalkan"


# Perpindahan status yang diizinkan yang dilakukan penjual
_ALUR_PENJUAL = {
    StatusPesanan.DIPROSES: StatusPesanan.SIAP_DIAMBIL,
    StatusPesanan.SIAP_DIAMBIL: StatusPesanan.SELESAI,
}


class Pesanan:
    """Transaksi pemesanan milik satu pelanggan."""

    _penghitung_id = count(1)

    def __init__(self, pelanggan, daftar_item):
        if not daftar_item:
            raise ValueError("Pesanan tidak boleh kosong.")
        self._id_pesanan = f"PSN-{next(Pesanan._penghitung_id):03d}"
        self._pelanggan = pelanggan
        # salin item agar perubahan keranjang tidak mempengaruhi pesanan
        self._daftar_item = [ItemPesanan(i.menu, i.jumlah) for i in daftar_item]
        self._status = StatusPesanan.MENUNGGU_PEMBAYARAN

    @property
    def id_pesanan(self):
        return self._id_pesanan

    @property
    def pelanggan(self):
        return self._pelanggan

    @property
    def daftar_item(self):
        return list(self._daftar_item)

    @property
    def status(self):
        return self._status

    def hitung_total(self):
        return sum(item.subtotal() for item in self._daftar_item)

    def sudah_dibayar(self):
        return self._status not in (
            StatusPesanan.MENUNGGU_PEMBAYARAN, StatusPesanan.DIBATALKAN
        )

    def tandai_dibayar(self):
        """Dipanggil oleh Pembayaran setelah pembayaran sukses."""
        if self._status != StatusPesanan.MENUNGGU_PEMBAYARAN:
            raise ValueError(
                f"Pesanan {self._id_pesanan} tidak dapat dibayar "
                f"(status: {self._status.value})."
            )
        self._status = StatusPesanan.DIPROSES

    def ubah_status(self, status_baru):
        """Dipanggil penjual: Diproses -> Siap Diambil -> Selesai."""
        if _ALUR_PENJUAL.get(self._status) != status_baru:
            raise ValueError(
                f"Status tidak bisa diubah dari '{self._status.value}' "
                f"ke '{status_baru.value}'."
            )
        self._status = status_baru

    def batalkan(self):
        """Batalkan pesanan yang belum dibayar & kembalikan stok."""
        if self._status != StatusPesanan.MENUNGGU_PEMBAYARAN:
            raise ValueError("Hanya pesanan yang belum dibayar yang dapat dibatalkan.")
        for item in self._daftar_item:
            item.menu.tambah_stok(item.jumlah)
        self._status = StatusPesanan.DIBATALKAN

    def __str__(self):
        baris = [f"[{self._id_pesanan}] {self._pelanggan.nama} - {self._status.value}"]
        baris += [
            f"  {i.menu.nama} x{i.jumlah} = Rp{i.subtotal():,.0f}"
            for i in self._daftar_item
        ]
        baris.append(f"  TOTAL = Rp{self.hitung_total():,.0f}")
        return "\n".join(baris)