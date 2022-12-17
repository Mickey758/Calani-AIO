from modules.variables import Checker
from modules.functions import *
from time import sleep
from threading import Thread
from multiprocessing.dummy import Pool
from requests import Session
from requests.adapters import HTTPAdapter, Retry
import functools
import os

def start():
    clear()
    ascii()
    reset_stats()
    print("\n\n")
    print(f"    [{cyan}Selected Proxy Type: {Checker.proxy_type.title()}{reset}]")
    print("\n")
    print(f"    [{cyan}>{reset}] Pick Proxy File")
    file_path = get_file("Proxy File",type="Proxy File")
    if not file_path:
        print(f"    [{cyan}No File Detected{reset}]")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        before_proxies = file.read().splitlines()
        proxies = list(set(before_proxies))
        Checker.accounts = proxies
        Checker.remaining = proxies.copy()
        duplicates = len(before_proxies) - len(proxies)
    if not len(before_proxies):
        print(f"    [{red}>{reset}] No Proxies Detected")
        sleep(1)
        return
    print(f"    [{cyan}>{reset}] Imported {green}{len(before_proxies)}{reset} Accounts")
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
    ascii()
    if not Checker.cui:
        print("\n\n")
    mainpool.imap_unordered(func=check,iterable=Checker.accounts)
    mainpool.close()
    mainpool.join()
    sleep(1)
    Checker.checking = False
    print("\n\n")
    save_path = os.path.join(os.getcwd(),f'Results\\{Checker.time}')
    print(f"    [{cyan}>{reset}] Finished Checking Proxies")
    print(f"    [{cyan}>{reset}] Saved to \"{save_path}\"")
    input(f"    [{cyan}>{reset}] Press Enter To Go Back")

def check(proxy:str):
    while 1:
        try:
            with Session() as s:
                s.request = functools.partial(s.request, timeout=Checker.timeout)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.proxies.update(set_proxy(proxy))
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                s.get("http://httpbin.org/get")
                Checker.good += 1
                
                if not Checker.cui: log("good",proxy,Checker.proxy_type.title())
                save(Checker.proxy_type.title(),"good",Checker.time,proxy)
        except:
            Checker.bad += 1
        finally:
            Checker.cpm += 60
            Checker.remaining.remove(proxy)
            return