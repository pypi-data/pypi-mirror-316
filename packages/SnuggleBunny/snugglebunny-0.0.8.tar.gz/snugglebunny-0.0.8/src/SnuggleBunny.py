import argparse
import http.cookiejar
import ipaddress
import json
import re
import socket
import ssl
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
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar), urllib.request.HTTPRedirectHandler())

def SnuggleBunny():
    clear()
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", required = True)
    parser.add_argument("-filename", default = "")
    args = parser.parse_args()

    methods = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]
    
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

        if ssl_support:
            try:
                # REQUEST
                my_request = urllib.request.Request(f"https://{host}", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10)

                # WEB BANNER
                banner = my_request.headers["server"]
                results.append(f"WEB BANNER: {banner}")

                # BACKEND
                backend = my_request.headers["x-powered-by"]
                if backend:
                    results.append(f"BACKEND: {backend}")

                # DJANGO
                for cookie in cookie_jar:
                    if cookie.name == "csrftoken" or cookie.name == "csrf":
                        results.append(f"DJANGO FOUND")

            except:
                pass

        else:
            try:
                # REQUEST
                my_request = urllib.request.Request(f"https://{host}", headers = fake_headers, unverifiable = True)
                my_request = opener.open(my_request, timeout = 10)

                # WEB BANNER
                banner = my_request.headers["server"]
                results.append(f"WEB BANNER: {banner}")

                # BACKEND
                backend = my_request.headers["x-powered-by"]
                if backend:
                    results.append(f"BACKEND: {backend}")

                # DJANGO
                for cookie in cookie_jar:
                    if cookie.name == "csrftoken" or cookie.name == "csrf":
                        results.append(f"DJANGO FOUND")

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
