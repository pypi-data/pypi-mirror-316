import argparse
import ftplib
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

def SnuggleBunny():
    clear()
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", required = True)
    parser.add_argument("-vuln", action = "store_true")
    args = parser.parse_args()

    hosts = []
    if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}", args.host):
        for i in list(ipaddress.ip_network(args.host, strict = False).hosts()):
            hosts.append(str(i))

    else:
        hosts.append(args.host)
        

    hits = {}
    mal = ["3DES", "ANY", "DES", "MD5", "NULL", "RC4", "SSL", "TLSv1.0", "TLSv1.1", "TRACE"]
    methods = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]

    for host in hosts:
        results = []
        print(f"{CYAN}checking: {host}")
        dns = socket.getfqdn(host)
        results.append(f"DNS: {dns}")
        
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

        try:
            ftp_client = ftplib.FTP(host, timeout = 10)
            ftp_client.login()
            ftp_client.quit()
            results.append("ANONYMOUS FTP ALLOWED")

        except:
            pass

        try:
            ftp_client = ftplib.FTP_TLS(host, timeout = 10)
            ftp_client.login()
            ftp_client.quit()
            results.append("ANONYMOUS FTP TLS ALLOWED")

        except:
            pass

        if ssl_support:
            try:
                my_request = urllib.request.Request(f"https://{host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "GET")
                my_request = urllib.request.urlopen(my_request, timeout = 10).headers
                banner = my_request["server"]
                results.append(f"WEB BANNER: {banner}")

            except:
                pass

        else:
            try:
                my_request = urllib.request.Request(f"http://{host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "GET")
                my_request = urllib.request.urlopen(my_request, timeout = 10).headers
                banner = my_request["server"]
                results.append(f"WEB BANNER: {banner}")

            except:
                pass

        for i in methods:
            if ssl_support:
                try:
                    my_request = urllib.request.Request(f"https://{host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = i)
                    my_request = urllib.request.urlopen(my_request, timeout = 10)
                    results.append(f"{i} METHOD ALLOWED")

                except:
                    pass

            else:
                try:
                    my_request = urllib.request.Request(f"http://{host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = i)
                    my_request = urllib.request.urlopen(my_request, timeout = 10)
                    results.append(f"{i} METHOD ALLOWED")

                except:
                    pass

        if ssl_support:
            try:
                my_request = urllib.request.Request(f"https://{host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "*")
                my_request = urllib.request.urlopen(my_request, timeout = 10)
                results.append("ANY METHOD ALLOWED")

            except:
                pass

        else:
            try:
                my_request = urllib.request.Request(f"http://{host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "*")
                my_request = urllib.request.urlopen(my_request, timeout = 10)
                results.append("ANY METHOD ALLOWED")

            except:
                pass

        hits.update({host: results})

    clear()
    if args.vuln:
        results = hits.copy()
        hits = {}
        for key, value in results.items():
            temp = []
            for i in value:
                if any(keyword in i for keyword in mal):
                    temp.append(i)

            hits.update({key: temp})

        hits = json.dumps(hits, indent = 4)
        print(f"{RED}{hits}")
                        
    else:
        hits = json.dumps(hits, indent = 4)
        print(f"{GREEN}{hits}")

if __name__ == "__main__":
    SnuggleBunny()
