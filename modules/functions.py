from os import _exit
from datetime import datetime
from modules.variables import Checker,lock
from random import choice, choices, randint
from tkinter import Tk,filedialog
from base64 import b64decode
from zlib import decompress
from tempfile import mkstemp
from time import sleep
from console.utils import set_title
from os import makedirs
import win32gui,win32process,os
from numerize.numerize import numerize
from colored import fg
import ctypes

yellow = fg(3)
green = fg(2)
reset = fg(7)
cyan = fg(6)
red = fg(1)
dark_yellow = fg(166)
dark_cyan = fg(4)

ICON = decompress(b64decode('eJxjYGAEQgEBBiDJwZDBy''sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
_, ICON_PATH = mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

def get_guid():
    letters = list("abcdefghijklmnopqrstuvwxyz")
    numbers = list("1234567890")
    def char8():
        return "".join(choices(letters+numbers,k=8))
    def char4():
        return "".join(choices(letters+numbers,k=4))
    return f"{char8()}-{char4()}-{char4()}-{char4()}-{char8()}"
def get_string(characters:int):
    chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    return "".join(choices(chars,k=characters))
def get_number(min:int,max:int):
    return randint(min,max)

def reset_stats():
    Checker.bad = 0
    Checker.cpm = 0
    Checker.good = 0
    Checker.custom = 0
    Checker.errors = 0
    Checker.total_accounts = 0
    Checker.total_proxies = 0
    Checker.proxies.clear()
    Checker.accounts.clear()
    Checker.remaining.clear()
    Checker.bad_proxies.clear()
    Checker.cpm_averages = [0]

def message_box(title, text, style):
    """Creates a message box"""
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def clear():
    """Clears the console"""
    os.system('cls')

def ascii():
    """Prints the ascii logo"""
    print(cyan+"""
     ______   ________   __       ________   ___   __     ________      ________    ________  ______
    /_____/\ /_______/\ /_/\     /_______/\ /__/\ /__/\  /_______/\    /_______/\  /_______/\/_____/\\
    \:::__\/ \::: _  \ \\\\:\ \    \::: _  \ \\\\::\_\\\\  \ \ \__.::._\/    \::: _  \ \ \__.::._\/\:::_ \ \\
     \:\ \  __\::(_)  \ \\\\:\ \    \::(_)  \ \\\\:. `-\  \ \   \::\ \      \::(_)  \ \   \::\ \  \:\ \ \ \\
      \:\ \/_/\\\\:: __  \ \\\\:\ \____\:: __  \ \\\\:. _    \ \  _\::\ \__    \:: __  \ \  _\::\ \__\:\ \ \ \\
       \:\_\ \ \\\\:.\ \  \ \\\\:\/___/\\\\:.\ \  \ \\\\. \`-\  \ \/__\::\__/\    \:.\ \  \ \/__\::\__/\\\\:\_\ \ \\
        \_____\/ \__\/\__\/ \_____\/ \__\/\__\/ \__\/ \__\/\________\/     \__\/\__\/\________\/ \_____\/ """+reset)

def get_time():
    """
    Gets the time and date in the format:
    Year-Month-Day Hour-Minute-Second
    """
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

def save(name:str,saveType:str,time:str,content:str):
    """
    Saves the given account to a file
    save(
        name="NordVPN",
        type="good",
        time="2021-11-02 22-01-02",
        content="example@example.com:example123@"
    )
    """
    if not os.path.exists(f"Results/{time}"):
        makedirs(f"Results/{time}",exist_ok=True)
    with Checker.save_lock:
        match saveType:
            case "custom":
                with open(f"Results/{time}/{name}_custom.txt","a",errors="ignore") as file: file.write(content+"\n")
            case "good":
                with open(f"Results/{time}/{name}_good.txt","a",errors="ignore") as file: file.write(content+"\n")
            case _:
                with open(f"Results/{time}/{name}.txt","a",errors="ignore") as file: file.write(content+"\n")

def log(logType:str,account:str,service:str=None):
    """
    Prints to the console
    log(
        type="good",
        account="example@gmail.com:example123@,
        service="NordVPN"
    )
    """
    with Checker.print_lock:
        match logType:
            case "custom":
                print(f"    [{yellow}Custom{reset}] {account} ~ {service}")
            case "good":
                print(f"    [{green}Good{reset}] {account} ~ {service}")
            case "bad":
                print(f"    [{red}Bad{reset}] {account} ~ {service}")
            case _:
                print(f"    {cyan}{account}")

def set_proxy(proxy:str=False):
    """
    Returns a proxy to use in requests
    Set a proxy to get a dictionary response

    set_proxy(proxy="127.0.0.1:5000")
    """
    if Checker.proxy_type == 'none': return {}

    if proxy:
        if proxy.count(':') == 3:
            host,port,username,password = proxy.split(':')
            proxy = f'{username}:{password}@{host}:{port}'

        match Checker.proxy_type:
            case "http": return {"http":f"http://{proxy}","https":f"http://{proxy}"}
            case "socks4": return {"http":f"socks4://{proxy}","https":f"socks4://{proxy}"}
            case "socks5": return {"http":f"socks5://{proxy}","https":f"socks5://{proxy}"}

    while 1:
        with Checker.proxy_lock:
            proxies = [proxy for proxy in Checker.proxies if proxy not in Checker.bad_proxies and proxy not in Checker.locked_proxies]
            if not proxies:
                Checker.bad_proxies.clear()
                continue
            proxy = choice(proxies)
            lock_proxy(proxy)
        return proxy
def return_proxy(proxy):
    """
    Remove a proxy from the locked proxies pool
    """
    if not proxy: return
    with Checker.proxy_lock:
        if proxy in Checker.locked_proxies: Checker.locked_proxies.remove(proxy)
def lock_proxy(proxy):
    """
    Temporarily remove a proxy from the pool to lock to one thread
    """
    if not proxy: return
    if Checker.lockProxies and proxy not in Checker.locked_proxies: Checker.locked_proxies.append(proxy)
def bad_proxy(proxy):
    """
    Temporarily remove a proxy from the pool for being bad
    """
    if not proxy: return
    if proxy not in Checker.bad_proxies: Checker.bad_proxies.append(proxy)

def get_file(title:str,type:str):
    """
    Gets a filepath
    Returns False if nothing was given
    get_file(title="Combo File",type="Combo File")
    """
    root = Tk()
    root.withdraw()
    root.lift()
    root.iconbitmap(default=ICON_PATH)
    response = filedialog.askopenfilename(title=title,filetypes=((type, '.txt'),('All Files', '.*'),))
    root.destroy()
    return response if response not in ("",()) else False

def cui(modules:int):
    """Prints the cui"""

    while Checker.checking:
        with lock:
            clear()
            ascii()
            print(f"""
            
                                            {cyan}{modules}{reset} Loaded Module{'s' if modules > 1 else ''}

    {'Hits'.center(11,' ')}{fg(8)}-{reset}  {fg(2)}{numerize(Checker.good)}{reset}
    {'Custom'.center(11,' ')}{fg(8)}-{reset}  {fg(3)}{numerize(Checker.custom)}{reset}
    {'Bad'.center(11,' ')}{fg(8)}-{reset}  {fg(1)}{numerize(Checker.bad)}{reset}

    {'Remaining'.center(11,' ')}{fg(8)}-{reset}  {fg(25)}{numerize(len(Checker.remaining)*modules)}{reset}
    {'Errors'.center(11,' ')}{fg(8)}-{reset}  {fg(124)}{numerize(Checker.errors)}{reset}
    {'CPM'.center(11,' ')}{fg(8)}-{reset}  {fg(104)}{numerize(get_cpm())}{reset}
    
            """)
        sleep(5)

def cui_2():
    """Prints the proxy checker cui"""
    while Checker.checking:
        with lock:
            clear()
            ascii()
            print(f"""  


    {'Hits'.center(11,' ')}{fg(8)}-{reset}  {fg(2)}{numerize(Checker.good)}{reset}
    {'Bad'.center(11,' ')}{fg(8)}-{reset}  {fg(1)}{numerize(Checker.bad)}{reset}

    {'Remaining'.center(11,' ')}{fg(8)}-{reset}  {fg(25)}{numerize(len(Checker.remaining))}{reset}
    {'CPM'.center(11,' ')}{fg(8)}-{reset}  {fg(104)}{numerize(get_cpm())}{reset}
    
            """)
        sleep(5)

def title(modules:int):
    """
    Sets the title while checking
    """
    while Checker.checking:
        Checker.title = f"Calani AIO | Good: {numerize(Checker.good)}  ~  Custom: {numerize(Checker.custom)}  ~  Bad: {numerize(Checker.bad)}  ~  Errors: {numerize(Checker.errors)}  ~  CPM: {numerize(get_cpm())}  ~  Remaining: {numerize(len(Checker.remaining)*modules)}"
        change_title(Checker.title)
        sleep(0.1)
def title_2():
    """
    Sets the title while checking for the proxy checker
    """
    while Checker.checking:
        Checker.title = f"Calani AIO | Good: {numerize(Checker.good)} ~ Bad: {numerize(Checker.bad)} ~ CPM: {numerize(get_cpm())} ~ Remaining: {numerize(len(Checker.remaining))}"
        change_title(Checker.title)
        sleep(0.1)

def save_lines(_=None):
    """
    Save remaining lines
    """
    if Checker.checking:
        with lock:
            clear()
            ascii()
            print('\n\n')
            print(f"    [{cyan}Saving Remaining Lines{reset}]")
            with open(f"Results/{Checker.time}/remaining_lines.txt","w") as file: file.write("\n".join(Checker.remaining))
            sleep(2)
            if _ == 2: _exit(1)

def is_focused():
    """
    Check if the application is in focus
    Returns True/False

    is_focused()
    """
    focus_window_pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]
    current_process_pid = os.getppid()

    return focus_window_pid == current_process_pid

def get_cpm():
    return round(int(sum(Checker.cpm_averages)/30) / 5) * 5

def level_cpm():
    """This levels the cpm every second"""

    while Checker.checking:
        now = Checker.cpm
        sleep(1)
        Checker.cpm -= now
        Checker.cpm_averages.append(Checker.cpm)
        Checker.cpm_averages = Checker.cpm_averages[-60:]

def change_title(text:str):
    """Change window title"""
    Checker.title = text
    set_title(Checker.title)

def get_random_ua():
    from random_user_agent.user_agent import UserAgent
    from random_user_agent.params import SoftwareName, OperatingSystem
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    return user_agent_rotator.get_random_user_agent()

def get_solver_balance():
    from twocaptcha import TwoCaptcha
    from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
    from anycaptcha import AnycaptchaClient
    from console.utils import clear_lines
    invalid_key = f'{red}Api Key Invalid{reset}'
    match Checker.solver_serice:
        case '2captcha': 
            try: balance = TwoCaptcha(Checker.api_key).balance()
            except: return invalid_key
            else: return f'{green}${round(float(balance),2)}{reset}'
        case 'anticaptcha':
            solver = recaptchaV2Proxyless()
            solver.set_verbose(1)
            solver.set_key(Checker.api_key)
            try:
                balance = solver.get_balance()
                clear_lines(1)
            except: 
                clear_lines(1)
                return invalid_key
            else: return f'{green}${round(balance,2)}{reset}'
        case 'anycaptcha':
            client = AnycaptchaClient(Checker.api_key)
            try: balance = client.getBalance()
            except: return invalid_key
            else: return f'{green}${round(balance,2)}{reset}'
            
def get_captcha(site_key,site_url,captcha_type):
    from twocaptcha import TwoCaptcha
    from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless
    from anycaptcha import AnycaptchaClient, HCaptchaTaskProxyless
    match Checker.solver_serice:
        case '2captcha':
            solver = TwoCaptcha(Checker.api_key)
            match captcha_type:
                case 'hcaptcha': 
                    result = solver.hcaptcha(site_key,site_url)['code']
                    if not result: raise
                    return result
        case 'anticaptcha':
            match captcha_type:
                case 'hcaptcha':
                    solver = hCaptchaProxyless()
                    solver.set_verbose(1)
                    solver.set_key(Checker.api_key)
                    solver.set_website_url(site_url)
                    solver.set_website_key(site_key)
                    
                    result = solver.solve_and_return_solution()
                    if not result:
                        solver.report_incorrect_hcaptcha()
                        raise
                    return result
        case 'anycaptcha':
            match captcha_type:
                case 'hcaptcha':
                    client = AnycaptchaClient(Checker.api_key)
                    task = HCaptchaTaskProxyless(site_url,site_key)
                    job = client.createTask(task)
                    job.join(maximum_time=120)
                    result = job.get_solution_response()
                    
                    if result.find("ERROR") != -1: raise
                    return result
