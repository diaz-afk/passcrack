import os
import random
import time
import requests
from tabulate import tabulate

BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

def start_fuzzing(args, charsets):
    # Set default status code if not provided
    default_sc = 302
    if not args.sc:
        args.sc = default_sc

    # Prepare log and table directories
    log_dir = "log"
    table_dir = "Table"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(table_dir):
        os.makedirs(table_dir)

    # Dictionary attack preparation
    if args.d:
        username_file = os.path.basename(args.username)
        password_file = os.path.basename(args.password)

    base_log_file = f"{log_dir}/dictionary-attack_log" if args.d else f"{log_dir}/brute-force_log"
    log_file = f"{base_log_file}1.txt"
    counter = 1
    while os.path.exists(log_file):
        counter += 1
        log_file = f"{base_log_file}{counter}.txt"

    # Print starting configuration
    print("\n🔧 Configuration:")
    print("──────────────────────────────────────────────────────")
    print(f"Target URL       : {args.url}")
    if args.b:
        print("Method           : Brute-force")
    elif args.d:
        print("Method           : Dictionary Attack")
        print(f"Username File    : {username_file}")
        print(f"Password File    : {password_file}")

    # Tambahkan domain jika ada
    if args.domain:
        print(f"Domain           : {args.domain}")

    # Print Status Code jika --sc diberikan oleh user
    if args.sc != default_sc:
        print(f"Status Code      : {args.sc}")

    if args.c:
        charsets_list = args.c if isinstance(args.c, list) else [args.c]
        if len(charsets_list) == 2:
            username_charset = charsets[charsets_list[0]]
            password_charset = charsets[charsets_list[1]]
            if args.username == '':
                print(f"Username Charset : ({charsets_list[0]}) {username_charset}")
            if args.password == '':
                print(f"Password Charset : ({charsets_list[1]}) {password_charset}")
        else:
            common_charset = charsets[charsets_list[0]]
            if args.username == '':
                print(f"Username Charset : ({charsets_list[0]}) {common_charset}")
            if args.password == '':
                print(f"Password Charset : ({charsets_list[0]}) {common_charset}")

    if args.length:
        if len(args.length) == 2:
            if args.username == '':
                print(f"Username Length  : {args.length[0]} characters")
            if args.password == '':
                print(f"Password Length  : {args.length[1]} characters")
        else:
            if args.username == '':
                print(f"Username Length  : {args.length[0]} characters")
            if args.password == '':
                print(f"Password Length  : {args.length[0]} characters")

    if args.t:
        time_limit_seconds = args.t * 60
        print(f"Time Limit       : {args.t} minutes ({time_limit_seconds} seconds)")
    else:
        print("Time Limit       : None (running indefinitely)")
    print("──────────────────────────────────────────────────────")

    results = []
    status_counts = {}
    weak_passwords = []
    start_time = time.time()
    time_limit = args.t * 60 if args.t else None

    # Progress tracker
    total_attempts = 0
    found_weak_password = False

    try:
        # Dictionary attack
        if args.d:
            usernames = load_payload(args.username)
            passwords = load_payload(args.password)

            for username in usernames:
                if args.domain:
                    username += args.domain
                for password in passwords:
                    total_attempts += 1
                    response, elapsed_time = make_attempt(args.url, username, password)

                    # Proses respons
                    found_weak_password = process_response(
                        total_attempts, username, password, response, elapsed_time,
                        results, status_counts, weak_passwords, args.sc
                    )

                    # Waktu Tersisa jika -t diberikan
                    if time_limit:
                        elapsed = time.time() - start_time
                        remaining_time = int(time_limit - elapsed)
                        if remaining_time <= 0:
                            print("\nTime limit reached.")
                            raise KeyboardInterrupt
                        print(
                            f"Time Remaining: {remaining_time // 60} minutes {remaining_time % 60} seconds",
                            end="\r"
                        )
                    else:
                        progress = (total_attempts % 100) / 100
                        print(f"Please wait, loading progress ({int(progress * 100)}%)", end="\r")

            # Output setelah payload selesai
            print("\nDictionary Attack completed.")
            print(f"Total Attempts: {total_attempts}")
            filtered_results = [res for res in results if res[0] == args.sc]
            displayed_table, remaining_table, table_file = print_table(
                filtered_results, filter_status=args.sc,
                status_counts=status_counts, table_dir=table_dir, mode="dictionary-attack"
            )

            if displayed_table:
                print("\nWeak Password Detected:")
                for entry in displayed_table:
                    username, password = entry[5].split(" - ")
                    print(f"ID: {entry[0]} | Username: {username} | Password: {password} | Time: {entry[6]} ms")

            if remaining_table:
                with open(table_file, "a") as f:
                    f.write("\nWeak Password Detected (Continued):\n")
                    for entry in remaining_table:
                        username, password = entry[5].split(" - ")
                        f.write(f"ID: {entry[0]} | Username: {username} | Password: {password} | Time: {entry[6]} ms\n")
                print(f"📁 Weak Password Detected (continued) saved in {table_file}")

            if not filtered_results:
                print("\n📁 Log:")
                print(f"Log saved in {log_file}")
                save_log(results, log_file)

        # Brute-force attack
        elif args.b:
            while (time_limit is None or time.time() - start_time < time_limit):
                total_attempts += 1

                # Pastikan args.c selalu berupa list
                charsets_list = args.c if isinstance(args.c, list) else [args.c]
                try:
                    if len(charsets_list) == 2:  # Jika dua charset diberikan
                        charset_username = charsets[charsets_list[0]]
                        charset_password = charsets[charsets_list[1]]
                    else:  # Jika satu charset diberikan
                        charset_username = charsets[charsets_list[0]]
                        charset_password = charsets[charsets_list[0]]
                except (IndexError, KeyError):
                    print("Invalid charset selection. Please ensure correct values from charset.txt.")
                    return

                # Tentukan panjang untuk username dan password
                if args.length and len(args.length) == 2:  # Jika dua panjang diberikan
                    length_username = args.length[0]
                    length_password = args.length[1]
                else:  # Jika satu panjang diberikan
                    length_username = length_password = args.length[0]

                # Logika brute force username dan password
                if args.username and not args.password:  # Brute-force hanya password
                    username = args.username
                    password = generate_random_string(length_password, charset_password)
                elif args.password and not args.username:  # Brute-force hanya username
                    username = generate_random_string(length_username, charset_username)
                    password = args.password
                else:  # Brute-force username dan password
                    username = generate_random_string(length_username, charset_username)
                    password = generate_random_string(length_password, charset_password)

                # Tambahkan domain jika ada
                if args.domain:
                    username += args.domain

                # Kirim percobaan login
                response, elapsed_time = make_attempt(args.url, username, password)
                found_weak_password = process_response(
                    total_attempts, username, password, response, elapsed_time, results, status_counts, weak_passwords, args.sc
                )

                # Show progress or countdown timer
                if time_limit:
                    remaining_time = int(time_limit - (time.time() - start_time))
                    print(f"Time Remaining: {remaining_time // 60} minutes {remaining_time % 60} seconds", end="\r")
                else:
                    progress = (total_attempts % 100) / 100
                    print(f"Please wait, loading progress ({int(progress * 100)}%)", end="\r")

            # Setelah waktu habis
            total_time = time.time() - start_time
            print("\nBrute force completed.")
            print(f"Total Time Elapsed: {total_time:.2f} seconds")
            print(f"Total Attempts: {total_attempts}")

            # Tampilkan hasil akhir
            filtered_results = [res for res in results if res[0] == args.sc]
            displayed_table, remaining_table, table_file = print_table(
                filtered_results, filter_status=args.sc, status_counts=status_counts, table_dir=table_dir, mode="brute-force"
            )

            # Weak Password Detected
            if displayed_table:
                print("\nWeak Password Detected:")
                for entry in displayed_table:
                    username, password = entry[5].split(" - ")
                    print(f"ID: {entry[0]} | Username: {username} | Password: {password} | Time: {entry[6]} ms")

            if remaining_table:
                with open(table_file, "a") as f:
                    f.write("\nWeak Password Detected (Continued):\n")
                    for entry in remaining_table:
                        username, password = entry[5].split(" - ")
                        f.write(f"ID: {entry[0]} | Username: {username} | Password: {password} | Time: {entry[6]} ms\n")
                print(f"📁 Weak Password Detected (continued) saved in {table_file}")

            if not filtered_results:
                print("\n📁 Log:")
                print(f"Log saved in {log_file}")
                save_log(results, log_file)

    except KeyboardInterrupt:
        print("\nStopped by user.")
        print(f"Total Attempts: {total_attempts}")

        # Display results on interrupt
        filtered_results = [res for res in results if res[0] == args.sc]
        displayed_table, remaining_table, table_file = print_table(
            filtered_results, filter_status=args.sc, status_counts=status_counts, table_dir=table_dir, mode="dictionary-attack" if args.d else "brute-force"
        )

        # Handle Weak Password Detected
        if displayed_table:
            print("\nWeak Password Detected:")
            for entry in displayed_table:
                username, password = entry[5].split(" - ")
                print(f"ID: {entry[0]} | Username: {username} | Password: {password} | Time: {entry[6]} ms")

        if remaining_table:
            with open(table_file, "a") as f:
                f.write("\nWeak Password Detected (Continued):\n")
                for entry in remaining_table:
                    username, password = entry[5].split(" - ")
                    f.write(f"ID: {entry[0]} | Username: {username} | Password: {password} | Time: {entry[6]} ms\n")
            print(f"📁 Weak Password Detected (continued) saved in {table_file}")

        if not filtered_results:
            print("\n📁 Log:")
            print(f"Log saved in {log_file}")
            save_log(results, log_file)


