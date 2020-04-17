# -*- coding: utf-8 -*-
__author__ = 'DarkBot FYP'

import time
import urllib.request
from urllib.error import HTTPError
from urllib.error import URLError
from stem import Signal
from stem.control import Controller


class ConnectionManager:
    def __init__(self):
        self.new_ip = "0.0.0.0"
        self.old_ip = "0.0.0.0"
        self.new_identity()

    @classmethod
    def _get_connection(self):
        """
        TOR new connection
        """
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password="9339")
            controller.signal(Signal.NEWNYM)
            controller.close()

    @classmethod
    def _set_url_proxy(self):
        """
        Request to URL through local proxy
        """
        proxy_support = urllib.request.ProxyHandler({"http": "127.0.0.1:8118"})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)

    @classmethod
    def request(self, url):
        """
        TOR communication through local proxy
        :param url: web page to parser
        :return: request
        """
        try:
            self._set_url_proxy()
            request = urllib.request.Request(url, None, {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
                              "AppleWebKit/535.11 (KHTML, like Gecko) "
                              "Ubuntu/10.10 Chromium/17.0.963.65 "
                              "Chrome/17.0.963.65 Safari/535.11"})
            request = urllib.request.urlopen(request)
            return request
        except HTTPError as e:
            print(e.msg)
            return e.msg

    def new_identity(self):
        """
        new connection with new IP
        """
        # First Connection
        if self.new_ip == "0.0.0.0":
            self._get_connection()
            self.new_ip = self.request("http://icanhazip.com/").read()
        else:
            self.old_ip = self.new_ip
            self._get_connection()
            self.new_ip = self.request("http://icanhazip.com/").read()

        seg = 0

        # If we get the same ip, we'll wait 5 seconds to request a new IP
        while self.old_ip == self.new_ip:
            time.sleep(5)
            seg += 5
            print ("Waiting to obtain new IP: %s Seconds" % seg)
            self.new_ip = self.request("http://icanhazip.com/").read()

        print ("New connection with IP: %s" % self.new_ip)