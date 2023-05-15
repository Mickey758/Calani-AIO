from modules.variables import Checker,discord_name
from modules.functions import *
from time import sleep
from requests import get
from string import digits
from multiprocessing.dummy import Pool
import os

default = """https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all
https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all
http://olaf4snow.com/public/proxy.txt
http://atomintersoft.com/products/alive-proxy/proxy-list/3128
http://rammstein.narod.ru/proxy.html
http://sergei-m.narod.ru/proxy.htm
http://tomoney.narod.ru/help/proxi.htm
http://westdollar.narod.ru/proxy.htm
http://atomintersoft.com/products/alive-proxy/proxy-list/high-anonymity/
http://atomintersoft.com/products/alive-proxy/socks5-list
http://atomintersoft.com/anonymous_proxy_list
http://atomintersoft.com/products/alive-proxy/proxy-list/com
http://atomintersoft.com/proxy_list_domain_com
http://atomintersoft.com/proxy_list_domain_edu
http://atomintersoft.com/proxy_list_domain_net
http://atomintersoft.com/proxy_list_domain_org
http://atomintersoft.com/proxy_list_port_3128
http://atomintersoft.com/proxy_list_port_80
http://atomintersoft.com/proxy_list_port_8000
http://atomintersoft.com/proxy_list_port_81
http://atomintersoft.com/transparent_proxy_list
https://free-proxy-list.net/
https://www.us-proxy.org/
https://free-proxy-list.net/uk-proxy.html
https://www.sslproxies.org/
https://free-proxy-list.net/anonymous-proxy.html
https://www.socks-proxy.net/
http://proxydb.net/
https://raw.githubusercontent.com/thespeedx/proxy-list/master/socks5.txt
https://raw.githubusercontent.com/thespeedx/proxy-list/master/socks4.txt
https://raw.githubusercontent.com/thespeedx/proxy-list/master/http.txt
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt
https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt
https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks4.txt
https://raw.githubusercontent.com/shiftytr/proxy-list/master/socks5.txt
http://globalproxies.blogspot.com/
http://biskutliat.blogspot.com/
http://freeproxylist-daily.blogspot.com/2013/05/usa-proxy-list-2013-05-15-0111-am-gmt8.html
http://freeproxylist-daily.blogspot.com/2013/05/usa-proxy-list-2013-05-13-812-gmt7.html
http://vipprox.blogspot.com/2013_06_01_archive.html
http://vipprox.blogspot.com/2013/05/us-proxy-servers-74_24.html
http://vipprox.blogspot.com/p/blog-page_7.html
http://vipprox.blogspot.com/2013/05/us-proxy-servers-199_20.html
http://vipprox.blogspot.com/2013_02_01_archive.html
http://alexa.lr2b.com/proxylist.txt
http://vipprox.blogspot.com/2013_03_01_archive.html
http://free-ssh.blogspot.com/feeds/posts/default
http://sockproxy.blogspot.com/2013/04/11-04-13-socks-45.html
http://proxyfirenet.blogspot.com/
https://www.javatpoint.com/proxy-server-list
https://openproxy.space/list/http
https://openproxy.space/list/socks4
https://openproxy.space/list/socks5
https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt
https://free-proxy-list.com/
https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt
https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all
https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all
http://spys.me/proxy.txt
https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt
https://www.us-proxy.org
https://free-proxy-list.net
https://raw.githubusercontent.com/thespeedx/socks-list/master/socks5.txt
https://raw.githubusercontent.com/thespeedx/socks-list/master/socks4.txt
https://raw.githubusercontent.com/thespeedx/socks-list/master/http.txt
https://proxy50-50.blogspot.com/
https://www.my-proxy.com/free-anonymous-proxy.html
https://www.my-proxy.com/free-socks-4-proxy.html
https://www.my-proxy.com/free-socks-5-proxy.html
https://www.my-proxy.com/free-proxy-list.html
https://www.my-proxy.com/free-proxy-list-2.html
https://www.my-proxy.com/free-proxy-list-3.html
https://www.my-proxy.com/free-proxy-list-4.html
https://www.my-proxy.com/free-proxy-list-5.html
https://www.my-proxy.com/free-proxy-list-6.html
https://www.my-proxy.com/free-proxy-list-7.html
https://www.my-proxy.com/free-proxy-list-8.html
https://www.my-proxy.com/free-proxy-list-9.html
https://www.my-proxy.com/free-proxy-list-10.html
https://www.my-proxy.com/free-elite-proxy.html
https://www.proxyscan.io/download?type=http
https://www.proxyscan.io/download?type=https
https://www.proxyscan.io/download?type=socks4
https://www.proxyscan.io/download?type=socks5
https://multiproxy.org/txt_all/proxy.txt
http://rootjazz.com/proxies/proxies.txt
http://ab57.ru/downloads/proxyold.txt
https://proxy-spider.com/api/proxies.example.txt
https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt
https://www.proxy-list.download/api/v1/get?type=socks4
https://raw.githubusercontent.com/saisuiu/lionkings-http-proxys-proxies/main/cnfree.txt
https://raw.githubusercontent.com/saisuiu/lionkings-http-proxys-proxies/main/free.txt
https://raw.githubusercontent.com/zuoxiaolei/proxys/main/proxys/proxys.txt
https://raw.githubusercontent.com/hyperbeats/proxy-list/main/socks4.txt
https://raw.githubusercontent.com/hyperbeats/proxy-list/main/socks5.txt
https://raw.githubusercontent.com/hyperbeats/proxy-list/main/http.txt
https://raw.githubusercontent.com/hyperbeats/proxy-list/main/https.txt
https://raw.githubusercontent.com/prxchk/proxy-list/main/all.txt
https://raw.githubusercontent.com/almroot/proxylist/master/list.txt
https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http_old.txt
https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt
https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/hproxy.txt
https://raw.githubusercontent.com/roma8ok/proxy-list/main/proxy-list-socks5.txt
https://raw.githubusercontent.com/roma8ok/proxy-list/main/proxy-list-http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt
https://raw.githubusercontent.com/saschazesiger/free-proxies/master/proxies/socks4.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks4.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation/socks5.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/http.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/socks4.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_geolocation_anonymous/socks5.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_geolocation/socks4.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_geolocation/socks5.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_geolocation/http.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_anonymous/socks4.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_anonymous/socks5.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_anonymous/http.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_geolocation_anonymous/http.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_geolocation_anonymous/socks4.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies_geolocation_anonymous/socks5.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies/socks4.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies/socks5.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/master/proxies/http.txt
https://raw.githubusercontent.com/tahaluindo/free-proxies/main/proxies/all.txt
https://raw.githubusercontent.com/bardiafa/proxy-leecher/main/proxies.txt
https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt
https://raw.githubusercontent.com/saschazesiger/free-proxies/master/proxies/socks5.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt
https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt
https://raw.githubusercontent.com/zevtyardt/proxy-list/main/all.txt
https://raw.githubusercontent.com/ercindedeoglu/proxies/main/proxies/https.txt
https://raw.githubusercontent.com/ercindedeoglu/proxies/main/proxies/http.txt
https://raw.githubusercontent.com/ercindedeoglu/proxies/main/proxies/socks4.txt
https://raw.githubusercontent.com/ercindedeoglu/proxies/main/proxies/socks5.txt
https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt
https://raw.githubusercontent.com/saschazesiger/free-proxies/master/proxies/raw.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/socks5.txt
https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt
https://raw.githubusercontent.com/uptimerbot/proxy-list/main/proxies/socks4.txt""".splitlines()

