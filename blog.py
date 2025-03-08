#!/usr/bin/env python

import re
import requests

s = requests.Session()

s.cert = "/home/archer/uni/COMP6843/z3291100.pem"
flag_pattern = re.compile(r"COMP6443\{.+?\}")

for i in range(1, 20):
    url = f"https://blog.quoccacorp.com/?page_id={i}/"
    r = s.get(url)

    match = flag_pattern.search(r.text)
    if match:
        print(match.group(0))
        exit(0)
