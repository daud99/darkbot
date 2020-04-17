import requests
import urllib.parse
import cloudscraper
from bs4 import BeautifulSoup
import json
from search.darkbot.tor_connection import connect_tor
#from tor_connection import connect_tor
url = "https://haveibeenpwned.com"
class HaveIBeenPwned:
    def __init__(self):
        self.url = url
        self.response_json = None
    def parse_email(self, email):
        try:
            parsed_email = urllib.parse.quote(email)
        except Exception as e:
            return None
        else:
            return parsed_email
        
    def get_request_headers(self):
        headers = {
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) "
                        "AppleWebKit/535.11 (KHTML, like Gecko) "
                        "Ubuntu/10.10 Chromium/17.0.963.65 "
                        "Chrome/17.0.963.65 Safari/535.11",
                        'accept': '*/*',
                        'Content-type': 'application/json',
                        #'accept-encoding': 'gzip, deflate, br',
                        #'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                        'dnt': '1',
                        'referer': 'https://haveibeenpwned.com/',
                        #'request-context': 'appId=cid-v1:bcc569a3-d364-4306-8bbe-83e9fe4d020e',
                        'request-id': '|gQnbg.yBzHU',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'x-requested-with': 'XMLHttpRequest'
                        }
        return headers

    def clean_and_decode_text(self, data):
        soup = BeautifulSoup(data, 'html5lib')
        response_data = soup.text.encode('ascii','ignore').decode('utf-8')
        return response_data

    def text_to_json(self, data):
        '''
        try:
            dumped_response = json.dumps(data)
            response_json = json.loads(dumped_response)
        except Exception as e:
            return None
        else:

            return response_json
        '''
        pass
    def search_by_email(self,email):
        parsed_email = self.parse_email(email)
        if (parsed_email== None):
            parsed_email = email
        session = requests.sessions.session()
        scraper= cloudscraper.create_scraper(sess=session)
        headers = self.get_request_headers()
        url = self.url+'/unifiedsearch/'+parsed_email
        try:
            response = scraper.get(url, headers=headers, timeout=(20,30))
        except Exception as e:
            return False
        #print(response.json())
        if (response.status_code != 200):
            #return {'message': 'Found No Results', 'breaches':[]}
            self.response_json = None
            return False
        #response = response.text.encode('ascii','ignore').decode('utf-8')
        else:
            self.response_json = response.json()
            return True
            '''
            response_data = self.clean_and_decode_text(response.content)
            response_json = self.text_to_json(response_data)
            if (response_json == None):
                #return {'message': 'Found No Results', 'breaches':[]}
                self.response_json = None
                return False
            else:
                self.response_json = response_json
                return True
            '''
    def justify_strings(self, input_str):
        input_str = input_str.strip()
        ret_str = input_str.strip("{}()<>:;,'\"")
        return ret_str
    def modify_description(self, input_str, str_1,str_2):
        return input_str.replace(str_1,str_2)
    def clean_breach_list(self, b_list):
        final_breaches = []
        for breach in b_list:
            temp_breach = {}
            name = breach['Name']
            name = self.justify_strings(name)
            temp_breach['Name'] = name
            title = self.justify_strings(breach['Title'])
            temp_breach['company'] = title
            description = self.clean_and_decode_text(breach['Description'])
            description = self.modify_description(description,'Have I Been Pwned', 'Tranchulas Database System')
            temp_breach['description'] = description
            x = breach['DataClasses']
            breached_data = ""
            for s in x:
                breached_data = breached_data +" "+ s + ' ,'
            temp_breach['compromised_data'] = breached_data.strip(',')
            temp_breach['domain'] = breach.get('Domain')
            temp_breach['PwnCount'] = breach.get('PwnCount')
            temp_breach['BreachDate'] = breach.get('BreachDate')
            temp_breach['AddedDate'] = breach.get('AddedDate')
            temp_breach['ModifiedDate'] = breach.get('ModifiedDate')
            temp_breach['LogoPath'] = breach.get('LogoPath')
            final_breaches.append(temp_breach.copy())
        return final_breaches
    def retrieve_breaches(self):
        if (not self.response_json):
            return {'message': 'Found No Results', 'breaches':[]}
        else:
            if (self.response_json.get('Breaches')):
                Breach_list = self.response_json.get('Breaches')
                message = 'Found '+str(len(Breach_list))+' Results'
                Breach_list = self.clean_breach_list(Breach_list)
                return {'message': message, 'breaches':Breach_list}
            else:
                return {'message': 'Found No Results', 'breaches':[]}
            #print(response_data['breaches'])
    def clean_paste_list(self, paste_list):
        final_pastes = []
        for paste in paste_list:
            temp_paste = {}
            temp_paste['paste_url'] = paste.get('Id')
            temp_paste['Source'] = paste.get('Source')
            if(paste.get('Title')):
                title = paste['Title'].encode('ascii','ignore').decode('utf-8')
                if ',' in title:
                    title = title.split(',')[0]
                title= title.strip()
                temp_paste['paste_title'] = title
            else:
                temp_paste['paste_title'] = 'Not Defined'
            temp_paste['date'] = paste.get('Date')
            temp_paste['total_emails'] = paste.get('EmailCount')
            final_pastes.append(temp_paste.copy())
        return final_pastes
    def retrieve_pastes(self):
        if (not self.response_json):
            return {'message': 'Found No Results', 'pastes':[]}
        else:
            if (self.response_json.get('Pastes')):
                paste_list = self.response_json.get('Pastes')
                message = 'Found '+str(len(paste_list))+' Results'
                paste_list = self.clean_paste_list(paste_list)
                #print(paste_list)
                return {'message': message, 'pastes':paste_list}
            else:
                return {'message': 'Found No Results', 'pastes':[]}
    def close_driver(self):
        print('Closing')

if __name__ == "__main__":
    h = HaveIBeenPwned()
    h.search_by_email('zeeshan@gmail.com')
    print(h.retrieve_breaches())