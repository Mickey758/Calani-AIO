from threading import Lock
lock = Lock()
version = "0.2.6"
class Checker:
    bad = 0
    good = 0
    custom = 0
    cpm = 0
    errors = 0

    saving = False
    checking = False
    proxies = []
    bad_proxies = []
    accounts = []
    accounts_down = []
    save_lines = []
    time = ""

    cui = True
    share = False
    retries = 1
    timeout = 10
    threads = 200
    proxy_type = "socks4"