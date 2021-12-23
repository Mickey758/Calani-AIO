from modules.variables import Checker
from modules.functions import *
from colorama import Fore,init
from os import makedirs, listdir
from json import load, dump

default = {"proxy_type":"http","proxy_timeout":5,"threads":200,"retries":1,"print_mode":"cui","share":False}

def load_config():
    """Load the config values"""
    while 1:
        try:
            with open("Data/config.json","r") as file: data = load(file)
            Checker.proxy_type = str(data["proxy_type"]).lower()
            Checker.retries = int(data["retries"])
            Checker.timeout = int(data["proxy_timeout"])
            Checker.threads = int(data["threads"])
            Checker.share = bool(data['share'])
            cui = data["print_mode"].lower()
            if Checker.threads <= 0: Checker.threads = 1
            if Checker.proxy_type not in ("http","socks4","socks5"): raise
            if cui not in ("log","cui"): raise
            Checker.cui = False if cui == "log" else True
            break
        except:
            makedirs("Data",exist_ok=True)
            with open("Data/config.json","w") as file: dump(default,file,indent=4)

def update_config(values:dict):
    """Update the config values"""
    makedirs("Data",exist_ok=True)
    with open("Data/config.json","w") as file: dump(values,file,indent=4)

def change(option:str):
    """
    Change a value in the config file
    change("threads")
    """
    values = {"proxy_type":Checker.proxy_type,"proxy_timeout":Checker.timeout,"threads":Checker.threads,"retries":Checker.retries,"print_mode":"cui" if Checker.cui else "log","share":Checker.share}
    clear()
    ascii()
    print("\n\n")
    if option == "proxy_type":
        if Checker.proxy_type == "http":
            Checker.proxy_type = "socks4"
        elif Checker.proxy_type == "socks4":
            Checker.proxy_type = "socks5"
        elif Checker.proxy_type == "socks5":
            Checker.proxy_type = "http"
        values["proxy_type"] = Checker.proxy_type
        update_config(values)
    elif option == "proxy_timeout":
        print(f"    [{cyan}Pick proxy timeout{reset}]")
        print("\n")
        try:
            timeout = int(input(f"    [{cyan}>{reset}] "))
            Checker.timeout = timeout
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
            Checker.retries = retries
            values["retries"] = retries
            update_config(values)
        except:
            pass
    elif option == "print":
        if Checker.cui == False:
            Checker.cui = True
        else:
            Checker.cui = False
        values["print_mode"] = "cui" if Checker.cui else "log"
        update_config(values)
    elif option == "threads":
        print(f"    [{cyan}Pick ammount of threads{reset}]")
        print("\n")
        try:
            threads = int(input(f"    [{cyan}>{reset}] "))
            Checker.threads = threads
            values["threads"] = threads
            update_config(values)
        except:
            pass
    elif option == "share":
        Checker.share = False if Checker.share else True
        values["share"] = Checker.share
        update_config(values)