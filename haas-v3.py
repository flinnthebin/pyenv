#!/usr/bin/env python

import re
import requests

BASE_URL = "https://haas-v3.quoccacorp.com"
HEADERS = {
    "Host": "kb.quoccacorp.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "http://haas.quoccacorp.com/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://haas.quoccacorp.com",
    "Connection": "keep-alive"
}

s = requests.Session()
s.cert = "/home/archer/uni/COMP6843/z3291100.pem"
visited = set()

request_template = """GET {path} HTTP/1.1\r
Host: kb.quoccacorp.com\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r
Accept-Language: en-US,en;q=0.5\r
Referer: http://haas.quoccacorp.com/\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 0\r
Origin: http://haas.quoccacorp.com\r
Connection: keep-alive\r
\r
"""


def crawl(path):
    """Recursively crawls the given path to search for the flag."""
    if path in visited:
        return None  # Skip already visited pages
    visited.add(path)

    try:
        response = s.post(
            BASE_URL,
            data={"requestBox": request_template.format(path=path)}
        )
        content = response.text

        # Search for flag
        match = re.search(r"COMP6443{.+?}", content)
        if match:
            print(f"{match.group(0)}")
            return match.group(0)

        # Find new /deep/... links and crawl further
        new_links = re.findall(r'href="(/deep/[\w\d]+)"', content)
        for link in new_links:
            flag = crawl(link)
            if flag:
                return flag

    except requests.RequestException as e:
        print(f"Request failed for {path}: {e}")

    return None


# Start crawling from /deep
flag = crawl("/deep")

if not flag:
    print("Flag not found.")
