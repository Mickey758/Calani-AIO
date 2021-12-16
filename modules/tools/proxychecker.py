from modules.variables import Checker
from modules.functions import *
from time import sleep
from threading import Thread
from multiprocessing.dummy import Pool
from requests import get

def start():
    clear()
    ascii()
    reset_stats()
    print("\n\n")
    print(f"    [{cyan}Selected Proxy Type: {Checker.proxy_type.title()}{reset}]")
    print("\n")
    print(f"    [{cyan}Pick Proxy File{reset}]")
    sleep(1)
    file_path = get_file("Proxy File",type="Proxy File")
    get_focus()
    if not file_path:
        print(f"    [{cyan}No File Detected{reset}]")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        before_proxies = file.read().splitlines()
        proxies = list(set(before_proxies))
        Checker.accounts = proxies
        Checker.accounts_down = proxies
        duplicates = len(before_proxies) - len(proxies)
    print(f"    [{cyan}Imported {len(before_proxies)} Proxies{reset}]")
    if duplicates != 0:
        print(f"    [{cyan}Removed {duplicates} Duplicates{reset}]")
    sleep(1)

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
    mainpool.imap_unordered(func=check,iterable=Checker.accounts_down)
    mainpool.close()
    mainpool.join()
    sleep(5)
    Checker.checking = False
    print("\n\n")
    print(f"    [{cyan}Finished Checking{reset}]")
    input(f"    [{cyan}Press Enter To Go Back{reset}]")

def check(proxy:str):
    retries = 0
    while retries != Checker.retries:
        try:
            get("http://httpbin.org/get",proxies=set_proxy(proxy),timeout=Checker.timeout)
            Checker.good += 1
            Checker.cpm += 1
            if not Checker.cui:
                log("good",proxy,Checker.proxy_type.title())
            save(Checker.proxy_type.title(),"good",Checker.time,proxy)
            return
        except:
            retries += 1
    Checker.bad += 1
    Checker.cpm += 1
    return