def start():
    change_title(f"Calani AIO | Proxy Scraper | {discord_name}")
    reset_stats()
    while 1:
        clear()
        ascii()
        print(f"""
    [{cyan}1{reset}] Pick Links
    [{cyan}2{reset}] Use Default Links

    [{cyan}X{reset}] Back""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        match option:
            case "1":
                clear()
                ascii()
                print(f"    [{cyan}>{reset}] Pick Link File")
                file_path = get_file("Proxy Site Links File","Proxy Site Links File")
                if not file_path:
                    print(f"    [{cyan}>{reset}] No File Detected")
                    sleep(1)
                    return
                with open(file_path,errors="ignore") as file:
                    original_links = file.read().splitlines()
                    after_links = list(set(original_links))
                    duplicates = len(original_links)-len(after_links)
                if not len(original_links):
                    print(f"    [{red}>{reset}] No Links Detected")
                    sleep(1)
                    return
                print(f"    [{cyan}>{reset}] Imported {green}{len(original_links)}{reset} Links")
                if duplicates != 0:
                    print(f"    [{cyan}>{reset}] Removed {green}{duplicates}{reset} Duplicates")
                sleep(0.5)
                scrape(after_links)
            case "2": scrape()
            case "x": return

def scrape(links:list=None):
    Checker.time = get_time()
    proxies = []
    if not links: links = default
    def get_proxies(link):
        count = 0
        try: request = get(link,timeout=Checker.timeout,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}).text.splitlines()
        except: log(None,f"Connection Error ~ {link}")
        else:
            for line in request:
                try:
                    if ":" in line:
                        if line.count(':') == 1:
                            proxy = line.split(":")
                            ip = proxy[0]
                            port = proxy[1]
                            for char in port:
                                if char not in list(set(digits)):
                                    port = port.split(char)[0]
                            for char in ip:
                                if char not in list(set(digits+".")):
                                    ip = ip.split(char)[-1]
                            if ip and port and ip.count('.') == 3:
                                count += 1
                                proxies.append(':'.join([ip,port]))

                        elif line.count(':') > 1:
                            for _ in range(line.count(':')+1):
                                proxy = line.split(":")
                                ip = proxy[_]
                                port = proxy[_+1]
                                if "." in ip:
                                    for char in port:
                                        if char not in list(set(digits)):
                                            port = port.split(char)[0]
                                    for char in ip:
                                        if char not in list(set(digits+".")):
                                            ip = ip.split(char)[-1]
                                    if ip and port and ip.count('.') == 3:
                                        count += 1
                                        proxies.append(':'.join([ip,port]))
                except:
                    pass
            log(None,f"{count} Proxies ~ {link}")
    clear()
    ascii()
    mainpool = Pool(Checker.threads)
    mainpool.imap_unordered(func=get_proxies,iterable=list(set(links)))
    mainpool.close()
    mainpool.join()
    
    proxies = list(set(proxies))
    print(f"\n\n    [{cyan}>{reset}] Saving {green}{len(proxies)}{reset} Proxies")
    makedirs(f"Results/{Checker.time}",exist_ok=True)
    with open(f"Results/{Checker.time}/Scraped_Proxies.txt","w",errors="ignore") as file: file.write("\n".join(proxies))
    save_path = os.path.join(os.getcwd(),f'Results\\{Checker.time}')
    print(f"\n\n    [{cyan}>{reset}] Finished Scraping")
    print(f"    [{cyan}>{reset}] Saved to \"{save_path}\\Scraped_Proxies.txt\"")
    input(f"    [{cyan}>{reset}] Press Enter To Go Back")
