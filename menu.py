from dataclasses import dataclass

class StokTidakCukupError(ValueError):
    """Dilempar ketika stok menu tidak mencukupi jumlah yang diminta."""


class Menu:
    """Makanan/minuman yang dijual. Harga dan stok dilindungi (enkapsulasi)."""

    def __init__(self, nama, harga, stok):
        self.nama = nama      # lewat setter -> tervalidasi
        self.harga = harga
        self.stok = stok

    # --- nama ---
    @property
    def nama(self):
        return self._nama

    @nama.setter
    def nama(self, nilai):
        if not isinstance(nilai, str) or not nilai.strip():
            raise ValueError("Nama menu tidak boleh kosong.")
        self._nama = nilai.strip()

    # --- harga ---
    @property
    def harga(self):
        return self._harga

    @harga.setter
    def harga(self, nilai):
        if not isinstance(nilai, (int, float)) or nilai <= 0:
            raise ValueError("Harga harus berupa angka lebih dari 0.")
        self._harga = nilai

    # --- stok ---
    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, nilai):
        if not isinstance(nilai, int) or nilai < 0:
            raise ValueError("Stok harus bilangan bulat >= 0.")
        self._stok = nilai

    # --- perilaku ---
    def tersedia(self, jumlah=1):
        """True jika stok cukup untuk `jumlah` porsi."""
        return self._stok >= jumlah

    def kurangi_stok(self, jumlah):
        if not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("Jumlah harus bilangan bulat lebih dari 0.")
        if not self.tersedia(jumlah):
            raise StokTidakCukupError(
                f"Stok '{self._nama}' tidak cukup (sisa {self._stok}, diminta {jumlah})."
            )
        self._stok -= jumlah

    def tambah_stok(self, jumlah):
        if not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("Jumlah harus bilangan bulat lebih dari 0.")
        self._stok += jumlah

    def __str__(self):
        status = f"stok {self._stok}" if self._stok > 0 else "HABIS"
        return f"{self._nama} - Rp{self._harga:,.0f} ({status})"


@dataclass
class ItemPesanan:
    """Satu baris item: menu + jumlah."""
    menu: Menu
    jumlah: int

    def subtotal(self):
        return self.menu.harga * self.jumlah


class Keranjang:
    """Penyimpanan sementara menu pilihan pelanggan."""

    def __init__(self):
        self._daftar_item = []

    @property
    def daftar_item(self):
        return list(self._daftar_item)  # salinan, agar tidak diubah dari luar

    def kosong(self):
        return len(self._daftar_item) == 0

    def _cari(self, menu):
        for item in self._daftar_item:
            if item.menu is menu:
                return item
        return None

    def tambah_item(self, menu, jumlah):
        if not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("Jumlah harus bilangan bulat lebih dari 0.")
        item = self._cari(menu)
        jumlah_total = jumlah + (item.jumlah if item else 0)
        if not menu.tersedia(jumlah_total):
            raise StokTidakCukupError(
                f"Menu '{menu.nama}' tidak tersedia untuk {jumlah_total} porsi "
                f"(stok {menu.stok})."
            )
        if item:
            item.jumlah = jumlah_total
        else:
            self._daftar_item.append(ItemPesanan(menu, jumlah))

    def hapus_item(self, menu):
        item = self._cari(menu)
        if item is None:
            raise ValueError(f"'{menu.nama}' tidak ada di keranjang.")
        self._daftar_item.remove(item)

    def hitung_total(self):
        return sum(item.subtotal() for item in self._daftar_item)

    def kosongkan(self):
        self._daftar_item.clear()

    def __str__(self):
        if self.kosong():
            return "(keranjang kosong)"
        baris = [
            f"  {i.menu.nama} x{i.jumlah} = Rp{i.subtotal():,.0f}"
            for i in self._daftar_item
        ]
        baris.append(f"  TOTAL = Rp{self.hitung_total():,.0f}")
        return "\n".join(baris)