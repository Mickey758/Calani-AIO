from modules.variables import Checker
from modules.functions import *
from time import sleep
from threading import Thread
from multiprocessing.dummy import Pool
from requests import Session
from requests.adapters import HTTPAdapter, Retry
import functools
import os

class Settings:
    proxy_type = 'http'

def start():
    clear()
    ascii()
    reset_stats()
    print(f"    [{cyan}>{reset}] Pick Proxy Type [HTTP/SOCKS4/SOCKS5/AUTO]")
    option = input(f'    [{cyan}>{reset}] ').lower()
    if option not in ['auto','http','socks4','socks5']:
        print(f"    [{red}Invalid Option{reset}]")
        sleep(1)
        return
    Settings.proxy_type = option

    print("\n")
    print(f"    [{cyan}>{reset}] Pick Proxy File")
    file_path = get_file("Proxy File",type="Proxy File")
    if not file_path:
        print(f"    [{red}No File Detected{reset}]")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        before_proxies = file.read().splitlines()
        proxies = list(set(before_proxies))
        Checker.accounts = proxies
        Checker.remaining = proxies.copy()
        duplicates = len(before_proxies) - len(proxies)
    if not before_proxies:
        print(f"    [{red}>{reset}] No Proxies Detected")
        sleep(1)
        return
    print(f"    [{cyan}>{reset}] Imported {green}{len(before_proxies)}{reset} Proxies")
    if duplicates != 0:
        print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} Duplicates")
    sleep(0.5)

    Checker.checking = True
    Checker.time = get_time()
    if Checker.cui: Thread(target=cui_2,daemon=True).start()
    Thread(target=title_2,daemon=True).start()
    Thread(target=level_cpm,daemon=True).start()

    clear()
    print(f"    [{cyan}Starting Threads{reset}]")
    mainpool = Pool(processes=Checker.threads)
    clear()
    if not Checker.cui:
        ascii()
    mainpool.imap_unordered(func=check,iterable=Checker.accounts)
    mainpool.close()
    mainpool.join()
    sleep(1)
    Checker.checking = False
    save_path = os.path.join(os.getcwd(),f'Results\\{Checker.time}')
    print(f"\n\n    [{cyan}>{reset}] Finished Checking Proxies")
    print(f"    [{cyan}>{reset}] Saved to \"{save_path}\"")
    input(f"    [{cyan}>{reset}] Press Enter To Go Back")

def check(proxy:str):
    if Settings.proxy_type == 'auto':
        for proxyType in ['http','socks4','socks5']:
            try:
                with Session() as s:
                    s.request = functools.partial(s.request, timeout=Checker.timeout)
                    retries = Retry(total=Checker.retries, backoff_factor=0.1)
                    s.proxies.update(set_proxy(proxy,proxyType))
                    s.mount('http://', HTTPAdapter(max_retries=retries))
                    s.mount('https://', HTTPAdapter(max_retries=retries))

                    url = 'http://httpbin.org/get'
                    r = s.get(url)
                    if r.url != url or r.status_code != 200: raise
                    Checker.good += 1

                    if not Checker.cui: log("good",proxy,proxyType.upper())
                    save(proxyType.title(),"good",Checker.time,proxy,False)
                    
                    Checker.cpm += 60
                    Checker.remaining.remove(proxy)
                    return
            except:
                Checker.cpm += 5
        
        Checker.bad += 1
        Checker.cpm += 60
        Checker.remaining.remove(proxy)
        return
    
        
    try:
        with Session() as s:
            s.request = functools.partial(s.request, timeout=Checker.timeout)
            retries = Retry(total=Checker.retries, backoff_factor=0.1)
            s.proxies.update(set_proxy(proxy))
            s.mount('http://', HTTPAdapter(max_retries=retries))
            s.mount('https://', HTTPAdapter(max_retries=retries))

            url = 'http://httpbin.org/get'
            r = s.get(url)
            if r.url != url or r.status_code != 200: raise
            
            Checker.good += 1
            
            if not Checker.cui: log("good",proxy,Settings.proxy_type.title())
            save(Settings.proxy_type.title(),"good",Checker.time,proxy,False)
    except:
        Checker.bad += 1
    finally:
        Checker.cpm += 60
        Checker.remaining.remove(proxy)
        return