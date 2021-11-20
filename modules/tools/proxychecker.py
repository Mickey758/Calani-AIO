from __main__ import checker
from modules.functions import *
from colorama import Fore,init
from time import sleep
from threading import Thread
from multiprocessing.dummy import Pool
from requests import get

red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
reset = Fore.RESET
init(autoreset=True)

def start():
    clear()
    ascii()
    reset_stats()
    print("\n\n")
    print(f"    [{cyan}Selected Proxy Type: {checker.proxy_type.title()}{reset}]")
    print("\n")
    print(f"    [{cyan}Pick Proxy File{reset}]")
    sleep(1)
    file_path = get_file("Proxy File",type="Proxy File")
    if not file_path:
        print(f"    [{cyan}No File Detected{reset}]")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        before_proxies = file.read().splitlines()
        proxies = list(set(before_proxies))
        checker.accounts = proxies
        checker.accounts_down = proxies
        duplicates = len(before_proxies) - len(proxies)
    print(f"    [{cyan}Imported {len(before_proxies)} Proxies{reset}]")
    if duplicates != 0:
        print(f"    [{cyan}Removed {duplicates} Duplicates{reset}]")
    sleep(1)

    checker.checking = True
    checker.time = get_time()
    if checker.cui: Thread(target=cui_2,daemon=True).start()
    Thread(target=title_2,daemon=True).start()
    Thread(target=level_cpm,daemon=True).start()

    clear()
    print(f"    [{cyan}Starting Threads{reset}]")
    mainpool = Pool(processes=checker.threads)
    clear()
    ascii()
    if not checker.cui:
        print("\n\n")
    mainpool.imap_unordered(func=check,iterable=checker.accounts_down)
    mainpool.close()
    mainpool.join()
    sleep(5)
    checker.checking = False
    print("\n\n")
    print(f"    [{cyan}Finished Checking{reset}]")
    input(f"    [{cyan}Press Enter To Go Back{reset}]")

def check(proxy:str):
    retries = 0
    while retries != checker.retries:
        try:
            get("http://httpbin.org/get",proxies=set_proxy(proxy),timeout=checker.timeout)
            checker.good += 1
            checker.cpm += 1
            if not checker.cui:
                log("good",proxy,checker.proxy_type.title())
            save(checker.proxy_type.title(),"good",checker.time,proxy)
            return
        except:
            retries += 1
    checker.bad += 1
    checker.cpm += 1
    if not checker.cui:
        log("bad",proxy,checker.proxy_type.title())
    return