# Fungsi Pendukung
def make_attempt(url, username, password):
    start = time.time()
    try:
        response = attempt_login(url, username, password)
        elapsed_time = (time.time() - start) * 1000
        return response, elapsed_time
    except requests.exceptions.RequestException:
        print("Error: The provided URL is not reachable. Please check the URL and try again.")
        exit(1)

def process_response(user_id, username, password, response, elapsed_time, results, status_counts, weak_passwords, filter_status):
    status = response.status_code
    length = len(response.text)
    lines = len(response.text.splitlines())
    cols = max(len(line) for line in response.text.splitlines()) if lines > 0 else 0
    chars = len(response.content)

    results.append([status, length, lines, cols, chars, f"{username} - {password}", elapsed_time])

    if filter_status and status == filter_status:
        weak_passwords.append({"id": user_id, "username": username, "password": password, "time": elapsed_time})
        return True

    if status in status_counts:
        status_counts[status] += 1
    else:
        status_counts[status] = 1

    return False

def attempt_login(url, username, password):
    data = {'username': username, 'password': password}
    return requests.post(url, data=data, allow_redirects=False)

def save_log(results, log_file):
    with open(log_file, 'w') as f:
        for result in results:
            f.write("==================================================\n")
            f.write(f"Attempted login with ID: {result[0]}, Username: {result[5].split(' - ')[0]}, Password: {result[5].split(' - ')[1]}\n")
            f.write(f"Response Status: {result[0]}\n")
            f.write(f"Response Length: {result[1]} characters\n")
            f.write(f"Response Received in: {result[6]:.2f} ms\n")
            f.write(f"Lines: {result[2]}, Max Columns: {result[3]}, Total Characters: {result[4]}\n")
            f.write("==================================================\n")

