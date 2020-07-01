from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from search.models import MonitorEmail,CurrentStatus, IndexEmail, GlobalVar
from search.darkbot.common.get_ghostproject_data import get_ghost_data
#from search.darkbot.haveibeenpwnedApi import HaveIBeenPwned
from search.darkbot.pwnedorNot_new import HaveIBeenPwned
from search.darkbot.myspaceApi import MySpacX_pass_mail
from gatherdumps.models import CardCvv, CardDump, Email_passwords
from django.core.mail import send_mail
from accounts.script import sendmail
from search.api import views
import json


def continuousMonitor():
    globalvars = GlobalVar.objects.filter(id=1)[0]
    breaker = globalvars.emailmonitoring
    while True:
        if breaker:
            print('Live monitoring is turn off completely')
            break
        emails = MonitorEmail.objects.all()
        for each in emails:
            g = GlobalVar.objects.filter(id=1)[0]
            print(g)
            breaker = g.emailmonitoring
            if breaker:
                break
            obj = {}
            obj['type'] = 'email'
            obj['query'] = each
            obj['wildcard'] = 'false'
            obj['regex'] = 'false'
            cleanPass = views.leakCheck(obj)
            print('cleanpass')
            cleanPass = views.parseLeakCheckResponse(cleanPass)
            # print(cleanPass)
            db = views.getRecordsFromDB(obj)
            db = views.parseDbResponse(db)
            o = {}
            o['res1'] = db
            o['res2'] = cleanPass
            newcleanpasswords = views.mergeResponse(o)
            # newcleanpasswords = getPasswordByUsername(each.email)
            newbreaches = checkEmailBreaches(each.email)
            # newbreaches = json.loads(json.dumps(newbreaches['breaches']))
            pastes = pasteSearch(each.email)
            new_no_of_paste = len(pastes['pastes'])
            newindexemails = getEmailPresenceOnDarkweb(each)
            # newemailsindb = checkEmailInDB(each)
            email = MonitorEmail.objects.get(email__exact=each.email)
            currentstatus = CurrentStatus.objects.filter(email=email).values()
            currentstatus = list(currentstatus)
            if len(currentstatus) == 0:
                oldcleanpasswords = []
                oldbreaches = []
                old_no_of_paste = 0
                oldindexemails = []
                # oldemailsindb = []
            else:
                if 'breaches' in currentstatus[0]:
                    oldbreaches = currentstatus[0]['breaches']
                    oldbreaches = json.loads(oldbreaches)
                else:
                    oldbreaches = []
                if 'ghostfrpasswords' in currentstatus[0]:
                    oldcleanpasswords= currentstatus[0]['ghostfrpasswords']
                    oldcleanpasswords = json.loads(oldcleanpasswords)
                else:
                    oldcleanpasswords = []
                if 'no_of_paste' in currentstatus[0]:
                    old_no_of_paste = currentstatus[0]['no_of_paste']
                else:
                    old_no_of_paste = 0
                if 'indexemails' in currentstatus[0]:
                    oldindexemails = currentstatus[0]['indexemails']
                    oldindexemails = json.loads(oldindexemails)
                else:
                    oldindexemails = []
                # if 'oldemailsindb' in currentstatus[0]:
                #     oldemailsindb = currentstatus[0]['emailsindb']
                #     oldemailsindb = json.loads(oldemailsindb)
                # else:
                #     oldemailsindb = []
            if newcleanpasswords == oldcleanpasswords:
                pass
            else:
                if len(oldcleanpasswords) > len(newcleanpasswords):
                    result = all(elem in oldcleanpasswords for elem in newcleanpasswords)
                    if result:
                        pass
                    else:
                        sendMail(each.email,found_passwords=newcleanpasswords,subject="New Password leak is found")
                        CurrentStatus.objects.filter(email=email).update(ghostfrpasswords=newcleanpasswords)
                        print('Updated successfully in ghostfr')
                else:
                    sendMail(each.email, found_passwords=newcleanpasswords, subject="New Password leak is found")
                    print('For sure, Notify the respective user')
                    CurrentStatus.objects.filter(email=email).update(ghostfrpasswords=newcleanpasswords)
                    print('Updated successfully in ghost fr')


            if newbreaches == oldbreaches:
                print("yes we are same breaches")
            else:
                if len(oldbreaches) > len(newbreaches):
                    result = all(elem in oldbreaches for elem in newbreaches)
                    if result:
                        pass
                    else:
                        print('For sure, Notify the respective user')
                        CurrentStatus.objects.filter(email=email).update(breaches=newbreaches)
                        print('Updated successfully in breaches')
                        sendMail(each.email, found_breaches=newbreaches,subject="New Breach is found")
                else:
                    print('For sure, Notify the respective user')
                    CurrentStatus.objects.filter(email=email).update(breaches=newbreaches)
                    print('Updated successfully in breaches 2')
                    sendMail(each.email, found_breaches=newbreaches,subject="New breach is found")
            if new_no_of_paste == old_no_of_paste:
                pass
            elif new_no_of_paste > old_no_of_paste:
                sendMail(each.email, found_pastes=new_no_of_paste, subject="New Paste is found including your info")
                CurrentStatus.objects.filter(email=email).update(no_of_paste=new_no_of_paste)
                print('Updated successfully in pastes')
            else:
                pass
            if newindexemails == oldindexemails:
                print('both lists are equals')
            else:
                if len(oldindexemails) > len(newindexemails):
                    result = all(elem in oldindexemails for elem in newindexemails)
                    if result:
                        pass
                    else:
                        sendMail(each.email, found_occurrence_darkweb=newindexemails, subject="Your Email is found on Dark Web")
                        print('For sure, Notify the respective user')
                        CurrentStatus.objects.filter(email=email).update(indexemails=newindexemails)
                        print('Updated successfully in index emails')

                else:
                    sendMail(each.email, found_occurrence_darkweb=newindexemails, subject="Your Email is found on Dark Web")
                    print('For sure, Notify the respective user')
                    CurrentStatus.objects.filter(email=email).update(indexemails=newindexemails)
                    print('Updated successfully in index emails 2')

            # if newemailsindb == oldemailsindb:
            #     pass
            # else:
            #     if len(oldemailsindb) > len(newemailsindb):
            #         result = all(elem in oldemailsindb for elem in newemailsindb)
            #         if result:
            #             pass
            #         else:
            #             print('Notify the respective user')
            #             CurrentStatus.objects.filter(email=email).update(emailsindb=newemailsindb)
            #             print('Updated successfully emailindb')
            #     else:
            #         print('For sure, Notify the respective user')
            #         CurrentStatus.objects.filter(email=email).update(emailsindb=newemailsindb)
            #         print('Updated successfully emailsindb2')





