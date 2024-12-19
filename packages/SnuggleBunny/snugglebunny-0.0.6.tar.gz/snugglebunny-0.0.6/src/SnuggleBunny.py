import argparse
import http.cookiejar
import ipaddress
import json
import re
import socket
import ssl
import time
import urllib.request
from clear import clear

CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RED = "\033[1;31m"

fake_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
                "UPGRADE-INSECURE-REQUESTS": "1"}

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

def SnuggleBunny():
    clear()
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", required = True)
    parser.add_argument("-delay", default = 0)
    parser.add_argument("-filename", default = "")
    args = parser.parse_args()

    hosts = []
    if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}", args.host):
        for i in list(ipaddress.ip_network(args.host, strict = False).hosts()):
            hosts.append(str(i))

    else:
        hosts.append(args.host)
        
    hits = {}
    for host in hosts:
        results = []
        print(f"{CYAN}CHECKING: {host}")

        # DNS
        dns = socket.getfqdn(host)
        if dns != host:
            results.append(f"DNS: {dns}")

        time.sleep(args.delay)

        # CIPHER        
        ssl_support = False
        try:
            context = ssl.create_default_context()
            with socket.create_connection((host, 443)) as sock:
                sock.settimeout(10)
                with context.wrap_socket(sock, server_hostname = host) as secure_sock:
                    ssl_support = True
                    results.append(f"TLS VERSION: {secure_sock.version()}")
                    ciphers = secure_sock.context.get_ciphers()
                    for cipher in ciphers:
                        results.append(f"CIPHER SUPPORTED: {cipher['name']}")

        except:
            pass

        time.sleep(args.delay)

        # WEB BANNER
        if ssl_support:
            try:
                my_request = urllib.request.Request(f"https://{host}", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10).headers
                banner = my_request["server"]
                results.append(f"WEB BANNER: {banner}")

            except:
                pass

        else:
            try:
                my_request = urllib.request.Request(f"http://{host}", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10).headers
                banner = my_request["server"]
                results.append(f"WEB BANNER: {banner}")

            except:
                pass

        time.sleep(args.delay)

        # BACKEND
        if ssl_support:
            try:
                my_request = urllib.request.Request(f"https://{host}", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10).headers
                backend = my_request["x-powered-by"]
                if backend:
                    results.append(f"BACKEND: {backend}")

            except:
                pass

        else:
            try:
                my_request = urllib.request.Request(f"http://{host}", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10).headers
                backend = my_request["x-powered-by"]
                if backend:
                    results.append(f"BACKEND: {backend}")

            except:
                pass

        time.sleep(args.delay)

        # DJANGO
        if ssl_support:
            try:
                my_request = urllib.request.Request(f"https://{host}", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10).read()
                for cookie in cookie_jar:
                    if cookie.name == "csrftoken" or cookie.name == "csrf":
                        results.append(f"DJANGO FOUND")

            except:
                pass

        else:
            try:
                my_request = urllib.request.Request(f"http://{host}", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10).read()
                for cookie in cookie_jar:
                    if cookie.name == "csrftoken" or cookie.name == "csrf":
                        results.append(f"DJANGO FOUND")

            except:
                pass

        time.sleep(args.delay)

        # API
        if ssl_support:
            try:
                my_request = urllib.request.Request(f"https://{host}/api", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10)
                if my_request.status == 200:
                    results.append(f"API FOUND: {my_request.url}")

            except:
                pass

        else:
            try:
                my_request = urllib.request.Request(f"http://{host}/api", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10)
                if my_request.status == 200:
                     results.append(f"API FOUND: {my_request.url}")

            except:
                pass

        time.sleep(args.delay)
        
        # ADMIN
        if ssl_support:
            try:
                my_request = urllib.request.Request(f"https://{host}/admin", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10)
                if my_request.status == 200:
                    results.append(f"ADMIN FOUND: {my_request.url}")

            except:
                pass

        else:
            try:
                my_request = urllib.request.Request(f"http://{host}/admin", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10)
                if my_request.status == 200:
                    results.append(f"ADMIN FOUND: {my_request.url}")

            except:
                pass

        time.sleep(args.delay)
        
        # WORDPRESS
        for i in ["licence.txt", "readme.html", "wp-admin"]:
            if ssl_support:
                try:
                    my_request = urllib.request.Request(f"https://{host}/{i}", headers = fake_headers, unverifiable = True)
                    my_request = opener.open(my_request, timeout = 10)
                    if my_request.status == 200:
                        results.append(f"WORDPRESS FOUND: {my_request.url}")

                except:
                    pass

            else:
                try:
                    my_request = urllib.request.Request(f"http://{host}/{i}", headers = fake_headers, unverifiable = True)
                    my_request = opener.open(my_request, timeout = 10)
                    if my_request.status == 200:
                        results.append(f"WORDPRESS FOUND: {my_request.url}")

                except:
                    pass

        if results:
            hits.update({host: results})

    clear()
    hits = json.dumps(hits, indent = 4)
    if len(args.filename) > 0:
        with open(f"{args.filename}.json", "w") as json_file:
                json_file.write(hits)

    print(f"{GREEN}{hits}")

if __name__ == "__main__":
    SnuggleBunny()
