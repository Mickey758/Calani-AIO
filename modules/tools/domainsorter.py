from modules.variables import Checker
from modules.functions import *

def start():
    reset_stats()
    while 1:
        clear()
        ascii()
        print("\n\n")
        clear()
        ascii()
        print("\n\n")
        print(f"    [{cyan}Pick Combo File{reset}]")
        file_path = get_file("Combo File","Combo File")
        get_focus()
        if not file_path:
            print(f"    [{cyan}No File Detected{reset}]")
            sleep(1)
            return
        with open(file_path,errors="ignore") as file:
            original_combos = file.read().splitlines()
            after_combos = list(set(original_combos))
            duplicates = len(original_combos)-len(after_combos)
        print(f"    [{cyan}Imported {len(original_combos)} Combos{reset}]")
        if duplicates != 0:
            print(f"    [{cyan}Removed {duplicates} Duplicates{reset}]")
        sleep(1)
        Checker.time = get_time()
        sort(after_combos)
        print("\n\n")
        print(f"    [{cyan}Finished Sorting Domains{reset}]")
        input(f"    [{cyan}Press Enter To Go Back{reset}]")
        return
def sort(combos):
    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}Please Wait, Sorting Domains{reset}]")
    for combo in combos:
        if ":" in combo:
            email = combo.split(":")[0]
            if "@" in email:
                domain = email.split("@")[1].lower().split(".")[0]
                save("@"+domain,None,Checker.time,combo)