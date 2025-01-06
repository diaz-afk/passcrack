Berikut adalah dokumentasi Passcrack yang ditulis dalam format **Markdown (.md)**:

```markdown
# Passcrack

**Passcrack** adalah alat yang dirancang untuk melakukan serangan brute force, dictionary attack, dan cracking hash menggunakan rainbow table. Alat ini membantu mengidentifikasi kata sandi yang lemah dan meningkatkan keamanan sistem.

---

## Fitur Utama

- **Brute Force**: Mencoba berbagai kombinasi username dan password berdasarkan panjang dan karakter tertentu.
- **Dictionary Attack**: Menggunakan daftar username dan password yang telah ditentukan untuk mencocokkan kredensial.
- **Rainbow Table**:
  - Membuat rainbow table baru.
  - Mengurutkan rainbow table untuk efisiensi.
  - Memecahkan hash menggunakan rainbow table.

---

## Disclaimer

Alat ini dirancang untuk pengujian keamanan dengan izin resmi. Penggunaan untuk aktivitas ilegal atau tanpa izin sepenuhnya menjadi tanggung jawab pengguna.

---

## Instalasi

### Kloning Repository:
```bash
git clone https://github.com/username/passcrack.git
cd passcrack
```

### Persyaratan:
Pastikan Python 3.x dan pustaka yang dibutuhkan terinstal:
```bash
pip install -r requirements.txt
```

### Jalankan Alat:
```bash
python3 passcrack.py
```

---

## Panduan Penggunaan

### Brute Force Attack

#### Contoh: Brute Force untuk Password Saja
```bash
python3 passcrack.py -b --url http://target/login -username admin -password -c 5 -length 4
```

- **-b**: Mode brute force.
- **--url**: URL target.
- **-username**: Username tetap.
- **-password**: Password dicari dengan brute force.
- **-c**: Charset (angka).
- **-length**: Panjang password (4 karakter).

---

### Dictionary Attack

#### Contoh: Dictionary Attack untuk Kombinasi File Username dan Password
```bash
python3 passcrack.py -d --url http://target/login -username usernames.txt -password passwords.txt
```

- **-d**: Mode dictionary attack.
- **-username**: File daftar username.
- **-password**: File daftar password.

---

### Rainbow Table

#### Contoh: Membuat Rainbow Table
```bash
python3 passcrack.py rtgen md5 loweralpha 4 6 1000
```

- **rtgen**: Membuat rainbow table.
- **md5**: Algoritma hash.
- **loweralpha**: Karakter (a-z).
- **4**: Panjang minimum.
- **6**: Panjang maksimum.
- **1000**: Jumlah chain.

---

## Troubleshooting

### Masalah Umum

1. **Invalid charset option**
   - **Solusi**: Periksa kembali nilai charset yang digunakan.

2. **Kesalahan parameter**
   - **Solusi**: Sesuaikan parameter dengan panduan di atas.

3. **File tidak ditemukan**
   - **Solusi**: Pastikan file username/password ada di lokasi yang benar.

---

## Kontribusi

Kami menerima kontribusi untuk meningkatkan alat ini. Silakan kirim pull request atau buka issue di halaman repository.

---

## Lisensi

Alat ini dilindungi oleh **MIT License**.

---

## Dokumentasi Tambahan

Silakan baca manual [Passcrack Manual](Manual_Book_Passcrack.pdf) untuk detail lebih lanjut.
```

### Cara Menggunakan
1. Simpan file ini sebagai `README.md`.
2. Unggah ke root repository proyek Anda di GitHub.
3. Markdown ini akan secara otomatis ditampilkan sebagai dokumentasi di halaman utama repository Anda.

Jika Anda ingin menambahkan gambar atau bagian lain, beri tahu saya, dan saya akan membantu Anda menyesuaikannya! 😊
