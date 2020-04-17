#from read_html import read_html
#from pyvirtualdisplay import Display
import requests
#import cfscrape
import time
#from webbot import Browser
#import asyncio
from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException 
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
#from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
#from selenium.webdriver import Firefox
from time import sleep
from pymongo import MongoClient
from search.darkbot.tor_connection import disconnect
#import cloudscraper
#from seleniumrequests import Firefox
#from seleniumrequests.request import RequestMixin
from search.darkbot.common.firefox_proxy import proxy_profile
#from tor_connection import connect_tor
url_1 = "http://zfu7x4fuagirknhb.onion/"
url_2 = "https://ghostproject.fr/"
url = "https://ghostproject.fr/"
url_vip = "https://ghostproject.fr/vip"
vip_pas = 'zubair@tranchulas.com'
'''
class MyCustomWebDriver(Firefox, RequestMixin):
    pass
'''
class GhostProjectCrawler:
    # driver = None
    # url = url_vip
    # vip_pass = vip_pas
    # cookies = None
    # wait = None
    # loginField= None
    def __init__(self):
        self.driver = None
        self.url = url_vip
        self.vip_pass = vip_pas
        self.cookies = None
        self.wait = None
        self.loginField = None
        self.xvfb_display=None
        #self.driver =None
        #self.wait = None
        #self.cookies = None
        self.searchField = None
        self.query = None
        #self.url = url_vip
        #self.vip_pass = vip_pass
        #self.user_agent=''
    @classmethod
    def connect_db(cls):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['fyp']
        col = db['ghostProjectCredentials']
        creds = col.find_one()
        cls.url = creds['url']
        cls.vip_pass = creds['pass']
    @classmethod
    def get_cftokens(cls):
        pass
        '''
        scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
        cookie_arg, user_agent =scraper.get_tokens(self.url)
        self.cookies = cookie_arg
        self.user_agent = user_agent
        '''
    #@classmethod
    def create_driver(self):
        options = webdriver.FirefoxOptions()
        #profile = proxy_profile()
        options.add_argument('--headless')
        check = False
        while(True):
            try:
                self.driver = webdriver.Firefox(options=options)
                #self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
            except WebDriverException as we:
                print(we.msg)
                if (check):
                    return False
                else:
                    disconnect()
                    check = True
                    continue
                    
            except Exception as e:
                print("Exception while creatig driver")
                return False
            else:
                self.wait = WebDriverWait(self.driver,30)
                return True
            return False
        '''
        tes=self.driver.request('POST', self.url,
        headers={'user-agent':self.user_agent}, cookies=self.cookies,
        data={'mtusr':self.vip_pass})
        
        self.driver.add_cookie(self.cookies)
        self.driver.get(url)
        print(self.driver.page_source)
        '''
    #@classmethod
    def request_page(self):
        #test = False
        for i in range(0,3):

            try:
                '''
                if (cls.cookies):
                            print (cls.cookies)
                            #dd the stored session in the bew web driver instance
                            for cookie in cls.cookies:

                                cls.driver.add_cookie(cookie)
                '''
                self.driver.get(self.url)
                #self.wait = WebDriverWait(self.driver,24)
            except NewConnectionError as n:
                self.cookies = None
                print("Generate new connection: new connection error occured")
                #self.driver.get(url)
                continue
            except WebDriverException as e:
                print(e)
                print("Web driver exception")
                continue
            else:
                print("internet found")
                #test = True
                return True
        return False

    #@classmethod
    def bypass_cloudflare(self):
        for i in range(0,2):
            
            try:
                print('wait at loading login page')
                self.wait.until(EC.visibility_of_element_located((By.NAME,'mtusr')))
                #sleep(20)
            except TimeoutException as e:
                print('Time out while locating login box')
                return False
            except NewConnectionError as n:
                self.cookies = None
                #self.connect_ghost()    
                continue
            except Exception as e:
                continue
            else:
                return True
        return False
    #@classmethod
    def login(self):
        start_time = time.time()
        
        while (True):
            try:

                ready_State = self.driver.execute_script('return document.readyState')
                print(ready_State)
                finish_time = time.time()
                total_time = finish_time - start_time
                if (ready_State in ['complete']):
                    break
                if (ready_State not in ['complete'] and total_time < 10):
                    sleep(0.5)
                    continue
                else:
                    #cookies = driver.get_cookies()
                    return False
            except Exception as e:
                print("Exception at login page")
                return False

        for i in range(0,3):
            try:
                
                self.loginField = self.driver.find_element_by_name('mtusr')
                self.loginField.clear()
                self.loginField.send_keys(self.vip_pass)
                
                self.driver.find_element_by_xpath('/html/body/div/table/tbody/tr[2]/td[2]/form/div/table/tbody/tr[3]/td[2]/p/input').click()
            except ElementNotInteractableException as e:
                print('mtusr field or login button not interactable')
                self.driver.refresh()
                continue
            except ElementNotVisibleException as e:
                print('mtusr field or login button not visible')
                self.driver.refresh()
                continue
            except NoSuchElementException as e:
                print('login field or button not found')
                self.driver.refresh()
                continue
            except NoSuchElementException as e:
                print('element click interceptible at login')
                self.driver.refresh()
                continue
            except NewConnectionError as n:
                self.cookies = None
                return False
            except Exception as e:
                return False
            else:
                
                return True
        return False

    def connect_ghost(self):
        #global xvfb_display, driver, wait, cookies
        if (not self.xvfb_display):
            print("setting xvfb for first time")
            #xvfb_display = Display(visible=0, size=(800, 600))
            #xvfb_display.start()
        if(not self.driver):
            test = self.create_driver()
            if (test == False):
                return False
        
        test= self.request_page()
        if test == False:
            return False
        test = self.bypass_cloudflare()
        if test == False:
            return False
        if (self.driver.current_url !=self.url):
            test = self.login()
        
        test = self.login()
        if test == False:
            return False
        
        '''
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless') 
        self.driver = webdriver.Firefox(options=options)
        '''
            #self.driver = MyCustomWebDriver()
        #driver.implicitly_wait(60)

        """
        while True:
            try:
                '''
                if not(self.cookies and self.user_agent):
                    #print (self.cookies)
                    #dd the stored session in the bew web driver instance
                    #for cookie in self.cookies
                    self.get_cftokens()
                self.wait = WebDriverWait(self.driver,24)
                self.driver.get(self.url)
                #print(self.driver.current_url)
                #driver.get(url)
                #print(driver.page_source)
                self.driver.refresh()
                '''
                
                #print(self.driver.page_source)
                #print(soup)
            except NewConnectionError as n:
                self.cookies = None
                print("Generate new connection")
                self.driver.get(url)
            except WebDriverException as e:
                print(e)
                print("internet problem")
                continue
            else:
                print("internet found")
                break
                
        self.wait = WebDriverWait(self.driver,120)
        #driver.start_client()
        """
        return True
    #@classmethod
    def refresh_driver(self):
        self.driver.refresh()
    #@classmethod
    def set_cookie(self, v):
        self.cookies= v
    def main_page_processing(self):
        #global xvfb_display, driver, wait, cookies
        if (self.driver):
            #self.refresh_driver()
            pass
        else:
            test = self.connect_ghost()
            if test == False:
                return False
        while(True):
            
            try:
                print('wait at loading')
                self.wait.until(EC.visibility_of_element_located((By.ID,'searchStr')))
                #sleep(20)
            except TimeoutException as e:
                print('Time out while locating search box')
                return False
            except NewConnectionError as n:
                #self.cookies = None
                self.set_cookie(None)
                test = self.connect_ghost() 
                if test == False:
                    return False   
                continue
            except Exception as e:
                return False
            
            sleep(1)
            break
            #wait = WebDriverWait(driver, 30)
            #wait.until(EC.element_to_be_clickable())
            #driver.implicitly_wait(400)
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
                #cookies = driver.get_cookies()
                break
        return True   


    def visit(self):
        #global cookies, driver, wait, xvfb_display, searchField
        test = self.main_page_processing()
        if test == False:
            return False
        while (True):
            try:
                self.driver.find_element_by_partial_link_text('Got').click()
                self.set_cookie(self.driver.get_cookies())
                #main_page_processing()
                break
            except ElementNotInteractableException as e:
                print('Got button not interactable')
                break
            except NoSuchElementException as e:
                print('Got button not found')
                break
            except NewConnectionError as n:
                self.set_cookie(None)
                test = self.main_page_processing()
                if test == False:
                    return False
                continue
           
        sleep(1)
        while (True):
            try:
                self.searchField=self.driver.find_element_by_id('searchStr')
            except NoSuchElementException as e:
                print("sfield exp: not found")
                return False
                #self.driver.quit()
                #xvfb_display.stop()
            else:
                break
        return True

    def searching(self,query):
        #global cookies, driver, wait, xvfb_display, searchField
        test = self.visit()
        if test == False:
            return False
        self.searchField.clear()
        self.searchField.send_keys(query)
        #self.searchField.clear()
        #searchField.send_keys(Keys.ENTER)
        #Select.select_by_visible_text('Search')
        return True
    def retrieveData(self, query):  
        #global cookies, driver, wait, xvfb_display
        #searching()
        test = self.searching(query)
        if test == False:
            z = None
            return z
        for j in range (4):
        
            
            try:
                self.driver.find_element_by_xpath('/html/body/center/div/span/div/div/div/div[2]/div/div/div/div/div/div/div/div[5]/center/button').click()
            # driver.find_element_by_xpath('/html/body/center/div/span/div/div/div/div[2]/div/div/div/div/div/div/div/div[5]/center/button').click()
                #sleep(20)
                print('ok', j)
                #start_time = time.time()
                if (j !=4):
                    sleep(j*2)
                    self.wait.until(EC.visibility_of_element_located((By.ID,'result')))
                    p= self.driver.find_element_by_id('result').get_attribute('innerHTML')
                    print(p)
                    print('found 1')
                    bs = BeautifulSoup(p, 'html.parser')
                    x = bs.find_all('td')
                    x = x[1:len(x)]
                    z = []
                    for a in x:
                        if a.text not in [None, "", ' ']:
                            if "No result" not in a.text:
                                z.append(a.text)
                    if(p==""):
                        print("p==")
                        
                        continue
                    else:
                        print('Done P')
                        #self.close_driver()
                        return z
                '''
                if (j==4):
                        
                    for w  in range(1,5):
                        if(w==3 or w==4):
                            self.driver.find_element_by_xpath('/html/body/center/div/span/div/div/div/div[2]/div/div/div/div/div/div/div/div[5]/center/button').click()
                            sleep(5)
                        #wait.until_not(EC.invisibility_of_element_located((By.ID,'result')))
                        sleep(5)
                        p = self.driver.find_element_by_id('result').get_attribute('innerHTML')
                        #print("a"+x+"b")
                        if x not in [None, '',""," "]:
                            print(p, 'yes')
                            #print("\n======== Locale: %s ========" % lang_code)
                            print () # status text
                            print ()  # IP address
                            self.close_driver()
                            #p= self.driver.find_element_by_id('result').get_attribute('innerHTML')
                            print('found 1')
                            bs = BeautifulSoup(p, 'html.parser')
                            x = bs.find_all('td')
                            x = x[1:len(x)]
                            z = []
                            for a in x:
                                if a.text not in [None,"", ' ']:
                                    if "No result" not in a.text:
                                        z.append(a.text)
                            return z
                        else:
                            continue
                '''

            except ElementNotVisibleException as ev:
                print('aa')
                continue
            except NoSuchElementException as e:
                print('bb')
                continue
            except ElementClickInterceptedException as e:
                            
                            
                continue
            except TimeoutException as e:
                print('cc')
                continue
            except Exception as e:
                continue
            
            break
        #x = None
        #self.close_driver()
        return None
    #@classmethod
    def close_driver(self):
        #global xvfb_display, driver, wait, cookies
        #driver.close()
        if(self.driver):
            self.driver.quit()
        #xvfb_display.stop()
        self.driver= None
        self.wait= None
        self.cookies= None
    
    def close_sub_driver(self):
        if (self.driver):
            self.driver.close()
        
    
 
    
            

if __name__ == '__main__':
    #connect_tor()

    gp = GhostProjectCrawler()
    #gp.connect_ghost()
    gp.retrieveData('zeeshan2@gmail.com')
    gp.close_sub_driver()
    