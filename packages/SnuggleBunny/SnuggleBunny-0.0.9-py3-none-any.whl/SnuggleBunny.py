import argparse
import ipaddress
import re
import socket
import ssl
import time
from clear import clear

CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RED = "\033[1;31m"

fake_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
                "UPGRADE-INSECURE-REQUESTS": "1"}

def SnuggleBunny():
    clear()
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", required = True)
    parser.add_argument("-filename", default = "")
    args = parser.parse_args()
    
    hosts = []
    if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}", args.host):
        for i in list(ipaddress.ip_network(args.host, strict = False).hosts()):
            hosts.append(str(i))

    else:
        hosts.append(args.host)
        
    hits = []
    for host in hosts:
        print(f"{CYAN}CHECKING: {host}")

        # DNS
        dns = socket.getfqdn(host)
        if dns != host:
            hits.append(f"DNS: {dns}")
            print(f"DNS: {dns}")

        time.sleep(2.5)

        # CIPHER
        try:
            context = ssl.create_default_context()
            socket.setdefaulttimeout(10)
            with socket.create_connection((host, 443)) as sock:
                with context.wrap_socket(sock, server_hostname = host) as secure_sock:
                    ciphers = secure_sock.context.get_ciphers()
                    for cipher in ciphers:
                        time.sleep(1)
                        if "DES" in cipher["name"] or "EXP" in cipher["name"] or "MD5" in cipher["name"] or "NULL" in cipher["name"] or "RC4" in cipher["name"]:
                            if cipher["strength_bits"] < 128:
                                hits.append(f"OFFERS WEAK CIPHER and STRENGTH: {cipher['name']}  | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                                print(f"{RED}OFFERS WEAK CIPHER AND STRENGTH: {cipher['name']} | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")

                            elif cipher["protocol"] != "TLSv1.2" and cipher["protocol"] != "TLSv1.3":
                                hits.append(f"OFFERS WEAK CIPHER AND PROTOCOL: {cipher['name']} | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                                print(f"{RED}OFFERS WEAK CIPHER AND PROTOCOL: {cipher['name']} | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")

                            elif cipher["strength_bits"] < 128 and cipher["protocol"] != "TLSv1.2" and cipher["protocol"] != "TLSv1.3":
                                hits.append(f"OFFERS WEAK CIPHER, PROTOCOL, AND STRENGTH | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                                print(f"{RED}OFFERS WEAK CIPHER, PROTOCOL, AND STRENGTH | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                                
                            else:
                                hits.append(f"OFFERS WEAK CIPHER: {cipher['name']} | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                                print(f"{RED}OFFERS WEAK CIPHER: {cipher['name']} | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")

                        elif cipher["strength_bits"] < 128:
                            hits.append(f"OFFERS WEAK STRENGTH: {cipher['name']} | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                            print(f"{RED}OFFERS WEAK STRENGTH: {cipher['name']} | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")

                        elif cipher["protocol"] != "TLSv1.2" and cipher["protocol"] != "TLSv1.3":
                            hits.append(f"OFFERS WEAK PROTOCOL | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                            print(f"{RED}OFFERS WEAK PROTOCOL | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")

                        elif cipher["strength_bits"] < 128 and cipher["protocol"] != "TLSv1.2" and cipher["protocol"] != "TLSv1.3":
                            hits.append(f"OFFERS WEAK PROTOCOL AND STRENGTH | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                            print(f"{RED}OFFERS WEAK PROTOCOL AND STRENGTH | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")

                        else:
                            hits.append(f"OFFERS STRONG CIPHER, PROTOCOL, AND STRENGTH  | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")
                            print(f"{GREEN}OFFERS STRONG CIPHER, PROTOCOL, AND STRENGTH | NAME = {cipher['name']} | PROTOCOL = {cipher['protocol']} | STRENGTH = {cipher['strength_bits']} bits")

        except:
            pass

    if len(args.filename) > 0:
        with open(f"{args.filename}.txt", "w") as file:
            for hit in hits:
                file.write(hit)

    print(f"{CYAN}DONE!")

if __name__ == "__main__":
    SnuggleBunny()
