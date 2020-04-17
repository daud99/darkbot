from dark_bot import settings
import requests
#import cfscrape
import time
import string
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
from search.darkbot.common.firefox_proxy import proxy_profile
from selenium import webdriver
from time import sleep
#from tor_connection import connect_tor
url = "https://haveibeenpwned.com"
class HaveIBeenPwned:
    def __init__(self):
        self.driver =None
        self.wait = None
        self.cookies = None
        self.url = url

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
    def create_driver(self):
        print("setting xvfb for first time")  
        if(not self.driver):
            while(True):
                try:
                    #chrome_options = Options()
                    options = webdriver.FirefoxOptions()
                    profile = proxy_profile()
                    options.add_argument('--headless') 
                    #self.driver = webdriver.Firefox(options=options)
                    self.driver = webdriver.Firefox(options=options, firefox_profile=profile)
                except Exception as e:
                    continue
                else:
                    break
    def refresh_driver(self):
        if (self.driver):
            self.driver.refresh()
        else:
            print('You are refreshing with None driver')
    def visit_email_search_page(self):
        
        #driver.implicitly_wait(60)
        for i in range(0, 5):
            try:
                if (self.cookies):
                    print (self.cookies)
                    #dd the stored session in the bew web driver instance
                    for cookie in self.cookies:

                        self.driver.add_cookie(cookie)
                self.driver.get(self.url)

            except NewConnectionError as n:
                self.cookies = None
                print("Generate new connection")
                continue
            except WebDriverException as e:
                print(e)
                print("internet problem")
                continue
            else:
                print("internet found")
                self.wait = WebDriverWait(self.driver,25)
                return True
        return False       
        
    def search_by_email(self, query):
        self.create_driver()
        check = self.visit_email_search_page()
        if check== False:
            return False
        self.load_waiting()
        check = False
        for i in range(0,2):
            
            try:
                print('wait at loading')
                self.wait.until(EC.visibility_of_element_located((By.ID,'Account')))
                self.wait.until(EC.visibility_of_element_located((By.ID,'searchPwnage')))
                #sleep(20)
            except TimeoutException as e:
                continue
            except NewConnectionError as n:
                self.cookies = None
                continue
            except Exception as e:
                continue
            
            else:
                check = True
                break
        if check != True:
            return False
        try:

            searchField = self.driver.find_element_by_id('Account')
            searchField.clear()
            searchField.send_keys(query)
            searchButton = self.driver.find_element_by_id('searchPwnage')
            searchButton.click()
        except ElementNotInteractableException as e:
            print('Got button')
            return False
        except NoSuchElementException as e:
            print('Got button')
            return False
        return True
    def check_loading_completion(self):
        check = False
        for i in range(0,2):
            try:
                self.wait.until(EC.invisibility_of_element_located((By.ID,'loading')))
            except TimeoutException as te:
                print('timeout at loading')
                continue
            except Exception as e:
                continue
            else:
                check = True
                break
        if check == False:
            return False
        else:
            return True
    def retrieve_breaches(self):
        check = self.check_loading_completion()
        if check == False:
            return {'message': 'Found No Results', 'breaches':[]}
        check = self.load_waiting()

        if check == False:
            return {'message': 'Found No Results', 'breaches':[]}
        
        try:

            self.wait.until(EC.visibility_of_all_elements_located((By.ID,'pwnedSites')))
        except TimeoutException as te:
            return {'message': 'Found No Results', 'breaches':[]}
        except Exception as e:
            return {'message': 'Found No Results', 'breaches':[]}
        try:
            print('reading breaches')
            resluts = self.driver.find_element_by_id('pwnedSites')
            resluts = resluts.get_attribute('innerHTML')
            bs = BeautifulSoup(resluts,'html.parser')
            #print(bs)
            breach_list = []
            breach_dict = dict()
            result_rows = bs.find_all('div', recursive=False)
            for row in result_rows:
                container = row.find('div',{'class': 'container'})
                data_field = container.find('div',{'class':'row'})
                divs_in_datField = data_field.find_all('div')
                if (len(divs_in_datField)<2):
                    continue
                data_div = divs_in_datField[1]
                paras = data_div.find_all('p')
                description_div = paras[0]
                dataClasses = None
                if len(paras)>1:
                    dataClasses = paras[1]
                
                company = description_div.find('span',{'class':'pwnedCompanyTitle'}).find(text=True, recursive=False)
                company = company.strip()
                company = company.strip("{}()<>:;,'\"")
                company = company.strip()
                description_div.span.clear()
                description = description_div.get_text()
                description = description.strip()
                description = description.strip(':')
                description = description.strip()
                compromised_data = None
                if dataClasses:
                    dataClasses.strong.clear()
                    compromised_data = dataClasses.get_text().strip()
                breach_dict['company'] = company
                breach_dict['description'] = description
                breach_dict['compromised_data'] = compromised_data
                breach_list.append(breach_dict.copy())
                breach_dict.clear()
        except NoSuchElementException as e:
            return {'message': 'Found No Results', 'breaches':[]}
        except AttributeError as e:
            return {'message': 'Found No Results', 'breaches':[]}
        except Exception as e:
            return {'message': 'Found No Results', 'breaches':[]}
        else:
            return {'message': 'Found '+ str(len(breach_list))+' results', 'breaches': breach_list}
    
    def retrieve_pastes(self):
        check = self.check_loading_completion()
        if check == False:
            return {'message': 'Found No Results', 'pastes':[]}
        check = self.load_waiting()
        if check == False:
            return {'message': 'Found No Results', 'pastes':[]}
        
        try:
            self.wait.until(EC.visibility_of_all_elements_located((By.ID,'pasteDescription')))
            self.wait.until(EC.visibility_of_all_elements_located((By.ID,'pastes')))
        except TimeoutException as te:
            return {'message': 'Found No Results', 'pastes':[]}
        except Exception as e:
            return {'message': 'Found No Results', 'pastes':[]}
        try:
            print('pastes')
            resluts = self.driver.find_element_by_css_selector('#pasteDescription + #pastes')
            resluts = resluts.get_attribute('innerHTML')
            bs = BeautifulSoup(resluts,'html.parser')
            #print(bs)
            breach_list = []
            breach_dict = dict()
            result_rows = bs.find('div',{'id':'pastes'}, recursive=False)
            result_table = result_rows.find('table',{'class':'table-striped'})
            table_rows = result_table.find_all('tr')[1:]
            for row in table_rows:
                tds = row.find_all('td')
                title = tds[0].get_text().strip()
                '''
                for x in title:
                    if x not in list(string.printable):
                        title.replace(x,'')
                '''
                title =(title.encode('ascii','ignore')).decode('utf-8').strip()
                title = title.split(',')[0]
                breach_dict['paste_title'] = title
                breach_dict['paste_url'] =tds[0].a['href']
                breach_dict['date'] = tds[1].get_text().strip()
                breach_dict['total_emails'] = tds[2].get_text().strip()
                breach_list.append(breach_dict.copy())
                breach_dict.clear()
        except NoSuchElementException as e:
            return {'message': 'Found No Results', 'pastes':[]}
        except AttributeError as e:
            return {'message': 'Found No Results', 'pastes':[]}
        except Exception as e:
            return {'message': 'Found No Results', 'pastes':[]}
        else:
            return {'message': 'Found '+ str(len(breach_list))+' results', 'pastes': breach_list}
    
    
    def close_driver(self):
        #global xvfb_display, driver, wait, cookies
        #driver.close()
        if(self.driver):
            self.driver.quit()
        #xvfb_display.stop()
        self.driver= None
        self.wait= None
        self.cookies= None
    
 
