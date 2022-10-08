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
            print(f"    [{red}>{reset}] No File Detected")
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
        print("\n\n")
        print(f"    [{cyan}>{reset}] Finished Editing Combo")
        print(f"    [{cyan}>{reset}] Saved to Results/{Checker.time}/Combo_Editor.txt")
        input(f"    [{cyan}>{reset}] Press Enter To Go Back")
        return
def edit(combos):
    edited = []
    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}Please Wait, Editing Combo{reset}]")
    acc = 0
    for combo in combos:
        acc += 1
        print(f'    [{cyan}{int((acc/len(combos))*100)}%{reset}]')
        if not ":" in combo: continue
        email,password = combo.split(":")
        if not email or not password: continue

        passwords = []
        passwords.append(password)
        passwords.append(f"{password[0].upper()}{password[1:]}")
        passwords.append(f"{password[0].upper()}{password[1:]}1")
        passwords.append(f"{password[0].upper()}{password[1:]}12")
        passwords.append(f"{password[0].upper()}{password[1:]}123")
        passwords.append(f"{password[0].upper()}{password[1:]}1234")
        passwords.append(f"{password[0].upper()}{password[1:]}12345")
        passwords.append(f"{password[0].upper()}{password[1:]}!")
        passwords.append(f"{password[0].upper()}{password[1:]}?")
        passwords.append(f"{password[0].upper()}{password[1:]}@")
        passwords.append(f"{password[0].lower()}{password[1:]}")
        passwords.append(f"{password[0].lower()}{password[1:]}1")
        passwords.append(f"{password[0].lower()}{password[1:]}12")
        passwords.append(f"{password[0].lower()}{password[1:]}123")
        passwords.append(f"{password[0].lower()}{password[1:]}1234")
        passwords.append(f"{password[0].lower()}{password[1:]}12345")
        passwords.append(f"{password[0].lower()}{password[1:]}!")
        passwords.append(f"{password[0].lower()}{password[1:]}?")
        passwords.append(f"{password[0].lower()}{password[1:]}@")
        passwords.append(f"{password}1")
        passwords.append(f"{password}12")
        passwords.append(f"{password}123")
        passwords.append(f"{password}1234")
        passwords.append(f"{password}12345")
        passwords.append(f"{password}00")
        passwords.append(f"{password}*")
        passwords.append(f"{password}$")
        passwords.append(f"{password}1!")
        passwords.append(f"{password}?")
        passwords.append(f"{password}!@")
        passwords.append(f"{password}!@#")
        passwords.append(f"{password}*$@")
        passwords.append(f"{password}*$@")
        for password in passwords:
            edited.append(":".join([email,password]))
    save("Combo_Editor",None,Checker.time,"\n".join(edited))