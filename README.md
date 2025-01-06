# Passcrack

![Passcrack Logo](https://ibb.co.com/jhKBwrr)

Passcrack adalah alat yang dirancang untuk melakukan serangan brute force, dictionary attack, dan cracking hash menggunakan rainbow table. Alat ini membantu mengidentifikasi kata sandi yang lemah dan meningkatkan keamanan sistem.

[![Build Status](https://travis-ci.org/username/passcrack.svg?branch=master)](https://travis-ci.org/username/passcrack)

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

Passcrack memerlukan [Python 3.x](https://www.python.org/downloads/) untuk berjalan.

### Kloning Repository:
```sh
git clone https://github.com/username/passcrack.git
cd passcrack
```

### Instalasi Dependencies:
```sh
pip install -r requirements.txt
```

### Menjalankan Alat:
```sh
python3 passcrack.py
```

---

## Panduan Penggunaan

### Brute Force Attack

#### Contoh: Brute Force untuk Password Saja
```sh
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
```sh
python3 passcrack.py -d --url http://target/login -username usernames.txt -password passwords.txt
```

- **-d**: Mode dictionary attack.
- **-username**: File daftar username.
- **-password**: File daftar password.

---

### Rainbow Table

#### Contoh: Membuat Rainbow Table
```sh
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

Ingin berkontribusi? Hebat!

Kami menerima pull request untuk meningkatkan alat ini. Silakan buka issue di halaman repository kami untuk diskusi lebih lanjut.

