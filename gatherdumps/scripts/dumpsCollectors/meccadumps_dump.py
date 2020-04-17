import time
import datetime
import os
import requests
from decimal import Decimal
#from webbot import Browser
#import asyncio
from bs4 import BeautifulSoup
from urllib3.exceptions import NewConnectionError
from selenium.webdriver.support.ui import Select, WebDriverWait
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import start_xvfb, stop_xvfb
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
from gatherdumps.scripts.db.store_to_db import store_dumps, store_cvvs
#from gatherdumps.models import dumps
from gatherdumps.scripts.captchaSolver.bypassCaptcha import bypass_captcha
from gatherdumps.scripts.captchaSolver import txt
from gatherdumps.scripts.common import tor_path
from django.utils import timezone
class Meccadumps_DumpFinder:
    def __init__(self, m_url, m_username, m_password):
        self.xvfb_display=None
        self.driver =None
        self.wait = None
        self.cookies = None
        #self.searchField = None
        #self.query = query
        self.last_index = None
        self.url_o = m_url
        if (not self.url_o.endswith('/')):
            self.url = self.url+"/"
        else:
            self.url = self.url_o
        self.username = m_username
        self.password = m_password
        self.captcha = None
        self.captcha_image = None
    def stop_display(self):
        stop_xvfb(self.xvfb_display)
        #pass
    def start_display(self):
        self.xvfb_display = start_xvfb()
        #pass

    def create_driver(self):
        #global xvfb_display, driver, wait, cookies
        if (not self.xvfb_display):
            print("setting xvfb for first time")
            self.start_display()
        if(not self.driver):
            #options = webdriver.FirefoxOptions()
            #options.add_argument('--headless') 
            #self.driver = webdriver.Firefox(options=options)
            driver_path = tor_path.get_path()
            self.driver = TorBrowserDriver(driver_path)
        while True:
            
            try:
                if (self.cookies):
                    print (self.cookies)
                    #dd the stored session in the bew web driver instance
                    for cookie in self.cookies:

                        self.driver.add_cookie(cookie)
                self.driver.load_url(self.url,wait_for_page_body=True)
                #self.driver.get(self.url)
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
        self.wait = WebDriverWait(self.driver,35)
    
    def take_snapshot(self):
        try:

            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.load_url(self.url+'captcha/', wait_for_page_body=True)
            self.wait.until(EC.visibility_of_element_located((By.TAG_NAME,'img')))
            
            elm = self.driver.find_element_by_tag_name('img')
            captcha_image = 'zozo'+str(datetime.datetime.now())+'test.png'
            elm.screenshot(captcha_image)
        except Exception as e:
            return None
        else:

            return captcha_image
      
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
                #cookies = driver.get_cookies()
                return True
        return False

    def login(self):
        
        while(True):
            captcha_image = self.take_snapshot()
            captcha_text = bypass_captcha(captcha_image)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            if (captcha_text):
                captcha_text = captcha_text.lower()
                login = self.driver.find_element_by_id('login')
                passw = self.driver.find_element_by_id('password')
                captch = self.driver.find_element_by_id('captcha')
                login_button = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[1]/div[1]/form/button')
                login.clear()
                passw.clear()
                #captch.clear()
                login.send_keys(self.username)
                passw.send_keys(self.password)
                captch.send_keys(captcha_text)
            else:
                continue
            login_button.click()
            time.sleep(1)
            
            #chek if it is true or false
            check = self.load_waiting()
            try:
                cc_xpath ='/html/body/div[1]/div/div[1]/div[2]/div/ul/li[6]/a'
                self.wait.until(EC.visibility_of_element_located((By.XPATH,cc_xpath)))
            except TimeoutException as t:
                print('May be net err or wrong captcha')
                continue
            except Exception as e:
                print('Err at login: wrong captcha or some net failure')
                continue
            else:
                break
        #self.driver.refresh()
        #print(self.driver.page_source)
    def visit_cvvs(self):
        #self.driver.load_url(self.url+'cc',wait_for_page_body=True)
        self.driver.get(self.url+'dumps')
        
    def search_by_country(self,country):
        #searchField = self.driver.find_element_by_xpath('/html/body/span/span/span[1]/input')
        countries_container= self.driver.find_element_by_id('select2-countries-container').click()
        searchField = self.driver.switch_to.active_element
        searchField.clear()
        searchField.send_keys(country)
        #time.sleep(4)
        #time.sleep(10)
        try:
        #tag_class = "select2-results__option select2-results__option--highlighted"
            css_select ='.select2-results__option.select2-results__option--highlighted'
            self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,css_select)))
        except TimeoutException as te:
            print('could not find highlighted country')
            return False
        except Exception as e:
            print('could not find highlighted country')
            return False
        #self.driver.implicitly_wait(5)
        #self.page_source = self.driver.page_source
        selected_country = self.driver.find_element_by_css_selector(css_select).text
        
        if country.strip() == selected_country.strip():

            searchField.send_keys(Keys.ENTER)
        else:
            print('names doesnt match')
            return False
        #searchField.send_keys(Keys.ENTER)
        
        #temp_elem = self.driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li')
        #tag_css = 'html.localstorage body span.select2-container.select2-container--default.select2-container--open span.select2-dropdown.select2-dropdown--above span.select2-results ul#select2-countries-results.select2-results__options li.select2-results__option.select2-results__option--highlighted'
        #self.wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/span/span/span[2]/ul/li')))
        self.load_waiting()
        return True
    
    def get_current_page_cvvs(self):
        #time.sleep(5)
        try: 

            self.wait.until(EC.visibility_of_element_located((By.ID,'shop')))
            css_sel = '#shop > tbody:nth-child(2) > tr'
            self.wait.until(EC.invisibility_of_element_located((By.ID,'loader')))
            self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,'price-cell')))
            
        except TimeoutException as te:
            return None

        self.load_waiting()
        #time.sleep(5)
        #self.wait.until(EC.staleness_of(self.driver.find_element_by_tag_name('html')))
        '''
        while (self.page_source==self.driver.page_source):
            time.sleep(0.5)
        '''
        #print(self.driver.find_element_by_id('shop').get_attribute('innerHTML'))
        #print(self.driver.find_element_by_class_name('dumps').get_attribute('innerHTML'))
        #test = self.driver.execute_script('return $("tbody.dumps").innerHTML')
        #print(test)
        '''
        while (test in ['',' ',None]):
            #self.driver.implicitly_wait(1)
            time.sleep(0.5)
            print('waiting for tbody')
        '''

        shop = self.driver.find_element_by_id('shop')
        html = shop.get_attribute('innerHTML')
        #print(html)
        bank_json = dict()
        bank_json.clear()
        banks_array =list()
        banks_array.clear()
        try:
            print('trying')
            bs = BeautifulSoup(html,'html.parser')
            #tbody = bs.find('tbody',{'class':'dumps'})
            if self.last_index:
                x = self.last_index + 1
                rows = bs.find_all('tr')[x:-1]
            else:

                rows = bs.find_all('tr')[1:-1]
            for row in rows:
                lbin_track = row.find('div',{'class':'l-track'}).get_text().strip()
                carr_code = row.find('div',{'class':'l-code'}).get_text().strip()
                bin_no =row.find('div',{'class':'l-bin'}).get_text().strip()
                
                card_type = row.find('div',{'class':'l-type'}).get_text().strip()
                category = row.find('div',{'class':'l-subtype'}).get_text().strip()
                is_refund = row.find('div',{'class':'l-ref'}).get_text().strip()

                lcountry = row.find('div',{'class':'l-country'})
                '''
                lcountry.div.clear()
                country = lcountry.get_text().strip()
                '''
                #print(card_bank)
                #print(country)
                countryc = lcountry.find('div').next_sibling
                country = countryc.strip()
                card_mark =row.find('div',{'class':'l-mark'}).get_text().strip()
                card_bank = row.find('div',{'class':'l-bank'}).get_text().strip()
                #base = row.find('td',{'class':'lbasecc'})
                base = row.find('div',{'class':'l-base'}).get_text().strip()

                bb = base.split('(')
                base = bb[0]
                d_i = bb[-1]
                d_i = d_i.strip()
                dumped_in = d_i.strip(')')
                test = base.find('[ZIP]')
                if test != -1:
                    base = base.split('[ZIP]')
                    base = base[0]
                base = base.strip()
                #print(base)
                #print(country, state)
                #print(base)
                quantity = row.find('div',{'class':'l-available'}).get_text().strip()
                #print(quantity)
                price = row.find('div',{'class':'l-price'}).get_text()
                price = price.split()
                price = price[1]
                price = price.strip()
                
                #print(price)
                #price(price)
                #print('Next card is:')
                '''
                print(bin_no, card_type, category)
                print(is_refund)
                print(card_mark)
                print(expiry)
                print(name)
                print(city)
                print(state)
                print(zip_no)
                print(card_bank)
                print(country)
                print(base)
                print(price)
                '''

                bank_json['bin_no']= bin_no
                bank_json['track'] = lbin_track
                bank_json['carr'] = carr_code
                bank_json['card_type']= card_type
                bank_json['card_category']=category
                bank_json['refund']= is_refund
                bank_json['card_mark']= card_mark
                bank_json['bank']= card_bank
                bank_json['country']= country
                bank_json['dumped_in']=dumped_in
                bank_json['base']= base
                bank_json['quantity']= quantity
                bank_json['price']=price
                bank_json['source'] = self.url
                #bank_json['date']= datetime.datetime.now()
                bank_json['date']= timezone.now()
                banks_array.append(bank_json.copy())
                #store_dumps(banks_array)
                #print (str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
                #print(bank_json)

                '''
                print(bin_no, carr_code, card_type, is_refund, card_mark, card_bank,
                country,dumped_in,base, quantity, price)
                '''
        except AttributeError as e:
            print(e)
            print('attr error occured')
            return None
        except Exception as e:
            print('Exception like attr error in #shop')
            return None
        if (len(banks_array)<1):
            return None
        return banks_array.copy()



    def perform_crScrap_process(self, country,i):
        self.last_index = None
        #self.driver.get(self.url)
        self.driver.load_url(self.url+'dumps', wait_for_page_body= True)
        #self.driver.refresh()
        self.wait.until(EC.visibility_of_element_located((By.ID,'select2-countries-container')))
        
        check = self.search_by_country(country)
        if check == False:
            print('No match for country with id ', i)
            return False
        start_time = time.time()
        end_time = start_time + 900
        counter = 0
        while (time.time()<end_time):
            
            current_dumps = self.get_current_page_cvvs()
            #print(current_dumps)
            if current_dumps == None:
                return True
            else:
                
                #here store in db
                print(current_dumps[0]['country'])
                store_dumps(current_dumps)
                #print(current_dumps[0])
                #print(current_dumps[20])
                no_of_dumps= len(current_dumps)
                if not self.last_index:
                    self.last_index = no_of_dumps
                else:
            
                    self.last_index = self.last_index + no_of_dumps
                counter = counter + 1
                print ('till index',self.last_index,'of country with id',i, 'done')
                #the do this
                try:
                    if (self.driver== None):
                        return False
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                except AttributeError as ae:
                    print('Driver has no such attribute')
                    return False
                except Exception as e:
                    print('Could not find next button')
                    return False
                else:
                    #next_anchor = next_button.find_element_by_tag_name('a')
                    #next_anchor.click()
                    self.wait.until(EC.invisibility_of_element_located((By.ID,'loader')))
                    self.load_waiting()
        return True
            

    def close_driver(self):
        #driver.close()
        if self.driver:
            self.driver.quit()
        self.stop_display()
        self.xvfb_display=None
        self.driver= None
        self.wait= None
        self.cookies= None

if __name__ == "__main__":
    driver = Brocard_CvvFinder()
    driver.create_driver()
    driver.captcha = input("Enter captcha: ")
    driver.login()
    driver.visit_cvvs()
    driver.perform_crScrap_process('Pakistan',2)
    #driver.search_by_country('Pakistan')
    #print(driver.get_current_page_dumps())