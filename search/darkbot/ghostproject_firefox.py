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
from time import sleep
#from tor_connection import connect_tor
url_1 = "http://zfu7x4fuagirknhb.onion/"
url_2 = "https://ghostproject.fr/"
url = "https://ghostproject.fr"
class GhostProjectCrawler:
    def __init__(self, query):
        self.xvfb_display=None
        self.driver =None
        self.wait = None
        self.cookies = None
        self.searchField = None
        self.query = query
        self.url = url
    def connect_ghost(self):
        #global xvfb_display, driver, wait, cookies
        if (not self.xvfb_display):
            print("setting xvfb for first time")
            #xvfb_display = Display(visible=0, size=(800, 600))
            #xvfb_display.start()
        if(not self.driver):
            #chrome_options = Options()
            options = webdriver.FirefoxOptions()
            options.add_argument('--headless') 
            #chrome_options.add_argument("--headless") 
            #chrome_options.add_argument("--ignore-certificate-errors") 
            #capabilities = DesiredCapabilities.CHROME.copy()
            #capabilities['acceptSslCerts'] = True 
            #capabilities['acceptInsecureCerts'] = True
            #driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
            self.driver = webdriver.Firefox(options=options)
        #driver.implicitly_wait(60)

        while True:
            try:
                if (self.cookies):
                    print (self.cookies)
                    #dd the stored session in the bew web driver instance
                    for cookie in self.cookies:

                        self.driver.add_cookie(cookie)
                self.driver.get(self.url)
                #driver.get(url)
                #print(driver.page_source)
                self.driver.refresh()

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
    def main_page_processing(self):
        #global xvfb_display, driver, wait, cookies
        self.connect_ghost()
        while(True):
            
            try:
                print('wait at loading')
                self.wait.until(EC.visibility_of_element_located((By.ID,'searchStr')))
                #sleep(20)
            except TimeoutException as e:
                print()
                continue
            except NewConnectionError as n:
                self.cookies = None
                self.connect_ghost()    
                continue
            except Exception as e:
                continue
            
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


    def visit(self):
        #global cookies, driver, wait, xvfb_display, searchField
        self.main_page_processing()
        while (True):
            try:
                self.driver.find_element_by_partial_link_text('Got').click()
                self.cookies = self.driver.get_cookies()
                #main_page_processing()
                break
            except ElementNotInteractableException as e:
                print('Got button')
                break
            except NoSuchElementException as e:
                print('Got button')
                break
            except NewConnectionError as n:
                self.cookies = None
                self.main_page_processing()
                continue
           
        sleep(1)
        while (True):
            try:
                self.searchField=self.driver.find_element_by_id('searchStr')
            except NoSuchElementException as e:
                print("sfield exp")
                continue
                #self.driver.quit()
                #xvfb_display.stop()
            else:
                break
                
    def searching(self):
        #global cookies, driver, wait, xvfb_display, searchField
        self.visit()
        self.searchField.send_keys(self.query)
        #searchField.send_keys(Keys.ENTER)
        #Select.select_by_visible_text('Search')

    def retrieveData(self):  
        #global cookies, driver, wait, xvfb_display
        #searching()
        for j in range (1,5):
        
            self.searching()
            
            try:
                self.driver.find_element_by_xpath('/html/body/center/div/span/div/div/div/div[2]/div/div/div/div/div/div/div/div[5]/center/button').click()
            # driver.find_element_by_xpath('/html/body/center/div/span/div/div/div/div[2]/div/div/div/div/div/div/div/div[5]/center/button').click()
                #sleep(20)
                print('ok', j)
                #start_time = time.time()
                if (j !=4):
                    sleep(j*5)
                    self.wait.until(EC.visibility_of_element_located((By.ID,'result')))
                    p= self.driver.find_element_by_id('result').get_attribute('innerHTML')
                    print(p)
                    print('found 1')
                    bs = BeautifulSoup(p, 'html.parser')
                    x = bs.find_all('td')
                    x = x[1:len(x)]
                    z = []
                    for a in x:
                        if a not in [None, "", ' ']:
                            z.append(a.text)
                    if(p==""):
                        print("p==")
                        
                        continue
                    else:
                        print('Done P')
                        self.driver.close()
                        return z
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
                                if a not in [None,"", ' ']:
                                    z.append(a.text)
                            return z
                        else:
                            continue

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
        self.close_driver()
        return None
                    
                        
                        
                
            
        

     
    def close_driver(self):
        #global xvfb_display, driver, wait, cookies
        #driver.close()
        if(self.driver):
            self.driver.quit()
        #xvfb_display.stop()
        self.xvfb_display=None
        self.driver= None
        self.wait= None
        self.cookies= None
        self.query = None
    
 
    
            

if __name__ == '__main__':
    #connect_tor()

    gp = GhostProjectCrawler('zeeshan2@gmail.com')
    print(gp.retrieveData())