def load_payload(filepath):
    with open(filepath, "r") as f:
        return [line.strip() for line in f.readlines()]

def generate_random_string(length, charset):
    return ''.join(random.choice(charset) for _ in range(length))

def print_table(results, filter_status, status_counts, table_dir="Table", mode="brute-force"):
    headers = ["ID", "Response", "Lines", "Columns", "Chars", "Payload", "Response Time (ms)"]
    table = []

    for i, res in enumerate(results):
        if filter_status is None or res[0] == filter_status:
            table.append([f"{i:08d}:", res[0], res[2], res[3], res[4], res[5], f"{res[6]:.2f}"])

    # Tentukan log file dengan counter
    base_log_file = f"{table_dir}/{mode}_table"
    table_file = f"{base_log_file}1.txt"
    counter = 1
    while os.path.exists(table_file):
        counter += 1
        table_file = f"{base_log_file}{counter}.txt"

    # Jika lebih dari 20 baris ditemukan
    if len(table) > 20:
        print(tabulate(table[:20], headers=headers, tablefmt="grid"))
        print(f"\nMore than 20 rows found. \n📁 The remaining rows are saved in {table_file}\n")
        with open(table_file, "w") as f:
            f.write(tabulate(table, headers=headers, tablefmt="grid"))
    elif len(table) > 0:
        print(tabulate(table, headers=headers, tablefmt="grid"))
    else:
        print("No matching response code found.")

    return table[:20], table[20:], table_file  # Mengembalikan baris untuk Weak Password Detected