# -*- coding: utf-8 -*-
__author__ = 'DarkBot FYP'

#from tor_connection import connect_tor
import urllib
import argparse
#from requests.exceptions import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
import requests
from search.darkbot.tor_connection import connect_tor,disconnect
def read_html(url):
    # first connect to tor network
    #connect_tor()
    headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
                              "AppleWebKit/535.11 (KHTML, like Gecko) "
                              "Ubuntu/10.10 Chromium/17.0.963.65 "
                              "Chrome/17.0.963.65 Safari/535.11"}
    '''
    req = urllib.request.Request(url, None, {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
                              "AppleWebKit/535.11 (KHTML, like Gecko) "
                              "Ubuntu/10.10 Chromium/17.0.963.65 "
                              "Chrome/17.0.963.65 Safari/535.11"})
    '''
   
    try:
        proxy = connect_tor()
        req = requests.get(url, headers=headers, proxies=proxy)
        if (req.status_code ==200):
            html = req.text
        else:
            return None
    except HTTPError as e:
        print ("Page at", url, "may be unavailable")
        print(e.msg)
        return None
    except URLError as u:
        print(url, "Server is down")
        return None
    except Exception as e:
        return None

    return html
    
    