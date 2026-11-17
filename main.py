from menu import Menu, StokTidakCukupError
from user import Pelanggan, Penjual
from pesanan import StatusPesanan
from pembayaran import Pembayaran


def garis(judul):
    print(f"\n{'=' * 8} {judul} {'=' * 8}")


def main():
    # --- Persiapan data ---
    penjual = Penjual("P01", "Bu Sari", "Kios Bu Sari")
    penjual.tambah_menu(Menu("Nasi Goreng", 12000, 5))
    penjual.tambah_menu(Menu("Mie Ayam", 10000, 3))
    penjual.tambah_menu(Menu("Es Teh", 4000, 10))
    penjual.tambah_menu(Menu("Soto Ayam", 13000, 0))  # stok habis
    nasi, mie, teh, soto = penjual.daftar_menu

    pelanggan = Pelanggan("C01", "Fandi")

    # Polimorfisme: satu pemanggilan, perilaku berbeda per jenis user
    garis("Info Pengguna (polimorfisme)")
    for user in (penjual, pelanggan):
        print(user.tampilkan_info())

    garis("Daftar Menu")
    for m in penjual.daftar_menu:
        print(" -", m)

    # --- Skenario 1: memasukkan menu ke keranjang ---
    garis("Skenario 1: Tambah ke keranjang")
    pelanggan.tambah_ke_keranjang(nasi, 2)
    pelanggan.tambah_ke_keranjang(teh, 2)
    print(pelanggan.keranjang)

    # --- Skenario 3: menu habis ---
    garis("Skenario 3: Pesan menu stok habis")
    try:
        pelanggan.tambah_ke_keranjang(soto, 1)
    except StokTidakCukupError as e:
        print("Ditolak ->", e)

    # --- Validasi jumlah ---
    garis("Validasi: jumlah tidak valid")
    try:
        pelanggan.tambah_ke_keranjang(mie, 0)
    except ValueError as e:
        print("Ditolak ->", e)

    # --- Skenario 2: pesanan + pembayaran tunai ---
    garis("Skenario 2: Buat pesanan & bayar tunai")
    pesanan = pelanggan.buat_pesanan()
    print(pesanan)
    print("Stok Nasi Goreng sekarang:", nasi.stok)

    bayar_kurang = Pembayaran(pesanan, 20000)
    try:
        bayar_kurang.proses()
    except ValueError as e:
        print("Pembayaran gagal ->", e)

    bayar = Pembayaran(pesanan, 50000)
    kembalian = bayar.proses()
    print(f"Pembayaran berhasil. Kembalian: Rp{kembalian:,.0f}")
    print("Status:", pesanan.status.value)

    # --- Skenario 5: penjual mengubah status ---
    garis("Skenario 5: Penjual ubah status pesanan")
    penjual.ubah_status_pesanan(pesanan, StatusPesanan.SIAP_DIAMBIL)
    print("Status:", pesanan.status.value)
    penjual.ubah_status_pesanan(pesanan, StatusPesanan.SELESAI)
    print("Status:", pesanan.status.value)

    try:
        penjual.ubah_status_pesanan(pesanan, StatusPesanan.DIPROSES)
    except ValueError as e:
        print("Ditolak ->", e)

    # --- Pembatalan: stok dikembalikan ---
    garis("Pembatalan pesanan belum dibayar")
    pelanggan.tambah_ke_keranjang(mie, 2)
    pesanan2 = pelanggan.buat_pesanan()
    print("Stok Mie Ayam setelah pesan:", mie.stok)
    pesanan2.batalkan()
    print("Stok Mie Ayam setelah batal:", mie.stok)

    # --- Enkapsulasi: harga/stok tidak bisa diisi sembarangan ---
    garis("Enkapsulasi: validasi harga & stok")
    for atribut, nilai in (("harga", -500), ("stok", -1)):
        try:
            setattr(nasi, atribut, nilai)
        except ValueError as e:
            print("Ditolak ->", e)

    garis("Riwayat Pesanan Pelanggan")
    for p in pelanggan.riwayat_pesanan:
        print(p)


if __name__ == "__main__":
    main()