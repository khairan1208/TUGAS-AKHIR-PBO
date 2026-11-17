class Pembayaran:
    """Pembayaran tunai atas sebuah pesanan."""

    def __init__(self, pesanan, uang_diterima):
        if not isinstance(uang_diterima, (int, float)) or uang_diterima <= 0:
            raise ValueError("Uang yang diterima harus lebih dari 0.")
        self._pesanan = pesanan
        self._jumlah = pesanan.hitung_total()
        self._uang_diterima = uang_diterima
        self._berhasil = False

    @property
    def jumlah(self):
        return self._jumlah

    @property
    def uang_diterima(self):
        return self._uang_diterima

    @property
    def berhasil(self):
        return self._berhasil

    def hitung_kembalian(self):
        return self._uang_diterima - self._jumlah

    def proses(self):
        """Proses pembayaran. Mengembalikan jumlah kembalian."""
        if self._uang_diterima < self._jumlah:
            kurang = self._jumlah - self._uang_diterima
            raise ValueError(f"Uang kurang Rp{kurang:,.0f}. Pembayaran gagal.")
        self._pesanan.tandai_dibayar()  # error jika pesanan sudah dibayar/batal
        self._berhasil = True
        return self.hitung_kembalian()