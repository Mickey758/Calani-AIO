from threading import Lock

version = "1.0.6"
discord_name = "MickeyYe#9423"
discord_server = "https://discord.gg/PEhWnFcuhq"
class Checker:
    bad = 0
    good = 0
    custom = 0
    cpm = 0
    cpm_averages = [0]
    errors = 0

    checking = False
    stopping = False

    proxies = []
    locked_proxies = []
    bad_proxies = []
    accounts = []
    remaining = []
    total_proxies = 0
    total_accounts = 0
    time = ""

    solver_serice = '2captcha'
    api_key = ''

    discord_webhook = ''

    lockProxies = False
    cui = True
    retries = 1
    timeout = 10
    threads = 200
    proxy_type = "socks4"

    pool = None
    
    proxy_lock = Lock()
    save_lock = Lock()
    print_lock = Lock()

    def lock_all():
        Checker.proxy_lock.acquire()
        Checker.save_lock.acquire()
        Checker.print_lock.acquire()
    
    def unlock_all():
        Checker.proxy_lock.release()
        Checker.save_lock.release()
        Checker.print_lock.release()

