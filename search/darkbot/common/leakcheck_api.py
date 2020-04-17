import requests
from requests.exceptions import Timeout, HTTPError
import uuid
import multiprocessing
import threading
from search.darkbot.common.push_to_db import push_mails_to_db
#from search.views import save_passwords

def get_api_info(api_id= None):
    if (not api_id):
        return None
    else:
        api_id = uuid.UUID(api_id)
        try:
            obj = Api_info.objects.get(id=api_id)
        except Exception as e:
            print(e)
            return None
        else:
            return obj   
def parse_results(results):
    final_list = []
    if (len(results)==0):
        return ()
    for result in results:
        try:
            current_line = result.get('line')
            current_line = current_line.split(':')
            if(len(current_line) != 2):
                continue
            email = current_line[0].strip()
            email = email.lower()
            passw = current_line[1].strip()
            final_list.append((email,passw))
        except Exception as e:
            print('Exception while parsing current line in leakcheck results')
            print(e)
            continue
    return final_list

def get_leaks(query , query_type):
    #api_info = get_api_info(api_id='28e99d7a-d238-482f-bdc6-c4fef137688d')
    api_info = {'api_key': 'f9c39278a5c76d3747252975848b6c600b1e683f', 'api_route':'https://leakcheck.net/api/'}
    if (not api_info):
        return []
    else:
        key = api_info['api_key']
        #key = api_info.api_key
        url = api_info['api_route']
        #url = api_info.api_route
        if (query_type==1):
            query_type = 'auto'
        elif (query_type==2):
            query_type = 'mass'
        else:
            query_type = 'login'
        data = {'key': key, 'type': query_type, "check": query}
        try:

            req = requests.get(url, params=data, timeout=(10,20))
        except Timeout:
            print('The request timed out')
            return []
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
            return []
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
            return []
        if (req.status_code != 200):
            return []
        res = req.json()
        print(res.get('found'))
        
        try:
            check = res.get('success')
            if (not check):
                return []
            results = res.get('result')
            results = parse_results(results)
        except Exception as e:
            print(e)
            return []
        else:
            return results


def append_leaks(query, query_type, final_mails):
    mails = get_leaks(query,query_type)
    
    if(mails):
            final_mails.extend(mails)
            '''
            mail_thread = threading.Thread(
                target=push_mails_to_db, args=(mails,))
            
            mail_thread.start()
            '''

