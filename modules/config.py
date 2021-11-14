from __main__ import checker
from modules.functions import ascii,clear
from colorama import Fore,init
from os import makedirs, listdir
from json import load, dump
init(autoreset=True)

default = {"proxy_type":"http","proxy_timeout":5,"threads":200,"retries":1,"print_mode":"cui"}

cyan = Fore.CYAN
reset = Fore.RESET

def load_config():
    while 1:
        try:
            makedirs("Data",exist_ok=True)
            if "config.json" not in listdir("Data"):
                with open("Data/config.json","w") as file:
                    dump(default,file,indent=4)
            with open("Data/config.json","r") as file:
                data = load(file)
            checker.proxy_type = str(data["proxy_type"]).lower()
            if checker.proxy_type not in ("http","socks4","socks5"):
                raise
            checker.retries = int(data["retries"])
            checker.timeout = int(data["proxy_timeout"])
            checker.threads = int(data["threads"])
            if checker.threads <= 0:
                checker.threads = 1
            cui = data["print_mode"].lower()
            if cui in ("log","cui"):
                if cui == "log":
                    checker.cui = False
                else:
                    checker.cui = True
                break
            else:
                raise
        except:
            with open("Data/config.json","w") as file:
                dump(default,file,indent=4)
            pass

def update_config(values:dict):
    makedirs("Data",exist_ok=True)
    with open("Data/config.json","w") as file:
        dump(values,file,indent=4)

def change(option:str):
    """
    Change a value in the config file
    change("threads")
    """
    values = {"proxy_type":checker.proxy_type,"proxy_timeout":checker.timeout,"threads":checker.threads,"retries":checker.retries,"print_mode":"cui" if checker.cui else "log"}
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
        values["proxy_type"] = checker.proxy_type
        update_config(values)
    elif option == "proxy_timeout":
        print(f"    [{cyan}Pick proxy timeout{reset}]")
        print("\n")
        try:
            timeout = int(input(f"    [{cyan}>{reset}] "))
            checker.timeout = timeout
            values["proxy_timeout"] = timeout
            update_config(values)
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
            values["retries"] = retries
            update_config(values)
        except:
            pass
    elif option == "print":
        if checker.cui == False:
            checker.cui = True
        else:
            checker.cui = False
        values["print_mode"] = "cui" if checker.cui else "log"
        update_config(values)
    elif option == "threads":
        print(f"    [{cyan}Pick ammount of threads{reset}]")
        print("\n")
        try:
            threads = int(input(f"    [{cyan}>{reset}] "))
            checker.threads = threads
            values["threads"] = threads
            update_config(values)
        except:
            pass