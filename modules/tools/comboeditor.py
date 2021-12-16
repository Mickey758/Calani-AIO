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
        edit(after_combos)
        print("\n\n")
        print(f"    [{cyan}Finished Editing Combo{reset}]")
        input(f"    [{cyan}Press Enter To Go Back{reset}]")
        return
def edit(combos):
    edited = []
    clear()
    ascii()
    print("\n\n")
    print(f"    [{cyan}Please Wait, Editing Combo{reset}]")
    for combo in combos:
        if ":" in combo:
            email = combo.split(":")[0]
            password = combo.split(":")[1]

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
                edited.append(email+":"+password)
    save("Combo_Editor",None,Checker.time,"\n".join(edited))