import argparse
import os
import hashlib
import re
import time
import pickle
from itertools import product
from src.options import parse_args

# Ekstensi file untuk tabel rainbow
RAINBOW_TABLE_EXT = ".rt"

def load_charset(charset_name):
    """
    Load a charset from the default charset configuration file.
    """
    charset_file = "charset.txt" # Nama file charset
    try:
        with open(charset_file, 'r') as f:
            content = f.read()
        # Cari charset berdasarkan nama yang diberikan
        pattern = rf"^{charset_name}\s*=\s*\[(.*?)\]"
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            # Format ulang charset menjadi daftar karakter
            charset = match.group(1).replace(',', '').replace('"', '').replace(' ', '')
            return list(charset)
        else:
            raise ValueError(f"Charset '{charset_name}' not found in {charset_file}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Charset file {charset_file} not found")
    except Exception as e:
        raise RuntimeError(f"Error loading charset: {e}")

def generate_rainbow_table(hash_func, charset_name, min_len, max_len, chain_count):
    """
    Generate a rainbow table with the given parameters.
    """
    charset = load_charset(charset_name) # Muat charset
    table_name = f"{hash_func}_{charset_name}#{min_len}-{max_len}_{chain_count}.rt"

    # Periksa jika tabel sudah ada
    if os.path.exists(table_name):
        overwrite = input(f"Table {table_name} already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() != 'y':
            print("Aborting table generation.")
            return

    hash_function = getattr(hashlib, hash_func) # Ambil fungsi hash dari hashlib
    print("──────────────────────────────────────────────────────")
    print(f"rainbow table {table_name} parameters")
    print("──────────────────────────────────────────────────────")
    print(f"hash algorithm:         {hash_func}")
    print(f"hash length:            {hash_function().digest_size}")
    print(f"charset name:           {charset_name}")
    print(f"charset data:           {''.join(charset)}")
    print(f"charset length:         {len(charset)}")
    print(f"plaintext length range: {min_len} - {max_len}")
    print("──────────────────────────────────────────────────────")
    print("generating...")
    print("──────────────────────────────────────────────────────")
    start_time = time.time()
    table = []
    chain_idx = 0  # Indeks rantai saat ini

    # Membuat kombinasi plaintext dalam rentang panjang tertentu
    plaintexts = (
        ''.join(p) for length in range(min_len, max_len + 1)
        for p in product(charset, repeat=length)
    )

    try:
        for chain_idx in range(chain_count):
            try:
                plaintext = next(plaintexts) # Ambil plaintext berikutnya
            except StopIteration:
                print("\nNot enough unique plaintexts to generate the requested number of chains.")
                break

            hash_value = hash_function(plaintext.encode()).hexdigest() # Hash plaintext
            table.append((plaintext, hash_value)) # Tambahkan ke tabel

            # Dynamic progress update (overwrite previous line)
            elapsed_time = time.time() - start_time
            print(f"\r{chain_idx + 1} of {chain_count} rainbow chains generated ({elapsed_time:.1f} s)", end="")

    except KeyboardInterrupt:
        elapsed_time = time.time() - start_time
        print(f"\nCTRL+C detected! {chain_idx + 1} of {chain_count} rainbow chains generated ({elapsed_time:.1f} s)")
        print("Stopping generation and saving progress...")

    # Simpan tabel dalam format biner
    with open(table_name, 'wb') as f:
        pickle.dump(table, f)

    print(f"\n📁 Generated table saved to {table_name} with {len(table)} entries")

def load_rainbow_table(file_path):
    """Loads a rainbow table from a file."""
    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except (pickle.UnpicklingError, EOFError, FileNotFoundError) as e:
        print(f"Error loading file {file_path}: {e}")
        return None

def rtsort(directory):
    """Sorts rainbow tables in the given directory by endpoint."""
    for filename in os.listdir(directory):
        if filename.endswith(RAINBOW_TABLE_EXT):
            file_path = os.path.join(directory, filename)
            print(f"{file_path}: ")
            print("loading data...")
            table = load_rainbow_table(file_path)
            if table is None:
                print("Skipping file due to loading error.")
                continue
            print("sorting data...")
            # Urutkan berdasarkan hash
            table.sort(key=lambda chain: chain[1])
            print("writing sorted data...")
            with open(file_path, "wb") as file:
                pickle.dump(table, file)

def hash_plaintext(plaintext, algorithm):
    """Hashes a plaintext string using the specified algorithm."""
    hash_function = getattr(hashlib, algorithm)
    return hash_function(plaintext.encode()).hexdigest()

def crack_hash_single(hash_value, algorithm, rainbow_tables):
    """Cracks a single hash using the provided rainbow tables."""
    for table_path in rainbow_tables:
        print(f"disk: {table_path}: reading data")
        table = load_rainbow_table(table_path)
        if table is None:
            print("Skipping table due to loading error.")
            continue

        for plaintext, stored_hash in table:
            # Periksa apakah hash cocok
            if stored_hash == hash_value:
                return plaintext

    return None

def rcrack(hash_value=None, hash_file=None, algorithm="md5"):
    """Cracks hashes using rainbow tables in the current directory."""
    rainbow_tables = [os.path.join(os.getcwd(), f) for f in os.listdir(os.getcwd()) if f.endswith(RAINBOW_TABLE_EXT)]
    print(f"{len(rainbow_tables)} rainbow tables found")

    if hash_value:
        print("────────────────────────────────────────────────────────────────────────────────────────")
        print(f"disk: starting to process hash {hash_value}")
        start_time = time.time()
        plaintext = crack_hash_single(hash_value, algorithm, rainbow_tables)
        total_time = time.time() - start_time

        print("────────────────────────────────────────────────────────────────────────────────────────")
        print("\ndisk: finished reading all files")
        if plaintext:
            print(f"plaintext of {hash_value} is {plaintext}")
        else:
            print(f"plaintext of {hash_value} is <not found>")

        print("\nstatistics")
        print("──────────────────────────────────────────────────────")
        print(f"plaintext found:                             {'1 of 1' if plaintext else '0 of 1'}")
        print(f"total time:                                  {total_time:.2f} s")

        print("\nresult")
        print("──────────────────────────────────────────────────────")
        print(f"{hash_value}  {plaintext if plaintext else '<not found>'}")

    elif hash_file:
        print(f"disk: starting to process hashes in {hash_file}")
        with open(hash_file, "r") as file:
            hashes = [line.strip() for line in file]

        start_time = time.time()
        found_count = 0

        results = []
        for h in hashes:
            plaintext = crack_hash_single(h, algorithm, rainbow_tables)
            results.append((h, plaintext))
            if plaintext:
                found_count += 1

        total_time = time.time() - start_time
        print("──────────────────────────────────────────────────────")
        print("\ndisk: finished reading all files")
        for h, plaintext in results:
            if plaintext:
                print(f"plaintext of {h} is {plaintext}")
            else:
                print(f"plaintext of {h} is <not found>")

        print("\nstatistics")
        print("──────────────────────────────────────────────────────")
        print(f"plaintext found:                             {found_count} of {len(hashes)}")
        print(f"total time:                                  {total_time:.2f} s")

        print("\nresult")
        print("──────────────────────────────────────────────────────")
        for h, plaintext in results:
            print(f"{h}  {plaintext if plaintext else '<not found>'}")

if __name__ == "__main__":
    args = parse_args()
    if args.command == "rtgen":
        generate_rainbow_table(args.hash_algorithm, args.charset, args.min_len, args.max_len, args.chain_count)
    elif args.command == "rtsort":
        rtsort(args.directory)
    elif args.command == "rcrack":
        rcrack(hash_value=args.hash, hash_file=args.file, algorithm=args.algorithm)
