from modules.variables import Checker
from requests import Session
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy
from requests.adapters import HTTPAdapter, Retry
from time import sleep
import functools

def check(email:str,password:str):
    while 1:
        try:
            proxy = set_proxy()
            proxy_set = set_proxy(proxy)

            with Session() as s:
                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                r = s.get(f"https://spclient.wg.spotify.com/signup/public/v1/account?validate=1&email={email}").text
                if "That email is already registered to an account." in r:
                    if not Checker.cui: log("good",email,"SpotifyVM")
                    save("SpotifyVM","good",Checker.time,":".join([email,password]))
                    Checker.good += 1
                    return_proxy(proxy)
                    return
                elif "Enter your email to continue." in r or "status\":1" in r:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                else: raise
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        sleep(0.1)