def startMonitor(b):
    print("i have been called")
    GlobalVar.objects.filter(id=1).update(emailmonitoring=b)
    # global breaker
    # breaker = b
    # print(breaker)
    emails = MonitorEmail.objects.all().count()
    if emails == 0:
        print('NO emails to monitor')
        continuousMonitor()
    else:
        print(emails)
        continuousMonitor()


def getPasswordByUsername(email):
    print('yes i am here')
    final_mails = get_ghost_data(email, 1)
    return final_mails


def checkEmailBreaches(email):
    driver = HaveIBeenPwned()
    try:
        driver.search_by_email(email)
        breaches = driver.retrieve_breaches()
    except Exception as e:
        driver.close_driver()
    else:
        driver.close_driver()
        breaches = breaches["breaches"]
        for each in breaches:
            if each["company"][-1] == ":":
                each["company"] = each["company"][:-1]
        print("breaches method")
        # print(breaches)
        return breaches


def pasteSearch(email):
    driver = HaveIBeenPwned()
    try:
        driver.search_by_email(email)
        pastes = driver.retrieve_pastes()
    except Exception as e:
        driver.close_driver()
    else:
        driver.close_driver()
        return pastes



def getEmailsByPassword(email):
    driver = MySpacX_pass_mail()
    response_data = None
    try:
        driver.create_driver()
        response_data = driver.retrieve_emails(email)
    except Exception as e:
        driver.close_driver()
        response_data = None
    driver.close_driver()
    try:
        data_from_db = Email_passwords.objects.filter(password__iexact=email).values('email')
    except Exception as e:
        print("exception")
        data_from_db = None

    if response_data:
        total_results = response_data['total_results']
        documents = response_data['documents']
    else:
        total_results = 0
        documents = None
    if data_from_db:
        # print(data_from_db)
        if total_results:
            total_results = int(total_results) + data_from_db.count()
        else:
            total_results = data_from_db.count()
        if documents:
            for x in data_from_db:
                documents.append(x['email'])
        else:
            documents = []
            for x in data_from_db:
                documents.append(x['email'])
    return documents

def getEmailPresenceOnDarkweb(email):
    mylist = IndexEmail.objects.filter(email__iexact=email).values()
    mylist = list(mylist)
    return mylist

def checkEmailInDB(email):
    emails = Email_passwords.objects.filter(email__iexact=email).values()
    emails = list(emails)
    return emails


def sendMail(email, subject='SOC ALERT',found_passwords='', found_breaches='', found_pastes='', found_occurrence_darkweb=''):
    subject = subject
    from_email = sendmail.EMAIL_HOST_USER
    to_list = ['daudahmed870@gmail.com']
    context = {
        'email': email,
        'passwords': found_passwords,
        'breaches': found_breaches,
        'pastes': found_pastes,
        'dboccurence': found_occurrence_darkweb,
    }
    html_message = render_to_string('monitoring_email.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, to_list, html_message=html_message)
    print(f'Respective {email} is notified')
