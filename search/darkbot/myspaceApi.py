import time
import datetime
import re
import os
import requests
from decimal import Decimal
# from webbot import Browser
# import asyncio
from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError
from selenium.webdriver.support.ui import Select, WebDriverWait
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import start_xvfb, stop_xvfb
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from time import sleep
from gatherdumps.scripts.common import tor_path
# from gatherdumps.models import dumps
from django.utils import timezone


class MySpacX_pass_mail:
    def __init__(self):
        self.xvfb_display = None
        self.driver = None
        self.wait = None
        self.cookies = None
        # self.searchField = None
        # self.query = query
        self.url = 'http://myspacexsan7ksvq.onion/'

    def stop_display(self):
        stop_xvfb(self.xvfb_display)
        # pass

    def start_display(self):
        self.xvfb_display = start_xvfb()
        # pass

    def create_driver(self):
        # global xvfb_display, driver, wait, cookies
        if (not self.xvfb_display):
            print("setting xvfb for first time")
            self.start_display()
        if (not self.driver):
            driver_path = tor_path.get_path()
            self.driver = TorBrowserDriver(driver_path)
        while True:
            try:
                if (self.cookies):
                    print (self.cookies)
                    # dd the stored session in the bew web driver instance
                    for cookie in self.cookies:
                        self.driver.add_cookie(cookie)
                self.driver.load_url(self.url, wait_for_page_body=True)
            except NewConnectionError as n:
                self.cookies = None
                print("Generate new connection")
                self.driver.get(self.url)
            except WebDriverException as e:
                print(e)
                print("internet problem")
                continue
            else:
                print("internet found")
                break
        self.wait = WebDriverWait(self.driver, 25)

    def load_waiting(self):
        start_time = time.time()
        while (True):
            ready_State = self.driver.execute_script('return document.readyState')
            print(ready_State)
            finish_time = time.time()
            total_time = finish_time - start_time
            if (ready_State not in ['complete'] and total_time < 50):
                sleep(1)
                continue
            else:
                # cookies = driver.get_cookies()
                return True
        return False

    def analyze_response(self, text):
        if text in ["", " ", None]:
            return []
        elif text.find("No results found") > 0:
            return []
        elif text.find("[404] No results found") > 1:
            return []
        else:

            return re.findall(r'[\w\.-]+@[\w\.-]+', text)

    def retrieve_emails(self, passw):
        check = False
        for i in range(0, 1):
            try:
                self.wait.until(EC.visibility_of_all_elements_located((By.ID, 'password')))
                self.wait.until(EC.visibility_of_all_elements_located((By.ID, 'submit-password')))
                searchField = self.driver.find_element_by_id('password')
            except TimeoutException as te:
                continue
            except Exception as e:
                continue
            else:
                check = True
                break
        if check == False:
            return {'total_results': 0, 'documents': []}
        check = False
        for i in range(0, 2):
            try:
                searchField.clear()
                searchField.send_keys(passw)
                searchButton = self.driver.find_element_by_id('submit-password')
            except Exception as e:
                continue
            else:
                check = True
                break
        if check == False:
            return {'total_results': 0, 'documents': []}
        self.wait.until(EC.visibility_of_all_elements_located((By.ID, 'password-result')))
        searchButton.click()
        self.load_waiting()
        password_result = ""
        start_time = time.time()
        end_time = start_time + 40
        while (password_result in ["", " ", None] and time.time() < end_time):
            password_result = self.driver.find_element_by_id('password-result').text
        time.sleep(1)
        emails_list = self.analyze_response(password_result)
        return {'total_results': len(emails_list), 'documents': emails_list}

    def retrieve_emails_by_hash(self, passw):
        check = False
        for i in range(0, 2):
            try:
                self.wait.until(EC.visibility_of_all_elements_located((By.ID, 'hash')))
                self.wait.until(EC.visibility_of_all_elements_located((By.ID, 'submit-hash')))
                searchField = self.driver.find_element_by_id('hash')
            except TimeoutException as te:
                continue
            except Exception as e:
                continue
            else:
                check = True
                break
        if check == False:
            return {'total_results': 0, 'documents': []}
        check = False
        for i in range(0, 2):
            try:
                searchField.clear()
                searchField.send_keys(passw)
                searchButton = self.driver.find_element_by_id('submit-hash')
            except Exception as e:
                continue
            else:
                check = True
                break
        if check == False:
            return {'total_results': 0, 'documents': []}
        self.wait.until(EC.visibility_of_all_elements_located((By.ID, 'hash-result')))
        searchButton.click()
        self.load_waiting()
        password_result = ""
        start_time = time.time()
        end_time = start_time + 40
        while (password_result in ["", " ", None] and time.time() < end_time):
            password_result = self.driver.find_element_by_id('hash-result').text
        time.sleep(1)
        emails_list = self.analyze_response(password_result)
        return {'total_results': len(emails_list), 'documents': emails_list}

    def close_driver(self):
        # driver.close()
        if self.driver:
            self.driver.quit()
        self.stop_display()
        self.xvfb_display = None
        self.driver = None
        self.wait = None
        self.cookies = None


if __name__ == "__main__":
    driver = MySpacX_pass_mail()
    driver.create_driver()
    driver.retrieve_emails('abcd')

    # driver.search_by_country('Pakistan')
    # print(driver.get_current_page_dumps())