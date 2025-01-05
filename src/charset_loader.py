import os

def load_charset(file_path):
    """   
    Memuat file konfigurasi charset dan menguraikannya ke dalam kamus.
    :raises FileNotFoundError: Jika file tidak ditemukan di jalur yang ditentukan.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Charset file not found at: {file_path}")

    charsets = {}
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("[]")
                charsets[i + 1] = value  # Map index (starting at 1) ke string rangkaian karakter.
    return charsets