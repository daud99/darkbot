from search.darkbot import ghostproject_vip as ghost
from gatherdumps.models import CardCvv, CardDump, Email_passwords
from search.darkbot.common.leakcheck_api import append_leaks, get_leaks
import threading
import time
import re
import multiprocessing
       
def passwords_from_db(search_info, check):
    final_mails = []
    try:
        if check==1:

            # data_from_db = Email_passwords.objects.filter(email__regex='[a-z]+')
        #     data_from_db = Email_passwords.objects.mongo_aggregate([
        #     {
        #         '$match': {
        #             'email': 'daudahmed870@gmail.com'
        #         }
        #     },
        # ])
            regx = re.compile("d?", re.IGNORECASE)
            data_from_db = Email_passwords.objects.mongo_find({
                'email': {'$regex': "e{2}"}
            })
            data_from_db = list(data_from_db)
            print("below is the data")
            print(data_from_db)
            for each in data_from_db:
                print(each)
        elif check==2:
            data_from_db = Email_passwords.objects.filter(ep__icontains={'email': search_info}).values()
        if(data_from_db.count()>0):
            '''
            for x in data_from_db:
                
                #if [x.email, x.password] not in f_mails:
                temp_list = (x.email, x.password)
        
                final_mails.append(temp_list)
            '''
            print('Also found some results from db')
            final_mails.extend(data_from_db)
    except Exception as e:
            print(e)
            print('Exception at db after gp section')
    return final_mails

def append_db_data(search_info, check, final_mails):
    mails = passwords_from_db(search_info,check)
    if(len(mails)>0):
        final_mails.extend(mails)
        
def get_ghost_data(search_info, check):
    '''
    gp = ghost.GhostProjectCrawler()
    '''
    #multiprocessing stuff
    
    manager = multiprocessing.Manager()
    final_mails = manager.list()
    
    #final_mails = []
    '''
    try: 
        breached_list = gp.retrieveData(search_info)
        gp.close_driver()
        end_time = time.time() + 40
        
        
        if (len(breached_list)>0):
            #print(breached_list)
            
            for x in breached_list:
                row_split = x.split(':')
                row_split_0 = row_split[0].strip()
                row_split_1 = row_split[1].strip()
                move_email_pass_to_db(row_split_0, row_split_1)
                row_split.clear()
                row_split = [row_split_0,row_split_1]
                final_mails.append(row_split.copy())
        gp.close_driver()
    except Exception as e:
        print(e)
        gp.close_driver()
        print('Exception at gp section')
    gp.close_driver()
    '''
    #Multiprocessing stuff
    
    leakcheck_process = multiprocessing.Process(
        target=append_leaks, args=(search_info,check,final_mails,))
    db_passwords_process = multiprocessing.Process(
        target=append_db_data, args=(search_info,check,final_mails,))

    leakcheck_process.start()
    db_passwords_process.start()

    #wait
    leakcheck_process.join()
    db_passwords_process.join()
    final_mails = list(set(final_mails))
    '''
    leakcheck_data = get_leaks(search_info, check)
    final_mails.extend(leakcheck_data)
    data_from_db = passwords_from_db(search_info, check)
    final_mails.extend(data_from_db)
    print('Resturning email passwords')
    final_mails = list(set(final_mails))
    '''
    return final_mails
    