import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from search.darkbot.common.get_ghostproject_data import get_ghost_data
from search.darkbot.search_engine import search_engine as s
from search.models import IndexEmail, SearchLog
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

# Today
import concurrent.futures
from search import tasks
from search.api.views import leakCheck, getRecordsFromDB, parseLeakCheckResponse, parseDbResponse, mergeResponse


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
    obj = {}
    obj['wildcard'] = 'false'
    obj['regex'] = 'false'
    if request.method == 'POST':

        search_info = request.POST.get('search')
        search_type = request.POST.get('category')
        user = request.user
        search_log = SearchLog(user=user, type=type, search_term=search_info)
        search_log.save()

        start_time = time.time()
        obj['query'] = search_info
        if search_type == "1":
            obj['type'] = 'email'
        elif search_type == "2":
            obj['type'] = 'username'
        elif search_type == "3":
            obj['type'] = 'pass_email'
        elif search_type == "4":
            obj['type'] = 'domain'

        with concurrent.futures.ThreadPoolExecutor() as executor:
            t1 = executor.submit(leakCheck, obj)
            t2 = executor.submit(getRecordsFromDB, obj)
            r1 = t1.result()
            t3 = executor.submit(parseLeakCheckResponse, r1)
            r2 = t2.result()
            t4 = executor.submit(parseDbResponse, r2)
            objr = {}
            objr['res1'] = t4.result()
            objr['res2'] = t3.result()
            t7 = executor.submit(mergeResponse, objr)
            final = t7.result()
            tasks.saveData.delay(final)
            search_duration = time.time() - start_time
            search_duration = int(search_duration)
            if search_type in  ["3","4"] :
                obj['type'] = "email"
            if len(final) > 0:
                mydict = {'mydocuments': final, 'length': len(final),
                          'duration': search_duration, 'type': obj['type']}
            else:
                mydict = {'mydocuments': None, 'length': len(final),
                          'duration': search_duration, 'type': obj['type']}
            a = "search/results.html"

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