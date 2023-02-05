from requests import get
from time import sleep
from modules.functions import *
from modules.variables import *

def check_update():
    """Checks for updates"""
    change_title(f"Calani AIO | Checking For Updates | {discord_name}")
    print(f"    [{cyan}>{reset}] Checking for updates")
    
    try:
        latest_version = get("https://raw.githubusercontent.com/Mickey758/Calani-AIO/master/version").text.rstrip()
    except:
        print(f"    [{red}>{reset}] Could not connect to server")
        sleep(2)
        return
    
    if latest_version != version:
        print(f"    [{red}>{reset}] Your version is outdated!")
        print(f"    [{cyan}>{reset}] Find the latest version of Calani AIO here: https://github.com/Mickey758/Calani-AIO/releases")
        input(f"    [{cyan}>{reset}] Press enter to ignore")
        return
