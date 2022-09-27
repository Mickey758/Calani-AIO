import re
import requests
from os import environ
import threading
import time
from anycaptcha import AnycaptchaClient, HCaptchaTaskProxyless, RecaptchaV2TaskProxyless, RecaptchaV3TaskProxyless, \
    ImageToTextTask ,RecaptchaV2Task ,HCaptchaTask , FunCaptchaProxylessTask,ZaloTask
import random

def demo_recaptchav2Proxyless():
    url = "https://abc"
    site_key = "6Lc9qjcUAAAAADTnJq5kJMjN9aD1lxpRLMnCS2TR"
    api_key = "YOURAPIKEY"
    client = AnycaptchaClient(api_key)
    is_invisible=True
    task = RecaptchaV2TaskProxyless(website_url=url, website_key=site_key,is_invisible=is_invisible)
    job = client.createTask(task)
    job.join()
    result=job.get_solution_response()
    if result.find("ERROR") != -1:
        print("fail ",result)
    else:
        print("success ",result)
        
def demo_zalocaptcha():
    api_key = "YOURAPIKEY"
    client = AnycaptchaClient(api_key)
    task = ZaloTask()
    job = client.createTask(task)
    job.join()
    result = job.get_solution_response()
    if result.find("ERROR") != -1:
        print("error ", result)
    else:
        print("success ", result)


def demo_recaptchav2():
    url = "https://www.google.com/recaptcha/api2/demo"
    site_key = "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-"
    api_key = "YOURAPIKEY"
    proxy_address="x.x.x.x"
    proxy_port=2312312
    proxy_type="http"
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67"
    proxy_login="123123"
    proxy_password = "12312322"
    is_invisible=None
    client = AnycaptchaClient(api_key)

    task = RecaptchaV2Task(website_url=url, website_key=site_key, proxy_address=proxy_address, proxy_port=proxy_port,
                           proxy_type=proxy_type,
                           user_agent=user_agent,
                           proxy_login=proxy_login, proxy_password=proxy_password,is_invisible=is_invisible)
    job = client.createTask(task)
    job.join()
    result = job.get_solution_response()
    if result.find("ERROR") != -1:
        print("fail ",result)
    else:
        print("success ",result)


def demo_hcaptchaProxyless():

    url = "https://www.calhospitalprepare.org"
    site_key = "ca915d64-b987-4026-be6c-93cdaa26ad50"
    api_key = "YOURAPIKEY"
    client = AnycaptchaClient(api_key)
    t1 = time.time()
    task = HCaptchaTaskProxyless(website_url=url, website_key=site_key)

    job = client.createTask(task)
    t1 = time.time()
    job.join()
    result = job.get_solution_response()
    if result.find("ERROR") != -1:
        print("fail ",result)
    else:
        print("success ",result)

def demo_hcaptcha():
    url = "https://www.calhospitalprepare.org"
    site_key = "ca915d64-b987-4026-be6c-93cdaa26ad50"
    api_key = "YOURAPIKEY"
    client = AnycaptchaClient(api_key)
    t1 = time.time()
    proxy_address = "abcddd"
    proxy_port = 1080
    proxy_type = "http"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67"
    proxy_login = "aasdas"
    proxy_password = "12312adcc"
    task = HCaptchaTask(website_url=url, website_key=site_key, proxy_address=proxy_address, proxy_port=proxy_port,
                           proxy_type=proxy_type,
                           user_agent=user_agent,
                           proxy_login=proxy_login, proxy_password=proxy_password)

    job = client.createTask(task)
    job.join()
    result = job.get_solution_response()
    if result.find("ERROR") != -1:
        print("error ", result)
    else:
        print("success ",result)





def demo_recaptchav3Proxyless():
    url = "https://2captcha.com/demo/recaptcha-v3"
    site_key = "6LfdxboZAAAAAMtnONIt4DJ8J1t4wMC-kVG02zIO"
    api_key = "YOURAPIKEY"
    client = AnycaptchaClient(api_key)
    task = RecaptchaV3TaskProxyless(website_url=url, website_key=site_key, min_score=0.3)
    job = client.createTask(task)
    job.join()
    result = job.get_solution_response()
    if result.find("ERROR") != -1:
        print("fail ",result)
    else:
        print("success ",result)


def demo_imagetotext():
    api_key = '66b990fefd7b4435bd44ec4460efcde0'
    captcha_fp = open('1.png', 'rb')
    client = AnycaptchaClient(api_key)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task,typecaptcha="text")
    job.join()
    result = job.get_solution_response()
    if result.find("ERROR") != -1:
        print("error ", result)
    else:
        print("success ", result)


def demo_funcaptcha():
    website_url = "https://iframe.arkoselabs.com/B7D8911C-5CC8-A9A3-35B0-554ACEE604DA/index.html?mkt=en&fbclid=IwAR39Ke2N1WbK5SYDlRVZZHLZroSvrkTOdgLx3xLWIAKi4raAgobNka0LIbA"
    site_key = "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA"
    api_key = "YOURAPIKEY"

    client = AnycaptchaClient(api_key)
    task = FunCaptchaProxylessTask(website_url, site_key)

    job = client.createTask(task,typecaptcha="funcaptcha")
    job.join()
    result = job.get_solution_response()
    if result.find("ERROR") != -1:
        print("error ", result)
    else:
        print("success ", result)


def demo_getblance():
    api_key = api_key = "YOURAPIKEY"
    client = AnycaptchaClient(api_key)
    print(client.getBalance())


if __name__=="__main__":
    demo_funcaptcha()
    demo_hcaptcha()
    demo_hcaptchaProxyless()
    demo_recaptchav2()
    demo_recaptchav2Proxyless()
    demo_recaptchav3Proxyless()
    demo_imagetotext()

