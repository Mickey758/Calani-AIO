from requests import get
from time import sleep
from modules.functions import *
from modules.variables import *

def check():
    """Checks for updates"""
    change_title("Calani AIO | Checking For Updates | MickeyYe#0003")
    print(f"    [{cyan}>{reset}] Checking for updates")
    try:
        ver = get("https://raw.githubusercontent.com/Mickey758/Calani-AIO/master/version").text.rstrip()
        return True if ver != version else False
    except:
        print(f"    [{red}>{reset}] Could not connect to update server")
        sleep(2)
        return False
