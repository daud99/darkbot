# -*- coding: utf-8 -*-
__author__ = 'DarkBot FYP'

from bs4 import BeautifulSoup
#import cfscrape
import time
#import subprocess
import argparse
import socket
import socks
import urllib
import requests
from requests.exceptions import HTTPError
from urllib.request import urlopen
#import asyncio
#from aiocfscrape import CloudflareScraper


#from ConnectionManager import ConnectionManager
# GLOBAL CONSTS
LOCALHOST = "127.0.0.1"
DEFPORT = 9050
temp = ''
v = 1
# DarkBot VERSION
__VERSION = "1.0"

def disconnect():
    global temp
    global v
    if v == 1:
        temp=socket.socket
        v = v+1
        print("TEMPPPPPPPPPP BELOW")
        print(temp)
    socket.socket = temp

def connect(address, port):
    pass
    """ Establishes connection to port

    Assumes port is bound to localhost, if host that port is bound to changes
    then change the port

    Args:
        address: address for port to bound to
        port: Establishes connect to this port
    """

    '''
    if address and port:
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, address, port)
    elif address:
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, address, DEFPORT)
    elif port:
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, LOCALHOST, port)
    else:
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, LOCALHOST, DEFPORT)
    
    socket.socket = socks.socksocket  # Monkey Patch our socket to tor socket
    '''

   
def header():
    print("DarkBot")
def get_args():
    """
    Parses user flags passed to DarkBot
    
    parser = argparse.ArgumentParser(prog="TorBot",
                                     usage="Gather and analayze data from Tor sites.")
    parser.add_argument("--version", action="store_true",
                        help="Show current version of TorBot.")
    parser.add_argument("--update", action="store_true",
                        help="Update TorBot to the latest stable version")
    parser.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-u", "--url", help="Specifiy a website link to crawl")
    parser.add_argument("--ip", help="Change default ip of tor")
    parser.add_argument("-p", "--port", help="Change default port of tor")
    parser.add_argument("-s", "--save", action="store_true",
                        help="Save results in a file")
    parser.add_argument("-m", "--mail", action="store_true",
                        help="Get e-mail addresses from the crawled sites")
    parser.add_argument("-e", "--extension", action='append', dest='extension',
                        default=[],
                        help=' '.join(("Specifiy additional website",
                                       "extensions to the list(.com , .org, .etc)")))
    parser.add_argument("-i", "--info", action="store_true",
                        help=' '.join(("Info displays basic info of the",
                                       "scanned site")))
    parser.add_argument("--depth", help="Specifiy max depth of crawler (default 1)")
    parser.add_argument("-v", "--visualize", action="store_true",
                        help="Visualizes tree of data gathered.")
    parser.add_argument("-d", "--download", action="store_true",
                        help="Downloads tree of data gathered.")
    return parser.parse_args()
    """
    return None
def connect_tor():
    '''
    return connect(None, None)
    '''
    proxies ={'http':'socks5h://127.0.0.1:9050', 'https':'socks5h://127.0.0.1:9050'}
    return proxies
'''
async def test_open_page(url, loop=None):

    async with CloudflareScraper(loop=loop) as session:
        async with session.get(url) as resp:
            data = await resp.text()
    return data
'''
if __name__ == "__main__":
    proxies = connect_tor()
    #print(x)
    url = 'http://ip.3300.ir/'
    url1 = 'http://gjobqjj7wyczbqie.onion'
    response = requests.get(url1, timeout=10, proxies=proxies)
    print("Set ip: {}".format(response.content))

    # Without Socks5
    url = 'http://ip.3300.ir/'
    response = requests.get(url, timeout=10)
    print("Set ip: {}".format(response.content))
#     #args = get_args()
#     connect(None, None)
#     URL_BASE = "https://ghostproject.fr/"
#     MAX_PAGES = 30
#     counter_post = 0
#
#    # cm = ConnectionManager()
#     scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
#     scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
#     x =scraper.get(URL_BASE)
#     time.sleep(10)
#     print(x)
#     x =scraper.get(URL_BASE).content
#     print (x) # => "<!DOCTYPE html><html><head>..."
#     print("abcd")
#     html = BeautifulSoup(x.read(), "html.Parser")
#     print(html.find(input, {id:'searchStr'}))
#     '''
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(test_open_page(URL_BASE, loop=loop))
#     loop.close()
#     '''
#
#
#     '''
#     cookie_arg, user_agent = cfscrape.get_cookie_string(URL_BASE)
#     cmd = "curl --cookie {cookie_arg} -A {user_agent} {url}"
#     print(subprocess.check_output(cmd.format(cookie_arg=cookie_arg,
#     user_agent=user_agent, url=url), shell=True))
#     '''
#     url = URL_BASE
#
#     req = URL_BASE
#     '''
#     request1 = urllib.request.Request(url, {
#                 'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
#                               "AppleWebKit/535.11 (KHTML, like Gecko) "
#                               "Ubuntu/10.10 Chromium/17.0.963.65 "
#                               "Chrome/17.0.963.65 Safari/535.11",
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#                 'Accept-Encoding': 'none',
#                 'Accept-Language': 'en-US,en;q=0.8',
#                 'Connection': 'keep-alive'})
#
#     request2 = urlopen( str (request1))
#
#     #req= request
#     #req = requests.get(url)
#     req = request2.read()
#    # print(args)
#     status_code = req.status_code if req != '' else -1
#     print(status_code)
#     if status_code == 200:
#         html = BeautifulSoup(req.text, "html.parser")
#         posts = html.find_all('a')
#         print(posts)
#
#     else:
#         # if status code is diferent to 200
#         pass
#     '''
#     # obtain new ip if 5 requests have already been made