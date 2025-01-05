import argparse
import os

def show_banner():
    print("""
██████╗  █████╗ ███████╗███████╗     ██████╗██████╗  █████╗  ██████╗██╗  ██╗
██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
██████╔╝███████║███████╗███████╗    ██║     ██████╔╝███████║██║     █████╔╝
██╔═══╝ ██╔══██║╚════██║╚════██║    ██║     ██╔══██╗██╔══██║██║     ██╔═██╗
██║     ██║  ██║███████║███████║    ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
────────────────────────────────────────────────────────────────────────────
                    PASSWORD CRACKING TOOL by PBL-RKS503
────────────────────────────────────────────────────────────────────────────
    """)

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Password Cracking Tool Eith Brute Force, Dictionary Attack, and Rainbow Table Operations."
    )

    # Subparsers untuk rainbow table
    subparsers = parser.add_subparsers(dest="command", help="Rainbow table operations")

    rtgen_parser = subparsers.add_parser("rtgen", help="Generate a rainbow table")
    rtgen_parser.add_argument("hash_algorithm", type=str, help="Hash algorithm (e.g., md5, sha256)")
    rtgen_parser.add_argument("charset", type=str, help="Charset name (e.g., loweralpha, loweralpha-numeric)")
    rtgen_parser.add_argument("min_len", type=int, help="Minimum plaintext length")
    rtgen_parser.add_argument("max_len", type=int, help="Maximum plaintext length")
    rtgen_parser.add_argument("chain_count", type=int, help="Number of chains to generate")

    rtsort_parser = subparsers.add_parser("rtsort", help="Sort rainbow tables")
    rtsort_parser.add_argument("directory", type=str, help="Directory containing rainbow tables")

    rcrack_parser = subparsers.add_parser("rcrack", help="Crack hashes using rainbow tables")
    rcrack_parser.add_argument("--hash", type=str, help="Hash to crack")
    rcrack_parser.add_argument("--file", type=str, help="File containing hashes to crack")
    rcrack_parser.add_argument("--algorithm", type=str, default="md5", help="Hash algorithm")

    # Opsi brute-force dan dictionary attack
    parser.add_argument("-b", action="store_true", help="Use brute-force method")
    parser.add_argument("-d", action="store_true", help="Use dictionary attack method")
    parser.add_argument("--url", type=str, help="Target login page URL")
    parser.add_argument("-username", nargs="?", const="", help="Fixed username or empty for brute-forcing username")
    parser.add_argument("-password", nargs="?", const="", help="Fixed password or empty for brute-forcing password")
    parser.add_argument("-domain", nargs="?", const="", help="Domain for username (e.g., @example.com)")
    parser.add_argument("-c", nargs="*", type=int, choices=range(1, 8), help="Charset option (one or two values)")
    parser.add_argument("-t", nargs="?", const=2, type=int, help="Brute-force time limit in minutes (default is 2 minutes)")
    parser.add_argument("-length", nargs="*", type=int, help="Length for brute-forced username and/or password")
    parser.add_argument("--sc", type=int, help="Filter by status code")

    return parser

def validate_args(args):
    if args.b and not any([args.url, args.username, args.password, args.domain, args.c, args.length]):
        print_usage()
        exit(1)

    if args.d and not any([args.url, args.username, args.password]):
        print_usage()
        exit(1)

    if args.b:
        if args.username is None:
            raise ValueError("Username parameter is required.")

        if args.password is None:
            raise ValueError("Password parameter is required.")

        if args.domain is not None and args.domain.strip() == "":
            raise ValueError("Please enter a domain name")

        if args.c is None or len(args.c) == 0:
            raise ValueError("Charset parameter (-c) is required.")

        if args.length is None or len(args.length) == 0:
            raise ValueError("Length parameter (-length) is required.")

        if args.username and args.username.strip() and args.password and args.password.strip():
            raise ValueError("Error: Both -username and -password are fixed. Nothing to brute force.")

    if args.sc:
        try:
            status_codes = [int(sc.strip()) for sc in str(args.sc).split(',')]
            for sc in status_codes:
                if not 100 <= sc <= 599:
                    raise ValueError(f"Invalid status code: {sc}")
        except ValueError as e:
            raise ValueError(f"Invalid status code format: {str(e)}")
        
