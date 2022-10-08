from modules.variables import Checker
from modules.functions import *

def start():
    reset_stats()
    while 1:
        clear()
        ascii()
        print("\n\n")
        print(f"    [{cyan}>{reset}] Pick Combo File")
        file_path = get_file("Combo File","Combo File")
        if not file_path:
            print(f"    [{cyan}>{reset}] No File Detected")
            sleep(1)
            return
        with open(file_path,errors="ignore") as file:
            original_combos = file.read().splitlines()
            after_combos = list(set(original_combos))
            duplicates = len(original_combos)-len(after_combos)
        if not len(original_combos):
            print(f"    [{red}>{reset}] No Combos Detected")
            sleep(1)
            return
        print(f"    [{cyan}>{reset}] Imported {green}{len(original_combos)}{reset} Combos")
        if duplicates != 0:
            print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} Duplicates")
        sleep(1)
        Checker.time = get_time()
        sort(after_combos)
        print("\n\n")
        print(f"    [{cyan}>{reset}] Finished Sorting Domains")
        print(f"    [{cyan}>{reset}] Saved to Results/{Checker.time}")
        input(f"    [{cyan}>{reset}] Press Enter To Go Back")
        return
def sort(combos):
    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}Please Wait, Sorting Domains{reset}]")
    for combo in combos:
        if not ":" in combo: continue
        
        email = combo.split(":")[0]
        if not "@" in email: continue
        
        domain = email.split("@")[1].lower().split(".")[0]
        save(f"@{domain}",None,Checker.time,combo)