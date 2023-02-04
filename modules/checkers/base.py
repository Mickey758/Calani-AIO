from modules.variables import Checker
from modules.functions import bad_proxy, log, save, set_proxy, return_proxy
from requests import Session
import functools
from requests.adapters import HTTPAdapter, Retry

"""
USE THIS BASE FILE TO CREATE EXTRA MODULES FOR CALANI
REMEMBER TO ADD THE MODULE TO THE START.PY FILE
"""

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

                # Bad
                # Checker.bad += 1
                # return_proxy(proxy)
                # return

                # Good
                # if not Checker.cui: log("good",':'.join([email,password]),"NAME")
                # save("NAME","good",Checker.time,':'.join([email,password])+f"CAPTURE")
                # Checker.good += 1
                # return_proxy(proxy)
                # return

                # Custom
                # if not Checker.cui: log("custom",":".join([email,password]),"NAME")
                # save("NAME","custom",Checker.time,":".join([email,password]))
                # Checker.custom += 1
                # return_proxy(proxy)
                # return


        except:
            bad_proxy(proxy)
            return_proxy(proxy)
            Checker.errors += 1