def print_usage():
    print("""
Usage:
  passcrack -b [options]         # Brute force attack
  passcrack -d [options]         # Dictionary attack
  passcrack rtgen [args]         # Generate a rainbow table
  passcrack rtsort [args]        # Sort rainbow tables
  passcrack rcrack [args]        # Crack hashes using rainbow tables

For more details, use -h or refer to the documentation.
""")

def custom_help():
    print("""
A Tool For Cracking Passwords Using Brute Force, Dictionary Attacks, and Rainbow Table.

Brute Force and Dictionary Attack Operations

usage: passcrack -b --url -domain -username -password -c -length --sc -t
       passcrack -d --url -domain -username -password --sc -t

Brute Force and Dictionary Options:

       -h, --help     : show this help message and exit
       --url          : The target URL for the login page to be attacked.
       --sc           : Filter by status code (example: 302 for redirect).
       -b             : Use the Brute Force method to try all username/password combinations.
       -d             : Use the Dictionary Attack method with the given username/password file.
       -username      : Fixed or empty username for brute-forcing username.
       -password      : Fixed or empty password for brute-forcing password.
       -domain        : An additional domain for the username, such as @example.com.
       -c             : Select the charset for the characters to be used in the brute force (see charset.txt).
       -t             : Brute force timeout in minutes (default: 2 minutes).
       -length        : The length of the brute force username/password. Can be one number or two numbers (example: 4 6).


Rainbow Table Operations

usage: passcrack rtgen hash_algorithm charset plaintext_len_min plaintext_len_max chain_len
       passcrack rtsort .
       passcrack rcrack -h 5d41402abc4b2a76b9719d911017c592
       passcrack rcrack -l hash.txt

hash algorithms implemented:

       md5     : HashLen=16 PlaintextLen=0-15
       sha1    : HashLen=20 PlaintextLen=0-20
       sha224  : HashLen=28 PlaintextLen=0-20
       sha256  : HashLen=32 PlaintextLen=0-20
       sha384  : HashLen=48 PlaintextLen=0-20
       sha512  : HashLen=64 PlaintextLen=0-20

Rainbow Table Options:

       -h, --help     : show this help message and exit
       rtgen          : Generate a rainbow table
       rtsort         : Sort rainbow tables
       rcrack         : Crack hashes using rainbow tables
       hash_algorithm : Hash algorithm (e.g., md5, sha256)
       charset        : Charset name (e.g., loweralpha, loweralpha-numeric)
       min_len        : Minimum plaintext length
       max_len        : Maximum plaintext length
       chain_count    : Number of chains to generate
       directory      : Directory containing rainbow tables
       --hash         : Hash to crack
       --file         : File containing hashes to crack


Examples:
1. Brute force only password:
   passcrack -b --url example.com -domain @example.com -username example -password -c 5 -length 4 -t 3

2. Brute force only username:
   passcrack -b --url example.com -domain @example.com -username -password example -c 5 -length 4 -t 3

3. Brute force username and password:
   passcrack -b --url example.com -domain @example.com -username -password -c 6 5 -length 7 4 -t 3

4. Dictionary Attack:
   passcrack -d --url example.com -domain @example.com -username usernames.txt -password passwords.txt -t 3


5. Generate Rainbow Table:
   passcrack rtgen md5 loweralpha 4 6 1000

6. Sort Rainbow Table:
   passcrack rtsort .

7. Crack Hash with one hash:
   passcrack rcrack --hash ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb

8. Crack Hash with File containing a list of hashes:
   passcrack rcrack --file hash.txt
""")

def display_charsets():
    print("""
Available Charsets:
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
1. alpha                  = [ABCDEFGHIJKLMNOPQRSTUVWXYZ]
2. alpha-numeric          = [ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]
3. alpha-numeric-symbol14 = [ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=]
4. all                    = [abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=~`[]{}|\:;"'<>,.?/]
5. numeric                = [0123456789]
6. loweralpha             = [abcdefghijklmnopqrstuvwxyz]
7. loweralpha-numeric     = [abcdefghijklmnopqrstuvwxyz0123456789]
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """)