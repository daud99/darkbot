# print("current module is: " + __name__)
import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from search.darkbot.common.get_ghostproject_data import get_ghost_data
from search.darkbot.search_engine import search_engine as s
from search.models import IndexEmail, SearchLog, MonitorEmail, CurrentStatus
from accounts.models import User
from search.darkbot.haveibeenpwnedApi import HaveIBeenPwned
from search.darkbot.pwnedorNot_new import HaveIBeenPwned as HIBPwned
import time
from iso3166 import countries
from gatherdumps.models import CardCvv, CardDump, Email_passwords
from search.darkbot.myspaceApi import MySpacX_pass_mail
import json
#from search.tasks import push_mails_to_db
search_term = None
breaches = None


def user_is_loggedin(func):
    def wrapper(*args):
        if not args[0].user.is_authenticated:
            messages.error(args[0], 'You are not Logged In')
            return HttpResponseRedirect('/login')
        else:
            return func(args[0])

    return wrapper


# Create your views here.

@user_is_loggedin
def search(request):
    final_list = []
    a = "search/search.html"
    mydict = {}
    if request.method == 'POST':

        search_info = request.POST.get('search')
        search_type = request.POST.get('category')
        type = getSearchType(search_type)
        user = request.user
        search_log = SearchLog(user=user, type=type, search_term=search_info)
        search_log.save()
        print('search info : ' + search_info)
        # print('search type : ' + search_type)
        if search_type == "1":
            #disconnect()
            start_time = time.time()
            mylist = s(search_info)
            search_duration = time.time() - start_time
            search_duration = int(search_duration)
            if len(mylist) > 0:
                mydict = {'mydocuments': mylist, 'length': len(mylist),
                          'duration': search_duration}
            else:
                mydict = {'mydocuments': None, 'length': len(mylist),
                          'duration': search_duration}
            a = "search/results.html"

        elif search_type == "2":
            email_search_subtype = request.POST.get('email-search-what')
            email_search_type = request.POST.get('email-search-type')

            if (email_search_subtype == "1" and email_search_type == "1"):

                start_time = time.time()
                final_list = IndexEmail.objects.filter(email__iexact=search_info)

                # l = crawl.emails_with_channel()
                # for e in l:
                #     print('final list')
                #     print(e)
                #     if search_info == e[0]:
                #         final_list.append(e)
                '''for each in final_list:
                    print(each)'''
                # print("length of result is : ", len(final_list))
                search_duration = time.time() - start_time
                search_duration = int(search_duration)
                if len(final_list) > 0:
                    mydict = {'documents': final_list, 'length': len(final_list),
                              'duration': search_duration}
                else:
                    mydict = {'documents': None, 'length': len(final_list),
                              'duration': search_duration}
                a = "search/results.html"

            elif (email_search_subtype == "2" and email_search_type == "1"):
                a = "search/breach_result.html"
                final_mails = get_ghost_data(search_info, 1)
                if len(final_mails) > 0:
                    mydict = {'documents': final_mails}

                else:
                    mydict = {'documents': None}
            elif (email_search_subtype == "3" and email_search_type == "1"):
                #driver = HaveIBeenPwned()
                driver = HIBPwned()
                a = "search/pwned_breach.html"
                try:
                    start_time = time.time()
                    driver.search_by_email(search_info)
                    breaches = driver.retrieve_breaches()
                    search_duration = time.time() - start_time
                    search_duration = int(search_duration)

                    # print(breaches)
                    mydict = breaches.copy()
                    mydict['duration'] = search_duration
                except Exception as e:
                
                    driver.close_driver()

                else:
                    driver.close_driver()
                    request.session['breach_result'] = json.dumps(mydict)
                    return redirect('/search/pwned?page=1')

            elif (email_search_subtype == "4" and email_search_type == "1"):
                #driver = HaveIBeenPwned()
                driver = HIBPwned()
                a = "search/pwned_paste.html"
                try:
                    start_time = time.time()

                    driver.search_by_email(search_info)
                    pastes = driver.retrieve_pastes()
                    search_duration = time.time() - start_time
                    search_duration = int(search_duration)
                    mydict = pastes.copy()
                    mydict['duration'] = search_duration
                except Exception as e:
                    driver.close_driver()
                else:
                    driver.close_driver()
                    request.session['paste_result'] = json.dumps(mydict)
                    return redirect('/search/pastes?page=1')
                    # print(pastes)


            elif (email_search_subtype == "1" and email_search_type == "2"):
                '''
                driver = MySpacX_pass_mail()
                '''
                start_time = time.time()
                response_data = None
                a = "search/pass_mail.html"
                '''
                try:
                    driver.create_driver()
                    response_data = driver.retrieve_emails(search_info)
                except Exception as e:
                    driver.close_driver()
                    response_data = None
                driver.close_driver()
                '''
                try:
                    data_from_db = Email_passwords.objects.filter(password__iexact=search_info).values('email')
                except Exception as e:
                    print("exception")
                    data_from_db = None
                end_time = time.time() - start_time

                if response_data:
                    total_results = response_data['total_results']
                    documents = response_data['documents']
                else:
                    total_results = 0
                    documents = []
                if data_from_db:
                    print(data_from_db)
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

                mydict = {}
                mydict['total_results'] = total_results
                mydict['documents'] = documents
                mydict['duration'] = end_time
                mydict['passw'] = search_info
                request.session['clean_mails'] = json.dumps(mydict)
                return redirect('/search/emails?page=1')
            elif (email_search_subtype == "2" and email_search_type == "2"):
                
                messages.warning(request,"Don't Go there, try searching by cleanpass")
                return redirect('/search')
                '''
                driver = MySpacX_pass_mail()
                start_time = time.time()
                response_data = None
                a = "search/pass_mail.html"
                try:
                    driver.create_driver()
                    response_data = driver.retrieve_emails_by_hash(search_info)
                except Exception as e:
                    driver.close_driver()
                else:
                    driver.close_driver()
                    end_time = time.time() - start_time
                    mydict = response_data.copy()
                    mydict['duration'] = end_time
                    mydict['passw'] = search_info
                '''
            elif (email_search_subtype == "1" and email_search_type == "3"):
                a = "search/breach_result.html"
                final_mails = get_ghost_data(search_info, 2)
                if len(final_mails) > 0:
                    mydict = {'documents': final_mails}
                else:
                    mydict = {'documents': None}
            elif (email_search_subtype == "2" and email_search_type == "3"):

                start_time = time.time()
                final_list = IndexEmail.objects.filter(email__istartswith=search_info)

                # l = crawl.emails_with_channel()
                # for e in l:
                #     print('final list')
                #     print(e)
                #     if search_info == e[0]:
                #         final_list.append(e)
                '''for each in final_list:
                    print(each)'''
                # print("length of result is : ", len(final_list))
                search_duration = time.time() - start_time
                search_duration = int(search_duration)
                if len(final_list) > 0:
                    mydict = {'documents': final_list, 'length': len(final_list),
                              'duration': search_duration}
                else:
                    mydict = {'documents': None, 'length': len(final_list),
                              'duration': search_duration}
                a = "search/results.html"

        elif search_type == "3":
            bank_search_type = request.POST.get('option-dp')
            bank_search_category = request.POST.get('type-dp')

            if bank_search_category == "1":
                request.session['dump_checkpoint'] = True
                request.session['dump_query'] = search_info
                request.session['dump_search_type'] = bank_search_type
                start_time = time.time()

                return redirect('/search/dumps?page=1')
                # a= "search/dumps_result.html"
            if bank_search_category == "2":
                request.session['cvv_checkpoint'] = True
                request.session['cvv_query'] = search_info
                request.session['cvv_search_type'] = bank_search_type
                return redirect('/search/cvv?page=1')
                # return get_cvv(request)
                # a= "search/cvvs_results.html"
    if request.user.is_superuser:
        mydict["base_template"] = 'adminpanel/base.html'
    else:
        if request.method == 'POST':
            u = User.objects.get(pk=request.user.id)
            u.number_of_queries = request.user.number_of_queries - 1
            u.save()
        mydict["base_template"] = 'userdashboard/base.html'
    return render(request, a, context=mydict)


