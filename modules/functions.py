from os import system,name
from datetime import datetime
from colorama import Fore,Style
from modules.variables import Checker,lock
from random import choice
from tkinter import Tk,filedialog
from base64 import b64decode
from zlib import decompress
from tempfile import mkstemp
from time import sleep
from console.utils import set_title
from os import makedirs
from win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, EnumWindows

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

def reset_stats():
    Checker.bad = 0
    Checker.cpm = 0
    Checker.good = 0
    Checker.custom = 0
    Checker.errors = 0
    Checker.proxies.clear()
    Checker.accounts.clear()
    Checker.accounts_down.clear()
    Checker.bad_proxies.clear()

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
    makedirs(f"Results/{time}",exist_ok=True)
    with lock:
        if type == "custom":
            with open(f"Results/{time}/{name}_custom.txt","a",errors="ignore") as file: file.write(content+"\n")
        elif type == "good":
            with open(f"Results/{time}/{name}_good.txt","a",errors="ignore") as file: file.write(content+"\n")
        else:
            with open(f"Results/{time}/{name}.txt","a",errors="ignore") as file: file.write(content+"\n")

def log(type:str,account:str,service:str=None):
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
            print(f"    [{yellow}Custom{reset}] {account} ~ {service}")
        elif type == "good":
            print(f"    [{green}Good{reset}] {account} ~ {service}")
        elif type == "bad":
            print(f"    [{red}Bad{reset}] {account} ~ {service}")
        else:
            print(f"    {cyan}{account}")

def set_proxy(proxy:str=False):
    """
    Returns a proxy to use in requests
    Set a proxy to get a dictionary response

    set_proxy(proxy="0.0.0.0")
    """
    if proxy:
        if ":" in proxy:
            spl = proxy.split(":")
            if len(spl) == 4:
                proxy = spl[2]+":"+spl[3]+"@"+spl[0]+":"+spl[1]

        if Checker.proxy_type == "http": return {"http":f"http://{proxy}","https":f"https://{proxy}"}
        elif Checker.proxy_type == "socks4": return {"http":f"socks4://{proxy}","https":f"socks4://{proxy}"}
        elif Checker.proxy_type == "socks5": return {"http":f"socks5://{proxy}","https":f"socks5://{proxy}"}

    else:
        while 1:
            if len(Checker.bad_proxies) == len(Checker.proxies):
                Checker.bad_proxies.clear()
            proxy = choice(Checker.proxies)
            if proxy not in Checker.bad_proxies:
                return proxy

def bad_proxy(proxy):
    if proxy not in Checker.bad_proxies:
        Checker.bad_proxies.append(proxy) # Adds the proxy to a list of bads so that it cant be used

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
    response = filedialog.askopenfilename(title=title,filetypes=((type, '.txt'),('All Files', '.*'),))
    root.destroy()
    return response if response not in ("",()) else False

def cui(modules:int):
    """Prints the cui"""

    while Checker.checking:
        clear()
        ascii()
        print("\n\n")
        percent = round(((Checker.good+Checker.bad+Checker.custom)/(len(Checker.accounts)*modules))*100,2) if Checker.good+Checker.bad+Checker.custom > 0 else 0.0
        print(f"""
    [{dark_cyan}Loaded Modules{reset}] {modules}

    [{green}Hits{reset}] {Checker.good}
    [{yellow}Custom{reset}] {Checker.custom}
    [{red}Bad{reset}] {Checker.bad}

    [{dark_yellow}Errors{bright}{reset}] {Checker.errors}
    [{dark_cyan}CPM{bright}{reset}] {Checker.cpm}
    [{cyan}{bright}Progress{dark_cyan}{reset}] {Checker.good+Checker.bad+Checker.custom}/{len(Checker.accounts)*modules} = {percent}%
    
    [{cyan}S{reset}] Save Remaining Lines""")
        sleep(1)

def cui_2():
    """Prints the proxy checker cui"""
    while Checker.checking:
        clear()
        ascii()
        print("\n\n")
        percent = round( ( (Checker.good+Checker.bad)/(len(Checker.accounts)) )*100,2) if Checker.good + Checker.bad > 0 else 0.0
        print(f"""
    [{dark_cyan}Proxy Type{reset}] {Checker.proxy_type.title()}

    [{green}Good{reset}] {Checker.good}
    [{red}Bad{reset}] {Checker.bad}

    [{dark_cyan}CPM{bright}{reset}] {Checker.cpm}
    [{cyan}{bright}Progress{dark_cyan}{reset}] {Checker.good+Checker.bad}/{len(Checker.accounts)} = {percent}%""")
        sleep(1)

def title(modules:int):
    """Sets the title while checking"""
    while Checker.checking:
        try:
            Checker.title = f"Calani AIO | Good: {Checker.good}  ~  Custom: {Checker.custom}  ~  Bad: {Checker.bad}  ~  Errors: {Checker.errors}  ~  CPM: {Checker.cpm}  ~  Progress: {Checker.good+Checker.bad+Checker.custom}/{len(Checker.accounts)*modules} = {round(((Checker.good+Checker.bad+Checker.custom)/(len(Checker.accounts)*modules))*100,2)}%"
            change_title(Checker.title)
        except:
            pass
def title_2():
    """Sets the title while checking for the proxy checker"""
    while Checker.checking:
        try:
            Checker.title = f"Calani AIO | Good: {Checker.good} ~ Bad: {Checker.bad} ~ CPM: {Checker.cpm} ~ Progress: {Checker.good+Checker.bad}/{len(Checker.accounts)} = { round( ( ( Checker.good+Checker.bad) / len(Checker.accounts ) ) * 100 , 2 ) } %"
            change_title(Checker.title)
            sleep(1)
        except:
            pass

def save_lines():
    """Save remaining lines"""
    if Checker.checking:
        if "Calani AIO | Good: " in GetWindowText(GetForegroundWindow()):
            if not Checker.saving:
                Checker.saving = True
                with open(f"Results/{Checker.time}/save_lines.txt","w") as file: file.write("\n".join(Checker.save_lines))
                Checker.saving = False

def level_cpm():
    """This levels the cpm every 15 seconds"""
    while Checker.checking:
        now = Checker.cpm
        sleep(15)
        Checker.cpm = (Checker.cpm - now)*4

def get_focus():
    """Get window focus"""
    toplist = []
    winlist = []
    def enum_callback(hwnd, results):
        winlist.append((hwnd, GetWindowText(hwnd)))
    EnumWindows(enum_callback, toplist)
    calani = [(hwnd, title) for hwnd, title in winlist if 'calani' in title.lower()][0][0]
    try: SetForegroundWindow(calani)
    except:pass
def change_title(text:str):
    """Change window title"""
    Checker.title = text
    set_title(Checker.title)