from requests import get
from time import sleep
from modules.functions import *
from modules.variables import *
import tkinter.messagebox
import webbrowser

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
        if tkinter.messagebox.askyesno(title="Outdated Version", message=f"Current Version: v{version}\nLatest Version: v{latest_version}\n\nWould you like to be taken to the download page?"):
            webbrowser.open(f"https://github.com/Mickey758/Calani-AIO/releases/tag/v{latest_version}")
        return
