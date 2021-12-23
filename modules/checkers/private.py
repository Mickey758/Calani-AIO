from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import get,post
from base64 import b64encode

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        auth = b64encode(f"{email}:{password}".encode()).decode()
        try:
            pass
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return