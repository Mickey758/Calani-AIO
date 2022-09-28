from modules.variables import Checker,discord
from modules.functions import *
from time import sleep
from requests import get
from string import digits
from multiprocessing.dummy import Pool

default = """https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all
https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all
http://olaf4snow.com/public/proxy.txt
http://atomintersoft.com/products/alive-proxy/proxy-list/3128
http://atomintersoft.com/products/alive-proxy/proxy-list?ap=9
http://bestproxy.narod.ru/proxy1.html
http://bestproxy.narod.ru/proxy2.html
https://spys.one/
http://greenrain.bos.ru/R_Stuff/Proxy.htm
http://johnstudio0.tripod.com/index1.htm
http://rammstein.narod.ru/proxy.html
http://sergei-m.narod.ru/proxy.htm
http://tomoney.narod.ru/help/proxi.htm
http://westdollar.narod.ru/proxy.htm
http://atomintersoft.com/products/alive-proxy/proxy-list/high-anonymity/
http://atomintersoft.com/products/alive-proxy/socks5-list
http://atomintersoft.com/anonymous_proxy_list
http://atomintersoft.com/high_anonymity_elite_proxy_list
http://atomintersoft.com/products/alive-proxy/proxy-list
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
http://proxy-list.org/english/index.php
http://proxydb.net/
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt
http://globalproxies.blogspot.com/
http://www.cybersyndrome.net/plz.html
http://www.cybersyndrome.net/plr5.html
http://biskutliat.blogspot.com/
http://freeproxylist-daily.blogspot.com/2013/05/usa-proxy-list-2013-05-15-0111-am-gmt8.html
http://freeproxylist-daily.blogspot.com/2013/05/usa-proxy-list-2013-05-13-812-gmt7.html
http://www.cybersyndrome.net/pla5.html
http://vipprox.blogspot.com/2013_06_01_archive.html
http://vipprox.blogspot.com/2013/05/us-proxy-servers-74_24.html
http://vipprox.blogspot.com/p/blog-page_7.html
http://vipprox.blogspot.com/2013/05/us-proxy-servers-199_20.html
http://vipprox.blogspot.com/2013_02_01_archive.html
http://alexa.lr2b.com/proxylist.txt
http://vipprox.blogspot.com/2013_03_01_archive.html
http://browse.feedreader.com/c/Proxy_Server_List-1/449196260
http://browse.feedreader.com/c/Proxy_Server_List-1/449196258
http://sock5us.blogspot.com/2013/06/01-07-13-free-proxy-server-list.html#comment-form
http://browse.feedreader.com/c/Proxy_Server_List-1/449196251
http://free-ssh.blogspot.com/feeds/posts/default
http://browse.feedreader.com/c/Proxy_Server_List-1/449196259
http://sockproxy.blogspot.com/2013/04/11-04-13-socks-45.html
http://proxyfirenet.blogspot.com/
https://www.javatpoint.com/proxy-server-list
https://openproxy.space/list/http
https://openproxy.space/list/socks4
https://openproxy.space/list/socks5
http://inav.chat.ru/ftp/proxy.txt
http://hack-hack.chat.ru/proxy/allproxy.txt
https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies.txt
https://free-proxy-list.com/
https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt
https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all
https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all""".splitlines()

def start():
    change_title(f"Calani AIO | Proxy Scraper | {discord}")
    reset_stats()
    while 1:
        clear()
        ascii()
        print("\n\n")
        print(f"""
    [{cyan}1{reset}] Pick Links
    [{cyan}2{reset}] Use Default Links

    [{cyan}X{reset}] Back""")
        option = input(f"    [{cyan}>{reset}] ").lower()
        match option:
            case "1":
                clear()
                ascii()
                print("\n\n")
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
                sleep(1)
                scrape(after_links)
            case "2": scrape()
            case "x": return

def scrape(links:str=None):
    Checker.time = get_time()
    proxies = []
    if not links: links = default
    def foo(link):
        count = 0
        try: a = get(link,timeout=Checker.timeout,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}).text.splitlines()
        except: log(None,f"Connection Error ~ {link}")
        else:
            for line in a:
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
                                proxies.append(ip+":"+port)

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
                                        proxies.append(ip+":"+port)
                except:
                    pass
            log(None,f"{count} Proxies ~ {link}")
    clear()
    ascii()
    print("\n\n")
    mainpool = Pool(Checker.threads)
    mainpool.imap_unordered(func=foo,iterable=list(set(links)))
    mainpool.close()
    mainpool.join()
    print("\n\n")
    proxies = list(set(proxies))
    print(f"    [{cyan}>{reset}] Saving {green}{len(proxies)}{reset} Proxies")
    makedirs(f"Results/{Checker.time}",exist_ok=True)
    with open(f"Results/{Checker.time}/Scraped_Proxies.txt","w",errors="ignore") as file: file.write("\n".join(proxies))
    print("\n\n")
    print(f"    [{cyan}>{reset}] Finished Scraping")
    input(f"    [{cyan}>{reset}] Press Enter To Go Back")