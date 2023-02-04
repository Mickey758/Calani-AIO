from modules.variables import *
from modules.functions import *
import os

def start():
    change_title(f"Calani AIO | Capture Remover | {discord_name}")
    reset_stats()
    
    clear()
    ascii()
    
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
    edit(after_combos)
    save_path = os.path.join(os.getcwd(),f'Results\\{Checker.time}')
    
    print(f"\n\n    [{cyan}>{reset}] Finished Removing Capture")
    print(f"    [{cyan}>{reset}] Saved to \"{save_path}\\Capture_Remove.txt\"")
    input(f"    [{cyan}>{reset}] Press Enter To Go Back")

def edit(combos):
    clear()
    ascii()
    print(f"    [{cyan}Please Wait, Removing Capture{reset}]")
    combo_number = 0
    to_save = []
    for combo in combos:
        combo_number += 1
        print(f'    [{cyan}{int((combo_number/len(combos))*100)}%{reset}]',end='\r')
        if not ":" in combo:
            continue
        
        email,password = combo.split(":",1)
        if " " in password: password = password.split(" ")[0]
        new_combo = ':'.join([email,password])

        if new_combo not in to_save: to_save.append(new_combo)
    
    save("Capture_Remove",None,Checker.time,"\n".join(to_save))
