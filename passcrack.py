#!/usr/bin/env python3
import sys
from src.options import parse_args, show_banner, custom_help, print_usage, display_charsets, validate_args
from src.core import start_fuzzing
from src.rtcore import generate_rainbow_table, rtsort, rcrack
from src.charset_loader import load_charset

def main():
    # Tampilkan banner
    show_banner()

    # Tampilkan charsets jika --charset diberikan
    if "--charset" in sys.argv:
        display_charsets()
        sys.exit(0)

    # Tampilkan custom help jika diminta
    if "-h" in sys.argv or "--help" in sys.argv:
        custom_help()
        sys.exit(0)

    # Ambil argumen
    parser = parse_args()
    args = parser.parse_args()

    # Validasi argumen
    try:
        validate_args(args)
    except ValueError as e:
        print(f"Input Error: {e}")
        print_usage()
        sys.exit(1)

    # Pilih jalur eksekusi berdasarkan sub-command atau metode
    if args.command == "rtgen":
        generate_rainbow_table(args.hash_algorithm, args.charset, args.min_len, args.max_len, args.chain_count)
    elif args.command == "rtsort":
        rtsort(args.directory)
    elif args.command == "rcrack":
        rcrack(hash_value=args.hash, hash_file=args.file, algorithm=args.algorithm)
    elif args.b or args.d:
        # Jalankan metode brute-force atau dictionary attack
        if not args.url:
            print("Error: Target URL is required for brute-force or dictionary attack.\n")
            print_usage()
            sys.exit(1)
        charsets = load_charset("src/charset.txt")
        start_fuzzing(args, charsets)
    else:
        print_usage()

if __name__ == "__main__":
    main()