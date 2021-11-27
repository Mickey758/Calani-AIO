from colorama import Fore,init
from time import sleep
from console.utils import set_title
from modules.updater import check as check_updates
from threading import Lock

red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
reset = Fore.RESET
lock = Lock()

class checker:
    bad = 0
    good = 0
    custom = 0
    cpm = 0
    errors = 0

    saving = False
    checking = False
    proxies = []
    bad_proxies = []
    accounts = []
    accounts_down = []
    time = ""

    cui = True
    retries = 1
    timeout = 5
    threads = 200
    proxy_type = "socks4"

from modules.config import *
from modules.functions import *
from modules.start import starter,modules_list
import modules.tools.proxychecker as proxychecker
import modules.tools.proxyscraper as proxyscraper
import modules.tools.capture_remove as captureremover

load_config()

def home():
    while 1:
        set_title("Calani AIO | Home | MickeyYe#0003")
        clear()
        ascii()
        print("\n\n")
        print(f"""
    [{cyan}1{reset}] Modules
    [{cyan}2{reset}] Tools
    [{cyan}3{reset}] Settings

    [{cyan}X{reset}] Exit""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": modules()
        if option == "2": tools()
        elif option == "3": settings()
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
    [{cyan}5{reset}] Duolingo
    [{cyan}6{reset}] Gfuel
    [{cyan}7{reset}] Crunchyroll
    [{cyan}8{reset}] SpotifyVM
    [{cyan}9{reset}] Buffalo Wild Wings
   [{cyan}10{reset}] Pornhub
   [{cyan}11{reset}] Valorant
   [{cyan}12{reset}] Honeygain
   [{cyan}13{reset}] DiscordVM
   [{cyan}14{reset}] Netflix
   [{cyan}15{reset}] Steam

    [{cyan}>{reset}] Selected Modules: {str([x.title() for x in selected_modules]).replace("'","").replace("', '",", ")}
    [{cyan}A{reset}] Add All Modules
    [{cyan}S{reset}] Start Checking

    [{cyan}X{reset}] Back""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": selected_modules.append("minecraft") if "minecraft" not in selected_modules else selected_modules.remove("minecraft")
        elif option == "2": selected_modules.append("nordvpn") if "nordvpn" not in selected_modules else selected_modules.remove("nordvpn")
        elif option == "3": selected_modules.append("bonk.io") if "bonk.io" not in selected_modules else selected_modules.remove("bonk.io")
        elif option == "4": selected_modules.append("disney+") if "disney+" not in selected_modules else selected_modules.remove("disney+")
        elif option == "5": selected_modules.append("duolingo") if "duolingo" not in selected_modules else selected_modules.remove("duolingo")
        elif option == "6": selected_modules.append("gfuel") if "gfuel" not in selected_modules else selected_modules.remove("gfuel")
        elif option == "7": selected_modules.append("crunchyroll") if "crunchyroll" not in selected_modules else selected_modules.remove("crunchyroll")
        elif option == "8": selected_modules.append("spotifyvm") if "spotifyvm" not in selected_modules else selected_modules.remove("spotifyvm")
        elif option == "9": selected_modules.append("bww") if "bww" not in selected_modules else selected_modules.remove("bww")
        elif option == "10": selected_modules.append("pornhub") if "pornhub" not in selected_modules else selected_modules.remove("pornhub")
        elif option == "11": selected_modules.append("valorant") if "valorant" not in selected_modules else selected_modules.remove("valorant")
        elif option == "12": selected_modules.append("honeygain") if "honeygain" not in selected_modules else selected_modules.remove("honeygain")
        elif option == "13": selected_modules.append("discordvm") if "discordvm" not in selected_modules else selected_modules.remove("discordvm")
        elif option == "14": selected_modules.append("netflix") if "netflix" not in selected_modules else selected_modules.remove("netflix")
        elif option == "15": selected_modules.append("steam") if "steam" not in selected_modules else selected_modules.remove("steam")
        elif option == "s":
            if selected_modules != []:
                starter(selected_modules)
                return
            else:
                print(f"    [{cyan}>{reset}] Must select at least 1 module!")
                sleep(1)
        elif option == "a":
            for module in modules_list:
                if module not in selected_modules:
                    selected_modules.append(module)
        elif option == "x":
            return
def settings():
    while 1:
        load_config()
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
def tools():
    while 1:
        load_config()
        set_title("Calani AIO | Tools | MickeyYe#0003")
        clear()
        ascii()
        print("\n\n")
        print(f"""
    [{cyan}1{reset}] Proxy Checker
    [{cyan}2{reset}] Proxy Scraper
    [{cyan}3{reset}] Capture Remover

    [{cyan}X{reset}] Back""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        if option == "1": proxychecker.start()
        elif option == "2": set_title("Calani AIO | Proxy Scraper | MickeyYe#0003");proxyscraper.start()
        elif option == "3": set_title("Calani AIO | Capture Remover | MickeyYe#0003");captureremover.start()
        elif option == "x": return

if __name__ == "__main__":
    init(autoreset=True)
    clear()
    ascii()
    print("\n\n")
    update = check_updates()
    if not update:
        home()
    else:
        print(f"    [{red}>{reset}] Your version is outdated!")
        print(f"    [{cyan}>{reset}] Find the latest version of Calani AIO here: https://github.com/Mickey758/Calani-AIO/releases")
        input(f"    [{cyan}>{reset}] Press enter to ignore")
        home()
