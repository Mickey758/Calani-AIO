from colorama import init
from time import sleep
from modules.updater import check as check_updates
from modules.variables import Checker
import keyboard
from modules.config import *
from modules.functions import *
from modules.start import starter,modules_list
import modules.tools.proxychecker as proxychecker
import modules.tools.proxyscraper as proxyscraper
import modules.tools.capture_remove as captureremover
import modules.tools.comboeditor as comboeditor
import modules.tools.domainsorter as domainsorter

def home():
    while 1:
        change_title("Calani AIO | Home | MickeyYe#9423")
        clear()
        ascii()
        print("\n\n")
        print(f"""    [{cyan}Main Menu{reset}]
    
    [{cyan}1{reset}] Modules
    [{cyan}2{reset}] Tools
    [{cyan}3{reset}] Settings
    [{cyan}4{reset}] Info

    [{cyan}X{reset}] Exit""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": modules()
        elif option == "2": tools()
        elif option == "3": settings()
        elif option == "4": info()
        elif option == "x": return

def info():
    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}Info{reset}]\n")
    print(f"""    [{cyan}>{reset}] Created By: MickeyYe#9423
    [{cyan}>{reset}] Wanna Make A Donation?
        BTC: bc1qt6gcll4hp7wwqaap7x3lwunf9srw4enuxxddzn
        ETH: 0xd7F5C1AB4765Be15F738367905bF4E7Ea83eC9F7
        LTC: LdsjBD8ACvqUinrgbJJvCcELs2AxN5NSpc

    [{cyan}>{reset}] If you payed for this application, you were SCAMMED!

    Press Enter To Go Back""",end="")
    input()

def modules():
    selected_modules = []
    while 1:
        change_title("Calani AIO | Modules | MickeyYe#9423")
        clear()
        ascii()
        print("\n\n")
        print(f"    [{cyan}Modules{reset}]\n")
        
        for module in modules_list:
            index = list(modules_list).index(module)+1
            selected = f"{cyan}+{reset}" if module in selected_modules else " "
            print(f"    [{selected}] [{cyan}{index}{reset}] {module.title()}")
        
        print(f"""
    [{cyan}>{reset}] Choose A Number To Select/Deselect A Module
    [{cyan}>{reset}] Seperate Numbers With ',' To Select Multiple Modules Faster

    [{cyan}>{reset}] Selected Modules: {len(selected_modules)}/{len(modules_list)}
    [{cyan}A{reset}] Select/Deselect All
    [{cyan}S{reset}] Start Checking

    [{cyan}X{reset}] Back""")
        
        option = input(f"    [{cyan}>{reset}] ").lower()
        
        if option.isdigit():
            if int(option) <= len(modules_list) and int(option):
                module = list(modules_list)[int(option)-1]
                selected_modules.append(module) if module not in selected_modules else selected_modules.remove(module)
        
        elif "," in option:
            selects = option.split(",")
            for option in selects:
                if option.isdigit():
                    if int(option) <= len(modules_list) and int(option):
                        module = list(modules_list)[int(option)-1]
                        selected_modules.append(module) if module not in selected_modules else selected_modules.remove(module)
        
        elif option == "s":
            if selected_modules:
                starter(selected_modules)
                selected_modules.clear()
            else:
                print(f"    [{cyan}>{reset}] Must select at least 1 module!")
                sleep(1)
        
        elif option == "a":
            if len(selected_modules) == len(modules_list): selected_modules.clear()
            else:
                for module in modules_list:
                    if module not in selected_modules: selected_modules.append(module)
        
        elif option == "x": return

def settings():
    while 1:
        load_config()
        change_title("Calani AIO | Settings | MickeyYe#9423")
        clear()
        ascii()
        print("\n\n")
        print(f"""    [{cyan}Settings{reset}]

    [{cyan}1{reset}] Proxy Type : {Checker.proxy_type.title()}
    [{cyan}2{reset}] Proxy Timeout : {Checker.timeout}s
    [{cyan}3{reset}] Print Mode : {"CUI" if Checker.cui else "LOG"}
    [{cyan}4{reset}] Retries : {Checker.retries}
    [{cyan}5{reset}] Threads : {Checker.threads}

    [{cyan}X{reset}] Back""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": change("proxy_type")
        elif option == "2": change("proxy_timeout")
        elif option == "3": change("print")
        elif option == "4": change("retries")
        elif option == "5": change("threads")
        elif option == "x": return

def tools():
    while 1:
        load_config()
        change_title("Calani AIO | Tools | MickeyYe#9423")
        clear()
        ascii()
        print("\n\n")
        print(f"""    [{cyan}Tools{reset}]

    [{cyan}1{reset}] Proxy Checker
    [{cyan}2{reset}] Proxy Scraper
    [{cyan}3{reset}] Capture Remover
    [{cyan}4{reset}] Combo Editor
    [{cyan}5{reset}] Domain Sorter

    [{cyan}X{reset}] Back""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": proxychecker.start()
        elif option == "2": change_title("Calani AIO | Proxy Scraper | MickeyYe#9423");proxyscraper.start()
        elif option == "3": change_title("Calani AIO | Capture Remover | MickeyYe#9423");captureremover.start()
        elif option == "4": change_title("Calani AIO | Combo Editor | MickeyYe#9423");comboeditor.start()
        elif option == "5": change_title("Calani AIO | Domain Sorter | MickeyYe#9423");domainsorter.start()
        elif option == "x": return

if __name__ == "__main__":
    init(autoreset=True)
    load_config()
    keyboard.add_hotkey("s",save_lines)
    clear()
    ascii()
    print("\n\n")
    if not check_updates(): home()
    else:
        print(f"    [{red}>{reset}] Your version is outdated!")
        print(f"    [{cyan}>{reset}] Find the latest version of Calani AIO here: https://github.com/Mickey758/Calani-AIO/releases")
        input(f"    [{cyan}>{reset}] Press enter to ignore")
        home()
