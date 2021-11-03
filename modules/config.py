from __main__ import checker
from modules.functions import ascii,clear
from colorama import Fore,init

init(autoreset=True)

cyan = Fore.CYAN
reset = Fore.RESET

def change(option:str):
    """
    Change a value in the config file
    change("threads")
    """
    clear()
    ascii()
    print("\n\n")
    if option == "proxy_type":
        if checker.proxy_type == "http":
            checker.proxy_type = "socks4"
        elif checker.proxy_type == "socks4":
            checker.proxy_type = "socks5"
        elif checker.proxy_type == "socks5":
            checker.proxy_type = "http"
    elif option == "proxy_timeout":
        print(f"    [{cyan}Pick proxy timeout{reset}]")
        print("\n")
        try:
            timeout = int(input(f"    [{cyan}>{reset}] "))
            checker.timeout = timeout
        except:
            pass
    elif option == "retries":
        print(f"    [{cyan}Pick check retries{reset}]")
        print("\n")
        try:
            retries = int(input(f"    [{cyan}>{reset}] "))
            if retries <= 0:
                retries = 1
            checker.retries = retries
        except:
            pass
    elif option == "print":
        if checker.cui == False:
            checker.cui = True
        else:
            checker.cui = False
    elif option == "threads":
        print(f"    [{cyan}Pick ammount of threads{reset}]")
        print("\n")
        try:
            threads = int(input(f"    [{cyan}>{reset}] "))
            checker.threads = threads
        except:
            pass