@user_is_loggedin
def search_result(request):
    mydict = {}
    if request.user.is_superuser:
        mydict["base_template"] = 'adminpanel/base.html'
    else:
        mydict["base_template"] = 'userdashboard/base.html'
    return render(request, "search/results.html", context=mydict)


@user_is_loggedin
def load(request):
    render(request, "search/breach_result.html")
    # print('loaded')
    return render(request, "search/load.html")


@user_is_loggedin
def breach_result(request):
    mydict = {}
    if request.user.is_superuser:
        mydict["base_template"] = 'adminpanel/base.html'
    else:
        mydict["base_template"] = 'userdashboard/base.html'
    return render(request, "search/breach_result.html", context=mydict)


@user_is_loggedin
def get_pass_email(request):
    if (request.session.get('clean_mails')):
        mydict = json.loads(request.session.get('clean_mails'))
        paginator = Paginator(mydict['documents'], 10)
        page = request.GET.get('page')
        mydict['documents'] = paginator.get_page(page)
        if request.user.is_superuser:
            mydict["base_template"] = 'adminpanel/base.html'
        else:
            mydict["base_template"] = 'userdashboard/base.html'
        return render(request, 'search/pass_mail.html', context=mydict)
    else:
        messages.warning(request, "Something went wrong")
        return redirect('/search')


@user_is_loggedin
def get_paste(request):
    if (request.session.get('paste_result')):
        mydict = json.loads(request.session.get('paste_result'))
        paginator = Paginator(mydict['pastes'], 10)
        page = request.GET.get('page')
        mydict['pastes'] = paginator.get_page(page)
        if request.user.is_superuser:
            mydict["base_template"] = 'adminpanel/base.html'
        else:
            mydict["base_template"] = 'userdashboard/base.html'
        return render(request, 'search/pwned_paste.html', context=mydict)
    else:
        messages.warning(request, "Something went wrong")
        return redirect('/search')


@user_is_loggedin
def get_cvv(request):
    if (request.session.get('cvv_checkpoint')):

        start_time = time.time()
        bank_search_type = request.session.get('cvv_search_type')
        search_info = request.session.get('cvv_query')
        if bank_search_type == "1":
            if (not search_info.isnumeric()):
                messages.warning(request, 'Bin No contains only digits. OK?')
                return redirect('/search')
            elif (len(search_info) != 6):
                messages.warning(request, 'Enter just First 6 digits of Card No')
                return redirect('/search')
            card_cvvs = CardCvv.objects.filter(bin_no__exact=search_info).order_by('-date').all()

        if bank_search_type == "2":
            try:
                country = countries.get(search_info)
            except Exception as e:
                messages.warning(request, 'Please Enter Correct Name')
                mydict = {}
                if request.user.is_superuser:
                    mydict["base_template"] = 'adminpanel/base.html'
                else:
                    mydict["base_template"] = 'userdashboard/base.html'
                return render(request, 'search/search.html')
            else:
                country = country.alpha3
            card_cvvs = CardCvv.objects.filter(country__exact=country).order_by('-date').all()

        if bank_search_type == "3":
            card_cvvs = CardCvv.objects.filter(bank__istartswith=search_info).order_by('-date').all()

        if bank_search_type == "4":
            card_cvvs = CardCvv.objects.filter(base__icontains=search_info).order_by('-date').all()
        if bank_search_type == "5":
            card_cvvs = CardCvv.objects.filter(name__iexact=search_info).order_by('-date').all()
        if bank_search_type == "6":
            card_cvvs = CardCvv.objects.filter(city__iexact=search_info).order_by('-date').all()
        if bank_search_type == "7":
            card_cvvs = CardCvv.objects.filter(zip_no__iexact=search_info).order_by('-date').all()
        search_duration = time.time() - start_time
        search_duration = int(search_duration)

        mydict = {'total_results': card_cvvs.count(), 'dumps': card_cvvs, 'duration': search_duration}
        cvv = mydict.get('dumps')
        paginator = Paginator(cvv, 10)
        page = request.GET.get('page')
        dumps = paginator.get_page(page)
        # mydict['total_results'] = cvv_dict.get('total_results')
        mydict['dumps'] = dumps
        # mydict['duration'] = cvv_dict.get('duration')
        if request.user.is_superuser:
            mydict["base_template"] = 'adminpanel/base.html'
        else:
            mydict["base_template"] = 'userdashboard/base.html'
        return render(request, 'search/cvvs_results.html', context=mydict)


@user_is_loggedin
def get_dump(request):
    if (request.session.get('dump_checkpoint')):
        start_time = time.time()
        bank_search_type = request.session.get('dump_search_type')
        search_info = request.session.get('dump_query')
        if bank_search_type == "1":
            if (not search_info.isnumeric()):
                messages.warning(request, 'Bin No contains only digits. OK?')
                return redirect('/search')
            elif (len(search_info) != 6):
                messages.warning(request, 'Enter just First 6 digits of Card No')
                return redirect('/search')
            card_dumps = CardDump.objects.filter(bin_no__exact=search_info).order_by('-date').all()
            # print(card_dumps[0].date)
        if bank_search_type == "2":
            try:
                country = countries.get(search_info)
            except Exception as e:
                messages.warning(request, 'Please Enter Correct Name')
                mydict = {}
                if request.user.is_superuser:
                    mydict["base_template"] = 'adminpanel/base.html'
                else:
                    mydict["base_template"] = 'userdashboard/base.html'
                return render(request, 'search/search.html', context=mydict)
            else:
                country = country.alpha3
            card_dumps = CardDump.objects.filter(country__exact=country).order_by('-date').all()
            # print(card_dumps[0].date)
        if bank_search_type == "3":
            card_dumps = CardDump.objects.filter(bank__istartswith=search_info).order_by('-date').all()
            # print(card_dumps[0].date)
        if bank_search_type == "4":
            card_dumps = CardDump.objects.filter(base__icontains=search_info).order_by('-date').all()
            # print(card_dumps[0].date)
        search_duration = time.time() - start_time
        search_duration = int(search_duration)

        mydict = {'total_results': card_dumps.count(), 'dumps': card_dumps, 'duration': search_duration}

        dump = mydict.get('dumps')
        paginator = Paginator(dump, 10)
        page = request.GET.get('page')
        dumps = paginator.get_page(page)
        # mydict['total_results'] = dump_dict.get('total_results')
        mydict['dumps'] = dumps
        # mydict['duration'] = dump_dict.get('duration')
        if request.user.is_superuser:
            mydict["base_template"] = 'adminpanel/base.html'
        else:
            mydict["base_template"] = 'userdashboard/base.html'
        return render(request, 'search/dumps_result.html', context=mydict)


def pwned_breach(request):
    if (request.session.get('breach_result')):
        mydict = json.loads(request.session.get('breach_result'))
        paginator = Paginator(mydict['breaches'], 10)
        page = request.GET.get('page')
        mydict['breaches'] = paginator.get_page(page)
        if request.user.is_superuser:
            mydict["base_template"] = 'adminpanel/base.html'
        else:
            mydict["base_template"] = 'userdashboard/base.html'
        return render(request, 'search/pwned_breach.html', context=mydict)
    else:
        messages.warning(request, "Something went wrong")
        return redirect('/search')


def getSearchType(index):
    searchTypes = {1: "Trace Any Info", 2: "Trace Email", 3: "Trace Bank Data"}
    return searchTypes[int(index)]#print("current module is: " + __name__)

def vv(request):
    emails = MonitorEmail.objects.filter(fileid=22)

    leakedpasswords = []
    breaches = []
    pastes = []
    emailforbreaches = {}
    indexemails = []
    starttime = 0
    for email in emails:
        if starttime == 0 or starttime > email.start_date:
            starttime = email.start_date

        currentstatus = CurrentStatus.objects.filter(email=email).values()
        currentstatus = list(currentstatus)
        mypasses = json.loads(currentstatus[0]['ghostfrpasswords'])
        mybreaches = json.loads(currentstatus[0]['breaches'])
        mybreacheslen = len(mybreaches)
        if not mybreacheslen == 0:
            print(mybreacheslen)
            keyslist = list(emailforbreaches.keys())
            if 1 in keyslist:
                indi = emailforbreaches["previouslen"]
                emailforbreaches[indi] = email
                emailforbreaches["previouslen"] = mybreacheslen + indi
            else:
                emailforbreaches[1] = email
                emailforbreaches["previouslen"] = mybreacheslen + 1
        mypaste = currentstatus[0]['no_of_paste']
        myindexemails = json.loads(currentstatus[0]['indexemails'])

        p = [email, mypaste]
        leakedpasswords.extend(mypasses)
        breaches.extend(mybreaches)
        pastes.append(p)
        indexemails.extend(myindexemails)

    # charts = Charts.objects.filter(chart_file=fileid)[:3]
    # for (index,chart) in enumerate(charts):
    #     print("index ",index)
    #     if "overview" in chart.chart_name:
    #         chart1 = "img/report/" + str(chart.chart_name)
    #     if "password" in chart.chart_name:
    #         chart2 = "img/report/" + str(chart.chart_name)
    #     if "criticality" in chart.chart_name:
    #         chart3 = "img/report/" + str(chart.chart_name)
    #
    # context['chart1'] = chart1
    # context['chart2'] = chart2
    # context['chart3'] = chart3
    context = {}
    context['leakedpasswords'] = leakedpasswords
    context['breaches'] = breaches
    context['pastes'] = pastes
    context['emailforbreaches'] = emailforbreaches
    context['indexemails'] = indexemails
    context['endtime'] = str(datetime.datetime.now())
    context['starttime'] = str(starttime)
    return render(request, 'search/pdf.html', context=context)