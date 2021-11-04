from os import system,name
from datetime import datetime
from colorama import Fore,Style,init
from threading import Lock,Thread
from __main__ import checker
from random import choice
from tkinter import Tk,filedialog
from base64 import b64decode
from zlib import decompress
from tempfile import mkstemp
from time import sleep
from console.utils import set_title
from os import makedirs

lock = Lock()
init(autoreset=True)

yellow = Fore.YELLOW
green = Fore.GREEN
reset = Fore.RESET
cyan = Fore.CYAN
red = Fore.RED
dark_yellow = Fore.YELLOW+Style.DIM
dark_cyan = Fore.CYAN+Style.DIM
bright = Style.BRIGHT

ICON = decompress(b64decode('eJxjYGAEQgEBBiDJwZDBy''sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
_, ICON_PATH = mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

def clear():
    """Clears the console"""
    system('cls' if name=='nt' else 'clear')

def ascii():
    """Prints the ascii logo"""
    print(cyan+r"            ______   ________   __       ________   ___   __     ________      ________    ________  ______      ")
    print(cyan+r"           /_____/\ /_______/\ /_/\     /_______/\ /__/\ /__/\  /_______/\    /_______/\  /_______/\/_____/\     ")
    print(cyan+r"           \:::__\/ \::: _  \ \\:\ \    \::: _  \ \\::\_\\  \ \ \__.::._\/    \::: _  \ \ \__.::._\/\:::_ \ \    ")
    print(cyan+r"            \:\ \  __\::(_)  \ \\:\ \    \::(_)  \ \\:. `-\  \ \   \::\ \      \::(_)  \ \   \::\ \  \:\ \ \ \   ")
    print(cyan+r"             \:\ \/_/\\:: __  \ \\:\ \____\:: __  \ \\:. _    \ \  _\::\ \__    \:: __  \ \  _\::\ \__\:\ \ \ \  ")
    print(cyan+r"              \:\_\ \ \\:.\ \  \ \\:\/___/\\:.\ \  \ \\. \`-\  \ \/__\::\__/\    \:.\ \  \ \/__\::\__/\\:\_\ \ \ ")
    print(cyan+r"               \_____\/ \__\/\__\/ \_____\/ \__\/\__\/ \__\/ \__\/\________\/     \__\/\__\/\________\/ \_____\/ ")

def get_time():
    """
    Gets the time and date in the format:
    Year-Month-Day Hour-Minute-Second
    """
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

def save(name:str,type:str,time:str,content:str):
    """
    Saves the given account to a file
    save(
        name="NordVPN",
        type="good", 
        time="2021-11-02 22-01-02",
        content="example@example.com:example123@"
    )
    """
    makedirs(f"Results/{checker.time}",exist_ok=True)
    with lock:
        if type == "custom":
            with open(f"Results/{time}/{name}_custom.txt","a",errors="ignore") as file: file.write(content+"\n")
        elif type == "good":
            with open(f"Results/{time}/{name}_good.txt","a",errors="ignore") as file: file.write(content+"\n")

def log(type:str,account:str,service:str):
    """
    Prints to the console
    log(
        type="good",
        account="example@gmail.com:example123@,
        service="NordVPN"
    )
    """
    with lock:
        if type == "custom":
            print(f"    [{yellow}Custom{reset}] {account} | {service}")
        if type == "good":
            print(f"    [{green}Good{reset}] {account} | {service}")

def set_proxy(proxy:str=False):
    """
    Returns a proxy to use in requests
    Set a proxy to get a dictionary response

    set_proxy(proxy="0.0.0.0")
    """
    if proxy:
        try:
            spl = proxy.split(":")
            proxy = spl[2]+":"+spl[3]+"@"+spl[0]+":"+spl[1]
        except: pass
        
        if checker.proxy_type == "http":
            return {"http":f"http://{proxy}","https":f"http://{proxy}"}
        elif checker.proxy_type == "socks4":
            return {"http":f"socks4://{proxy}","https":f"socks4://{proxy}"}
        elif checker.proxy_type == "socks5":
            return {"htt":f"socks5://{proxy}","https":f"socks5://{proxy}"}
    else:
        return choice(checker.proxies)

def get_file(title:str,type:str):
    """
    Gets a filepath
    Returns False if nothing was given
    get_file(title="Combo File",type="Combo File")
    """
    root = Tk()
    root.withdraw()
    try: root.iconbitmap(default=ICON_PATH)
    except: pass
    root.withdraw
    response = filedialog.askopenfilename(title=title,filetypes=((type, '.txt'),))
    return response if response not in ("",()) else False

def cui(modules:int):
    """Prints the cui"""

    while checker.checking:
        clear()
        ascii()
        print("\n\n")
        print(f"""
    [{dark_cyan}Loaded Modules{reset}] {modules}

    [{green}Hits{reset}] {checker.good}
    [{yellow}Custom{reset}] {checker.custom}
    [{red}Bad{reset}] {checker.bad}
    
    [{dark_yellow}Errors{bright}{reset}] {checker.errors}
    [{dark_cyan}CPM{bright}{reset}] {checker.cpm}
    [{cyan}{bright}Progress{dark_cyan}{reset}] {checker.good+checker.bad+checker.custom}/{len(checker.accounts)*modules}

        """)
        sleep(1)

def title(modules:int):
    """Sets the title while checking"""
    while checker.checking:
        try:
            checker.title = f"Calani AIO | Good: {checker.good}  ~  Custom: {checker.custom}  ~  Bad: {checker.bad}  ~  Errors: {checker.errors}  ~  CPM: {checker.cpm}  |  Progress: {round(((checker.good+checker.bad+checker.custom)/(len(checker.accounts)*modules))*100,2)}%"
            set_title(checker.title)
            sleep(0.1)
        except:
            pass

def level_cpm():
    """This levels the cpm every 60 seconds"""
    while checker.checking:
        now = checker.cpm
        sleep(60)
        checker.cpm -= now