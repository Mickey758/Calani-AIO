from modules.variables import Checker
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
http://hack-hack.chat.ru/proxy/allproxy.txt
http://hack-hack.chat.ru/proxy/anon.txt
http://hack-hack.chat.ru/proxy/p1.txt
http://hack-hack.chat.ru/proxy/p2.txt
http://hack-hack.chat.ru/proxy/p3.txt
http://hack-hack.chat.ru/proxy/p4.txt
http://inav.chat.ru/ftp/proxy.txt
http://johnstudio0.tripod.com/index1.htm
http://rammstein.narod.ru/proxy.html
http://sergei-m.narod.ru/proxy.htm
http://tomoney.narod.ru/help/proxi.htm
http://westdollar.narod.ru/proxy.htm
http://atomintersoft.com/products/alive-proxy/proxy-list/high-anonymity/
http://atomintersoft.com/products/alive-proxy/socks5-list
http://proxy-ip-list.com/
http://proxy-ip-list.com
http://proxy-ip-list.com/download/free-usa-proxy-ip.txt
http://atomintersoft.com/anonymous_proxy_list
http://atomintersoft.com/high_anonymity_elite_proxy_list
http://atomintersoft.com/products/alive-proxy/proxy-list
http://atomintersoft.com/products/alive-proxy/proxy-list?ap=9
http://atomintersoft.com/products/alive-proxy/proxy-list/3128
http://atomintersoft.com/products/alive-proxy/proxy-list/com
http://atomintersoft.com/products/alive-proxy/proxy-list/high-anonymity/
http://atomintersoft.com/products/alive-proxy/socks5-list
http://atomintersoft.com/proxy_list_domain_com
http://atomintersoft.com/proxy_list_domain_edu
http://atomintersoft.com/proxy_list_domain_net
http://atomintersoft.com/proxy_list_domain_org
http://atomintersoft.com/proxy_list_port_3128
http://atomintersoft.com/proxy_list_port_80
http://atomintersoft.com/proxy_list_port_8000
http://atomintersoft.com/proxy_list_port_81
http://atomintersoft.com/transparent_proxy_list
http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any
http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any&p=2
http://best-proxy.com/english/search.php?search=anonymous-and-elite&country=any&type=anonymous-and-elite&port=any&ssl=any&p=3
http://bestproxy.narod.ru/proxy2.html
http://nntime.com/proxy-list-01.htm
http://nntime.com/proxy-list-02.htm
http://nntime.com/proxy-list-03.htm
http://nntime.com/proxy-list-04.htm
http://nntime.com/proxy-list-05.htm
http://nntime.com/proxy-list-06.htm
http://nntime.com/proxy-list-07.htm
http://nntime.com/proxy-list-08.htm
http://nntime.com/proxy-list-09.htm
http://nntime.com/proxy-list-10.htm
http://nntime.com/proxy-list-11.htm
http://nntime.com/proxy-list-12.htm
http://nntime.com/proxy-list-13.htm
http://nntime.com/proxy-list-14.htm
http://nntime.com/proxy-list-15.htm
http://nntime.com/proxy-list-16.htm
http://nntime.com/proxy-list-17.htm
http://nntime.com/proxy-list-18.htm
http://nntime.com/proxy-list-19.htm
http://nntime.com/proxy-list-20.htm
http://nntime.com/proxy-list-21.htm
http://nntime.com/proxy-list-22.htm
http://nntime.com/proxy-list-23.htm
http://nntime.com/proxy-list-24.htm
http://nntime.com/proxy-list-25.htm
http://nntime.com/proxy-list-26.htm
http://nntime.com/proxy-list-27.htm
http://nntime.com/proxy-list-28.htm
http://nntime.com/proxy-list-29.htm
http://nntime.com/proxy-list-30.htm
https://free-proxy-list.net/
https://www.us-proxy.org/
https://free-proxy-list.net/uk-proxy.html
https://www.sslproxies.org/
https://free-proxy-list.net/anonymous-proxy.html
https://www.socks-proxy.net/
https://www.freeproxylists.net/
http://proxy-list.org/english/index.php
http://proxydb.net/
https://www.proxynova.com/proxy-server-list/
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt""".splitlines()

def start():
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
        if option == "1":
            clear()
            ascii()
            print("\n\n")
            print(f"    [{cyan}Pick Link File{reset}]")
            file_path = get_file("Proxy Site Links File","Proxy Site Links File")
            get_focus()
            if not file_path:
                print(f"    [{cyan}No File Detected{reset}]")
                sleep(1)
                return
            with open(file_path,errors="ignore") as file:
                original_links = file.read().splitlines()
                after_links = list(set(original_links))
                duplicates = len(original_links)-len(after_links)
            print(f"    [{cyan}Imported {len(original_links)} Links{reset}]")
            if duplicates != 0:
                print(f"    [{cyan}Removed {duplicates} Duplicates{reset}]")
            sleep(1)
            scrape(after_links)
        elif option == "2": scrape()
        elif option == "x": return

def scrape(links:str=None):
    Checker.time = get_time()
    proxies = []
    if not links:
        links = default
    def foo(link):
        count = 0
        try: a = get(link,timeout=Checker.timeout).text.splitlines()
        except: log(None,f"Connection Error ~ {link}")
        else:
            for line in a:
                try:
                    if ":" in line:
                        if len(line.split(":")) == 2:
                            proxy = line.split(":")
                            ip = proxy[0]
                            port = proxy[1]
                            for char in port:
                                if char not in list(set(digits)):
                                    port = port.split(char)[0]
                            for char in ip:
                                if char not in list(set(digits+".")):
                                    ip = ip.split(char)[-1]
                            if ip and port:
                                if "." in ip:
                                    if len(ip.split(".")) == 4:
                                        count += 1
                                        proxies.append(ip+":"+port)

                        elif len(line.split(":")) > 2:
                            for _ in range(len(line.split(":"))):
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
                                    if ip and port:
                                        if "." in ip:
                                            if len(ip.split(".")) == 4:
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
    print(f"    [{cyan}Saving {len(list(set(proxies)))} Proxies{reset}]")
    makedirs(f"Results/{Checker.time}",exist_ok=True)
    with open(f"Results/{Checker.time}/Scraped_Proxies.txt","w",errors="ignore") as file: file.write("\n".join(list(set(proxies))))
    print("\n\n")
    print(f"    [{cyan}Finished Scraping{reset}]")
    input(f"    [{cyan}Press Enter To Go Back{reset}]")