def getBreach(email):
    print('getBreach')
    key = settings.HIBP_KEY
    agent = settings.HIBP_USER_AGENT
    headers = {'hibp-api-key': key, "User-Agent": agent}
    url = "https://haveibeenpwned.com/api/v3/breachedaccount/" + email + "?truncateResponse=false"
    try:
        res = requests.get(url, headers=headers)
        # for each in res:
        #     print(each)
        #res = []
    except Exception as err:
        return []
    if (res.status_code != 200):
        return []
    res = res.json()
    return res



def getPaste(email):
    print('getPaste')
    url = "https://haveibeenpwned.com/api/v3/pasteaccount/" + email
    key = settings.HIBP_KEY
    agent = settings.HIBP_USER_AGENT
    headers = {'hibp-api-key': key, "User-Agent": agent}
    try:
        res = requests.get(url, headers=headers)
        # for each in res:
        #     print(each)
        #res = []
    except Exception as err:
        return []
    if (res.status_code != 200):
        return []
    res = res.json()
    return res



if __name__ == '__main__':
    #connect_tor()
    driver = HaveIBeenPwned()
    driver.search_by_email('zeeshan@gmail.com')
    #p = driver.retrieve_breaches()
    #p = driver.retrieve_pastes()
    p = driver.retrieve_breaches()
    print(p)