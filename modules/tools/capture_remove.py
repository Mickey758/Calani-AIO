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
            print(f"    [{cyan}>{reset}] Removed {duplicates} Duplicates")
        sleep(1)
        Checker.time = get_time()
        edit(after_combos)
        print("\n\n")
        print(f"    [{cyan}>{reset}] Finished Removing Capture")
        input(f"    [{cyan}>{reset}] Press Enter To Go Back")
        return
def edit(combos):
    for combo in combos:
        if not ":" in combo:
            continue
        
        email = combo.split(":")[0].rstrip()
        password = combo.split(":")[1]
        if " " in password: password = password.split(" ")[0]
        log(None,":".join([email,password]))
        save("Capture_Remove",None,Checker.time,":".join([email,password]))
