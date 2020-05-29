
from jinja2 import Environment, FileSystemLoader
from search.api import misc
from weasyprint import HTML
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from search.darkbot.haveibeenpwnedApi import getBreach, getPaste
from search.darkbot.pwnedorNot_new import HaveIBeenPwned as HIBPwned
import re
import concurrent.futures
from rest_framework import status
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from search.api.serializers import IndexEmailSerializer, CardCvvSerializer, CardDumpSerializer, Email_passwordsSerializer, MonitorDomainSerializer, ReportSerializer
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseRedirect
from gatherdumps.models import CardCvv, CardDump, Email_passwords
from search.darkbot.common.get_ghostproject_data import get_ghost_data
from search.darkbot.pwnedorNot_new import HaveIBeenPwned
from search.darkbot.search_engine import search_engine as s
from search.darkbot import monitor, domain_monitoring
from search.models import MonitorEmail, CurrentStatus, Charts, MonitorDomain, IndexEmail, ApiSearchLog, Report
from django_weasyprint import WeasyTemplateResponseMixin
from dark_bot import settings
from adminpanel import views
import time
import datetime
import json
from selenium import webdriver
from functools import partial
import io
import os
from django.http import FileResponse
import requests
from requests.exceptions import Timeout, HTTPError
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from search import tasks

# global lists
filelist = []
domainlist = []


class OverRideDefaultPagination(PageNumberPagination):
    page_size = 10



class EmailListView(generics.ListAPIView):
    queryset = IndexEmail.objects.all()
    queryset = IndexEmail.objects.all()
    serializer_class = IndexEmailSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['email']



class CvvSearchBinNo(generics.ListAPIView):
    queryset = CardCvv.objects.all()
    serializer_class = CardCvvSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['bin_no']


class CvvSearchCountry(generics.ListAPIView):
    queryset = CardCvv.objects.all()
    serializer_class = CardCvvSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['country']


class CvvSearchBankName(generics.ListAPIView):
    queryset = CardCvv.objects.all()
    serializer_class = CardCvvSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['bank']

class CvvSearchOwnerName(generics.ListAPIView):
    queryset = CardCvv.objects.all()
    serializer_class = CardCvvSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name']

class CvvSearchZipNo(generics.ListAPIView):
    queryset = CardCvv.objects.all()
    serializer_class = CardCvvSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['zip_no']

class CvvSearchCity(generics.ListAPIView):
    queryset = CardCvv.objects.all()
    serializer_class = CardCvvSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['city']

class DumpSearchBinNo(generics.ListAPIView):
    queryset = CardDump.objects.all()
    serializer_class = CardDumpSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['bin_no']


class DumpSearchCountry(generics.ListAPIView):
    queryset = CardDump.objects.all()
    serializer_class = CardDumpSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['country']


class DumpSearchBankName(generics.ListAPIView):
    queryset = CardDump.objects.all()
    serializer_class = CardDumpSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['bank']

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def getPasswordByUsername(request):
    search_info = request.data["email"]
    final_mails = get_ghost_data(search_info, 1)
    if len(final_mails) > 0:
        mydict = {'documents': final_mails}
        for each in final_mails:
            print(each)
        # serializer = CleanPasswordSerializer(final_mails, many=True)
        return JsonResponse(final_mails, safe=False)
    else:
        return JsonResponse({"result":"no result found"}, safe=False)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def checkEmailBreaches(request):
    search_info = request.data["email"]
    driver = HaveIBeenPwned()
    try:
        driver.search_by_email(search_info)
        breaches = driver.retrieve_breaches()
    except Exception as e:
        driver.close_driver()
    else:
        driver.close_driver()
        return JsonResponse(breaches, safe=False)

def newCheckEmailBreaches(email):

    driver = HIBPwned()
    try:
        driver.search_by_email(email)
        breaches = driver.retrieve_breaches()
    except Exception as e:
        driver.close_driver()
    else:
        driver.close_driver()
        return JsonResponse(breaches, safe=False)

def newCheckPastes(email):
    driver = HIBPwned()
    a = "search/pwned_paste.html"
    try:
        driver.search_by_email(email)
        pastes = driver.retrieve_pastes()
    except Exception as e:
        driver.close_driver()
    else:
        driver.close_driver()
        return JsonResponse(pastes, safe=False)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def searchEngine(request):
    search_info = request.data["email"]
    #disconnect()
    mylist = s(search_info)
    return JsonResponse(mylist, safe=False)


def newSearchEngine(keyword):
    mylist = s(keyword)
    return JsonResponse(mylist, safe=False)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def pasteSearch(request):
    search_info = request.data["email"]
    driver = HaveIBeenPwned()
    try:
        driver.search_by_email(search_info)
        pastes = driver.retrieve_pastes()
    except Exception as e:
        driver.close_driver()
    else:
        driver.close_driver()
        return JsonResponse(pastes, safe=False)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def deleteDomain(request):
    id = request.data['id']
    userid = 0
    if 'userid' in request.data:
        userid = request.data['userid']
        print("userid id ", userid)
    print("id is ", id)
    try:
        if userid != 0:
            domain = MonitorDomain.objects.get(id=id, userid=userid)
        else:
            domain = MonitorDomain.objects.get(id=id)
    except MonitorDomain.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)
    data = ''
    if request.method == 'POST':
        operation = domain.delete()
        if operation:
            data = 'deleted successfully'
            print('deleted')
        else:
            data = 'Deletion fail'
    return JsonResponse({'data': data}, safe=False)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def getEmailsByPassword(request):
    search_info = request.data["email"]
    response_data = None
    try:
        data_from_db = Email_passwords.objects.filter(password__iexact=search_info).values('email')
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
        #print(data_from_db)
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
    return JsonResponse(documents, safe=False)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def getEmailsByHash(request):
    search_info = request.data["sha1"]
    response_data = None
    return JsonResponse(response_data, safe=False)

def saveReportInstance(typee ,userid, fileid):
    try:
        report = Report(userid=userid, fileid=fileid, report_type=typee)
        report.save()
    except Exception as e:
        print(e)
        print('exception at saving report instance is above')

def updateReportInstance(fileid, status, time):
    try:
        Report.objects.filter(fileid=fileid).update(status=status, create_date=time)
    except Exception as e:
        print(e)
        print('exception in updating report instance')

class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, format=None):
        starttime = str(misc.formatDate(datetime.datetime.now()))
        emails = request.data["emails"]
        print(emails)
        #emails = emails.read()
        #emails = str(emails, 'utf-8')
        userid = request.data["userid"]
        fileid = request.data["fileid"]
        print('fileid', fileid)
        print('userid', userid)
        saveReportInstance("Current Emails Exposure", userid, fileid+".pdf")
        uploaderemail = request.data["email"]
        tasks.processUploadEmailFileCreateReport.delay(emails, userid, fileid, uploaderemail, starttime)
        return Response(status=200)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def initializeSingleDomainReport(request):
    starttime = str(misc.formatDate(datetime.datetime.now()))
    domain = request.data["domain"]
    userid = request.data["userid"]
    now = datetime.datetime.now()
    pdf_filename = str(now) + ".pdf"
    saveReportInstance("Current " + domain + " Exposure", userid, pdf_filename)
    print('the rrrrrrreport generation should start')
    tasks.processDomainCreateReport.delay(domain, userid, pdf_filename, starttime)
    return Response(status=200)


def celerySingleDomainReport(domain, userid, pdf_filename, starttime):
    print("executed single domain report creation")
    context = {}
    if userid != "superuser":
        r = MonitorDomain.objects.filter(asset_verify__exact=True, domain__exact=domain, userid__exact=userid).count()
        d = MonitorDomain.objects.filter(asset_verify__exact=True, domain__exact=domain, userid__exact=userid).values()
    else:
        r = MonitorDomain.objects.filter(asset_verify__exact=True, domain__exact=domain).count()
        d = MonitorDomain.objects.filter(asset_verify__exact=True, domain__exact=domain).values()
    if r == 0:
        updateReportInstance(pdf_filename, "failure", datetime.datetime.now())
        return
    print(d)
    d = list(d)
    senderemail = d[0]['support_email']
    print(senderemail)
    emails = domain_monitoring.find_emails_over_domain(domain)
    indexedemails = domain_monitoring.find_emails_over_domain_in_indexemails(domain)
    leakedpasswords = []
    indexemails = []
    for email in emails:
        p = domain_monitoring.get_passwords_by_email_for_report(email)
        leakedpasswords.extend(p)

    for email in indexedemails:
        indexemails.extend(domain_monitoring.get_darknet_occurrences_for_report(email))

    context['leakedpasswords'] = leakedpasswords
    context['indexemails'] = indexemails
    context['endtime'] = str(misc.formatDate(datetime.datetime.now()))
    context['starttime'] = starttime
    stylesheet = misc.getPath(settings.BASE_DIR, "static/css/pdf.css")
    path = misc.getPath(settings.BASE_DIR, "search/templates/search")
    dest = misc.getPath(settings.BASE_DIR, "reports/" + pdf_filename)
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template("domainpdf.html")
    html_out = template.render(context)
    print(__file__)
    HTML(string=html_out, base_url=__file__).write_pdf(dest, stylesheets=[stylesheet])
    updateReportInstance(pdf_filename, "success", datetime.datetime.now())
    views.sendReportCompletionEmail(senderemail)



def celeryEmailReport(emails, userid, fileid, uploaderemail, starttime):
    emails = emails.replace("\n", "")
    emails = emails.replace(" ", "\r\n")
    emails = emails.split('\r\n')

    print('userid = ', userid)
    print('fileid = ', fileid)
    print('emails below')
    print(emails)
    for each in emails:
        print(each)
    for (index, each) in enumerate(emails):
        try:
            if '@' in each:
                currentEmail = saveMonitorEmail(each, userid, fileid)
                saveCurrentStatus(each, currentEmail, fileid)
        except Exception as e:
            print('exception')

    # return Response(status=200)
    # return HttpResponseRedirect('/api/trace/print/' + fileid)

    emails = MonitorEmail.objects.filter(fileid=fileid)
    context = {}
    leakedpasswords = []
    breaches = []
    pastes = []
    emailforbreaches = {}
    indexemails = []
    previouslen = 0
    for email in emails:
        currentstatus = CurrentStatus.objects.filter(email=email).values()
        currentstatus = list(currentstatus)
        mypasses = json.loads(currentstatus[0]['ghostfrpasswords'])
        mybreaches = json.loads(currentstatus[0]['breaches'])
        mybreacheslen = len(mybreaches)
        if not mybreacheslen == 0:
            print(mybreacheslen)
            keyslist = list(emailforbreaches.keys())
            if 1 in keyslist:
                indi = previouslen
                emailforbreaches[indi] = email
                previouslen = mybreacheslen + indi
            else:
                emailforbreaches[1] = email
                previouslen = mybreacheslen + 1
        mypaste = currentstatus[0]['no_of_paste']
        myindexemails = json.loads(currentstatus[0]['indexemails'])

        p = [email, mypaste]
        leakedpasswords.extend(mypasses)
        breaches.extend(mybreaches)
        pastes.append(p)
        indexemails.extend(myindexemails)
    context['leakedpasswords'] = leakedpasswords
    context['breaches'] = breaches
    context['pastes'] = pastes
    context['emailforbreaches'] = emailforbreaches
    context['indexemails'] = indexemails
    context['endtime'] = str(misc.formatDate(datetime.datetime.now()))
    context['starttime'] = starttime
    stylesheet = misc.getPath(settings.BASE_DIR, "static/css/pdf.css")
    path = misc.getPath(settings.BASE_DIR, "search/templates/search")
    dest = misc.getPath(settings.BASE_DIR, "reports/"+fileid+".pdf")
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template("pdf.html")
    html_out = template.render(context)
    print(__file__)
    HTML(string=html_out, base_url=__file__).write_pdf(dest, stylesheets=[stylesheet])
    updateReportInstance(fileid+".pdf", "success", datetime.datetime.now())
    views.sendReportCompletionEmail(uploaderemail)
    # MyModelPrintView.as_view()(request)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def monitorEmails(request):
    print('data received')
    # print(request)
    #print(request.body)
    #print(request.data)
    emails = request.data["emails"].replace(" ", "\r\n")
    userid = request.data["userid"]
    fileid = request.data["fileid"]
    emails = emails.split('\r\n')

    for (index, each) in enumerate(emails):
        try:
            if '@' in each:
               currentEmail = saveMonitorEmail(each, userid, fileid)
               saveCurrentStatus(each, currentEmail)
        except Exception as e:
            print('exception')
            #print(e)

    # print(request.body.get('file'))
    return Response({"success": "success"})

def saveMonitorEmail(email, userid, fileid):
    try:
        currentEmail = MonitorEmail(email=email, userid=userid, fileid=fileid)
        currentEmail.save()
        return currentEmail
    except Exception as e:
        MonitorEmail.objects.filter(email=email).update(userid=userid, fileid=fileid)
        print('exception')
        #print(e)

def saveCurrentStatus(email, currentEmail, fileid=1):
    try:
        print("is not it what it should be",email)
        print(type(email))
        obj = {}
        obj['type'] = 'email'
        obj['query'] = email
        obj['wildcard'] = 'false'
        obj['regex'] = 'false'
        cleanPass = leakCheck(obj)
        print('cleanpass')
        # print(cleanPass)
        cleanPass = parseLeakCheckResponse(cleanPass)
        # print(cleanPass)
        db = getRecordsFromDB(obj)
        db = parseDbResponse(db)
        o = {}
        o['res1'] = db
        o['res2'] = cleanPass
        cleanPass = mergeResponse(o)
        print(cleanPass)
        print("yaha",email)
        breaches = monitor.checkEmailBreaches(email)
        pastes = monitor.pasteSearch(email)
        no_of_paste = len(pastes['pastes'])
        print(no_of_paste)
        indexemails = monitor.getEmailPresenceOnDarkweb(email)
        #print('emailfound ', email)
        emailfound = CurrentStatus.objects.filter(email__email__exact=email, email__fileid__exact=fileid).count()
        #print('emailfound ', emailfound)
        # print("emailfound are ", emailfound)
        if emailfound == 0:
            currentstatus = CurrentStatus(email=currentEmail, ghostfrpasswords=cleanPass, breaches=breaches, no_of_paste=no_of_paste, indexemails=indexemails)
            #currentstatus = CurrentStatus(email=currentEmail, breaches=breaches, no_of_paste=no_of_paste, indexemails=indexemails)
            currentstatus.save()
        else:
            CurrentStatus.objects.filter(email=currentEmail).update(ghostfrpasswords=cleanPass, breaches=breaches, no_of_paste=no_of_paste, indexemails=indexemails)
            #CurrentStatus.objects.filter(email=currentEmail).update( breaches=breaches, no_of_paste=no_of_paste, indexemails=indexemails)
    except Exception as e:
        print('exception')
        print(e)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def registerDomains(request):
    #print(request.data["domains"])
    domains = request.data["domains"]
    userid = request.data["userid"]
    email = request.data["email"]
    domains = domains.split(" ")
    for each in domains:
        try:
            currentdomain = MonitorDomain(domain=each, userid=userid, support_email=email)
            currentdomain.save()
        except Exception as e:
            print('exception')
            #print(e)
    return Response({"success": "success"})


class Pdf(ListView):
    template_name = 'search/pdf.html'

    def get_queryset(self):
        return self.kwargs['file']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        fileid = self.kwargs['file']
        print ("fileid is ", fileid)
        emails = MonitorEmail.objects.filter(fileid=fileid)

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

            p = [email,mypaste]
            leakedpasswords.extend(mypasses)
            breaches.extend(mybreaches)
            pastes.append(p)
            indexemails.extend(myindexemails)
        context['leakedpasswords'] = leakedpasswords
        context['breaches'] = breaches
        context['pastes'] = pastes
        context['emailforbreaches'] = emailforbreaches
        context['indexemails'] = indexemails
        context['endtime'] = str(misc.formatDate(datetime.datetime.now()))
        context['starttime'] = str(misc.formatDate(starttime))
        return context

class TimeDelayMixin(object, ):

    def dispatch(self, request, *args, **kwargs):
        time.sleep(1)
        return super().dispatch(request, *args, **kwargs)

class MyModelPrintView(Pdf, WeasyTemplateResponseMixin):
    pdf_filename = 'tranchulas.pdf'
    # now = datetime.datetime.now()
    # pdf_filename = str(now) + ".pdf"
    # print('i wish i could be last things can get a bit easy then lol')

    def get_queryset(self):
        print("wao", self.kwargs['file'])
        MyModelPrintView.pdf_filename = str(self.kwargs['file']) + ".pdf"
        return self.kwargs['file']


class DomainPdf(ListView):
    template_name = 'search/domainpdf.html'

    def get_queryset(self):
        return self.kwargs['file']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        domain = self.kwargs['file']
        #print ("domain is ",domain)
        r = MonitorDomain.objects.filter(asset_verify__exact=True, domain__exact=domain).count()
        #print("r is ", r)
        if r == 0:
            return context
        emails = domain_monitoring.find_emails_over_domain(domain)
        indexedemails = domain_monitoring.find_emails_over_domain_in_indexemails(domain)
        leakedpasswords = []
        indexemails = []
        starttime = 0
        for email in emails:
            #print("email is ",email)
            starttime = datetime.datetime.now()
            p = domain_monitoring.get_passwords_by_email_for_report(email)
            leakedpasswords.extend(p)

        for email in indexedemails:
            indexemails.extend(domain_monitoring.get_darknet_occurrences_for_report(email))

        context['leakedpasswords'] = leakedpasswords
        context['indexemails'] = indexemails
        context['endtime'] = str(misc.formatDate(datetime.datetime.now()))
        context['starttime'] = str(misc.formatDate(starttime))
        return context

class DomainReportPrintView(DomainPdf, TimeDelayMixin, WeasyTemplateResponseMixin):
    # output of DetailView rendered as PDF

    # pdf_stylesheets = [
    #     settings.STATICFILES_DIRS[0] + '/css/pdf.css',
    # ]
    # # show pdf in-line (default: True, show download dialog)
    # pdf_attachment = True
    # # suggested filename (is required for attachment!)
    # pdf_filename = 'tranchulas.pdf'
    print('printing domain report')

def darkbotEmailReport(fileid, userid):
    global filelist
    currentChart1 = Charts(chart_name="dummynew", chart_file=fileid, chart_user=userid)
    currentChart1.save()
    currentChart2 = Charts(chart_name="dummynew", chart_file=fileid, chart_user=userid)
    currentChart2.save()
    currentChart3 = Charts(chart_name="dummynew", chart_file=fileid, chart_user=userid)
    currentChart3.save()
    filelist.append(fileid)
    driver = webdriver.Firefox (executable_path="geckodriver")
    driver.get('http://127.0.0.1:8080/api/trace/showcharts')
    time.sleep(3)
    driver.close()

def darkbotDomainReport(domain, userid, email):
    # global domainlist
    currentChart1 = Charts(chart_name="dummynew", chart_file=domain, chart_user=userid)
    currentChart1.save()
    currentChart2 = Charts(chart_name="dummynew", chart_file=domain, chart_user=userid)
    currentChart2.save()
    currentChart3 = Charts(chart_name="dummynew", chart_file=domain, chart_user=userid)
    currentChart3.save()
    # domainlist.append(domain)
    print('successfully appended domain to the domain list')
    driver = webdriver.Firefox(executable_path="geckodriver")
    driver.get('http://127.0.0.1:8080/api/trace/showdomaincharts')
    time.sleep(3)
    driver.close()
    views.saveReport(domain, userid, "Domain Monitoring")
    views.sendReportCompletionEmail(email)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def celeryReport(request):
    fileid = request.data["fileid"]
    tasks.createEmailReport.delay(fileid)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def celeryReportDomain(request):
    userid = request.data["userid"]
    tasks.createDomainReport.delay(userid)


def myLaterPages(canvas,doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page + 2, ""))
    canvas.restoreState()

def convertingDictToList(d):
    l = []
    for (index, each) in enumerate(d):
        l.append([])
        l[index].append(each['email'])
        l[index].append(each['password'])
    return l

def createCoverPage(canvas, img, width, height):
    canvas.drawImage(img, 0, 0, width=width, height=height)

def createHeader(c, startdate):
    width, height = A4
    c.translate(0, height)
    c.setFillColorRGB(0.9254901960784314, 0.9411764705882353, 0.9450980392156863)
    c.rect(0, -0.7 * inch, width, -3 *inch, fill=True, stroke=False)
    c.setFillColorRGB(0.0352941176470588, 0.5176470588235294, 0.8901960784313725)
    c.setStrokeColorRGB(0.0352941176470588, 0.5176470588235294, 0.8901960784313725)
    c.setLineWidth(0.5*inch)
    c.line(0, -0.7*inch, 0, -3.7*inch)
    c.setFont('Helvetica-Bold', 22)
    c.drawString(1.1 * inch, -1.6*inch, "Dark Web Monitoring")
    c.setFont('Helvetica', 12)
    c.setFillColorRGB(0.5843137254901961, 0.6470588235294118, 0.6509803921568627)
    c.drawString(1.1*inch, -2*inch, "Start Date")
    c.setFont('Helvetica-Bold', 12)
    c.setFillColorRGB(0.0352941176470588, 0.5176470588235294, 0.8901960784313725)
    c.drawString(2.3 * inch, -2 * inch, str(startdate))
    c.setFont('Helvetica', 12)
    enddate = datetime.datetime.now()
    c.setFillColorRGB(0.5843137254901961, 0.6470588235294118, 0.6509803921568627)
    c.drawString(1.1 * inch, -2.4 * inch, "End Date")
    c.setFont('Helvetica-Bold', 12)
    c.setFillColorRGB(0.0352941176470588, 0.5176470588235294, 0.8901960784313725)
    c.drawString(2.3 * inch, -2.4 * inch, str(enddate))

class Assets(generics.ListAPIView):
    queryset = MonitorDomain.objects.all()
    serializer_class = MonitorDomainSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = OverRideDefaultPagination


class Reports(generics.ListAPIView):
    queryset = Report.objects.all().order_by("-request_date")
    serializer_class = ReportSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = OverRideDefaultPagination

class GroupReports(generics.ListAPIView):
    queryset = Report.objects.all().order_by("-request_date")
    serializer_class = ReportSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = OverRideDefaultPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['userid']

class GroupAssets(generics.ListAPIView):
    queryset = MonitorDomain.objects.all()
    serializer_class = MonitorDomainSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = OverRideDefaultPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['userid']


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def search(request):
    start =  str(misc.formatDate(datetime.datetime.now()))
    print(request.data)
    type_constraint = ['email', 'username', 'password', 'hash', 'ip', 'domain', 'phone', 'searchengine', 'breaches', 'paste']

    if 'username' in request.data:
        username = request.data['username']

    if 'email' in request.data:
        useremail = request.data['email']

    if 'userid' in request.data:
        userid = request.data['userid']

    if 'query' in request.data:
        query = request.data['query']
    else:
        return Response(status.HTTP_400_BAD_REQUEST)

    if 'type' in request.data:
        typee = request.data['type']
    else:
        typee = ''

    if 'wildcard' in request.data:
        wildcard = request.data['wildcard'].lower()
    else:
        wildcard = 'false'

    if 'regex' in request.data:
        regex = request.data['regex'].lower()
    else:
        regex = 'false'

    if wildcard == 'false' or wildcard == 'true':
       pass
    else:
        return Response(status.HTTP_400_BAD_REQUEST)

    if regex == 'false' or regex == 'true':
        pass
    else:
        return Response(status.HTTP_400_BAD_REQUEST)

    if regex == 'true' and wildcard == 'true':
        return Response(status.HTTP_400_BAD_REQUEST)

    if typee not in type_constraint or typee == '':
        return Response(status.HTTP_400_BAD_REQUEST)

    # storeApiLog(type,query)

    tasks.saveLog.delay(typee, query, userid, username, useremail)

    if typee == 'email' or typee == 'breaches' or typee == 'indexemails' or typee == 'paste':
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", query):
            return Response(status.HTTP_400_BAD_REQUEST)


    if typee == 'domain' and regex == 'false' and wildcard == 'false':
        if not re.fullmatch(r'^[a-zA-Z0-9-]{2,61}\.[a-zA-Z0-9-]{2,61}\.?[a-zA-Z0-9-]*$', query):
            return Response(status.HTTP_400_BAD_REQUEST)

    if typee == 'ip' and regex == 'false' and wildcard == 'false':
        if not re.fullmatch(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', query):
            return Response(status.HTTP_404_NOT_FOUND)

    if typee == 'phone' and regex == 'false' and wildcard == 'false':
        if not re.fullmatch(r'\+?[0-9 ]+', query):
            return Response(status.HTTP_404_NOT_FOUND)

    if typee == 'email' and wildcard == 'true' and query in [r'*@*.*', r'*@*.*.*']:
        return Response(status.HTTP_400_BAD_REQUEST)


    obj = {}
    if typee == 'password':
        obj['query'] = query
    else:
        obj['query'] = query.lower()
    obj['type'] = typee
    obj['wildcard'] = wildcard
    obj['regex'] = regex

    if (not (typee in ['email', 'domain', 'username']) and wildcard == 'false' and regex == 'false'):
        obj['request'] = request
    final = []
    print('wildcard', wildcard)
    print('regex', regex)
    print('type', typee)
    if typee in ['email', 'domain', 'username'] and wildcard == 'false' and regex == 'false':
        print('no way what is he doing here')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            t1 = executor.submit(leakCheck, obj)
            t2 = executor.submit(getRecordsFromDB, obj)
            r1 = t1.result()
            if typee == 'username':
                r1['type'] = 'username'
            t3 = executor.submit(parseLeakCheckResponse, r1)
            r2 = t2.result()
            #print(r2)
            t4 = executor.submit(parseDbResponse, r2)
            objr = {}
            objr['res1'] = t4.result()
            objr['res2'] = t3.result()
            t7 = executor.submit(mergeResponse, objr)
            final = t7.result()
        tasks.saveData.delay(final)
        # storeInDbCaller(final)
        return Response(final)

    elif wildcard == 'false' and regex == 'false' and typee in ['hash', 'ip', 'name', 'phone', 'password', 'before_at']:
        print('daud bhai see this')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            print(obj)
            t1 = executor.submit(getRecordsFromDB, obj)
            final = t1.result()
            if final == 'Invalid Domain':
                return Response(status.HTTP_400_BAD_REQUEST)
    elif typee == 'searchengine':
        return newSearchEngine(query)
    elif typee == 'breaches':
        #return newCheckEmailBreaches(query)
        #print('yes')
        return Response(getBreach(query))
    elif typee == 'paste':
        #return newCheckPastes(query)
        #print('no')
        return Response(getPaste(query))
    elif wildcard == 'true' or regex == 'true':
        now = datetime.datetime.now()
        pdf_filename = str(now) + ".pdf"
        saveReportInstance(str(obj['query']), userid, pdf_filename)
        obj['fileid'] = pdf_filename
        obj['starttime'] = start
        obj['email'] = useremail
        tasks.createReportForRegexWildcard.delay(obj)
        return Response({"status": 200})
        # print("yessss")
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     t1 = executor.submit(getRecordsFromDB, obj)
        #     final = t1.result()


    # return Response(final)
    return final


def leakCheck(obj):
    key = settings.LEAK_CHECK_KEY
    url = settings.LEAK_CHECK_URL
    typee = obj['type']
    if obj['type'] == 'domain':
        typee = 'domain_email'
    elif obj['type'] == 'username':
        typee = 'login'
    data = {'key': key, 'type': typee, "check": obj['query']}
    #print(data)
    try:
        res = requests.get(url, params=data)
    except Timeout:
        print('timeout at leakcheck')
        return []
    except HTTPError as http_err:
        print('http errot at leakcheck')
        return []
    except Exception as err:
        print(err)
        return []
    if (res.status_code != 200):
        return []
    res = res.json()
    return res


def getRecordsFromDB(obj):
    print('yess')
    print(obj)
    max_limit = 10000
    invalid_domains = ['gmail.com', 'google.com', 'zoho.com', 'outlook.com', 'hotmail.com', 'live.com']
    records = []
    if obj['type'] == "email" and obj['wildcard'] == "false" and obj['regex'] == "false":
        try:
            before_at, domain = misc.returnTwo(obj['query'])
            print('here why not?')
            records = Email_passwords.objects.filter(before_at=before_at, domain=domain).values()
        except Exception as err:
            print(f'Other error occurred: {err}')
            records = []
    elif obj['type'] == "before_at" and obj['wildcard'] == "false" and obj['regex'] == "false":
        pagination_class = LimitOffsetPagination
        paginator = pagination_class()
        queryset = Email_passwords.objects.filter(before_at__exact=obj['query']).count()
        if queryset > max_limit:
            return Response(status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            queryset = Email_passwords.objects.filter(before_at__exact=obj['query'])
        page = paginator.paginate_queryset(queryset, obj['request'])
        serializer = Email_passwordsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif obj['type'] == "username" and obj['wildcard'] == "false" and obj['regex'] == "false":
        try:
            records = Email_passwords.objects.filter(username__exact=obj['query']).values()
            for each in records:
                print(each)
        except Exception as err:
            print(f'Other error occurred: {err}')
            records = []
    elif obj['type'] == "password" and obj['wildcard'] == "false" and obj['regex'] == "false":
        pagination_class = LimitOffsetPagination
        paginator = pagination_class()
        queryset = Email_passwords.objects.filter(password__exact=obj['query']).count()
        if queryset > max_limit:
            return Response(status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            queryset = Email_passwords.objects.filter(password__exact=obj['query'])
        page = paginator.paginate_queryset(queryset, obj['request'])
        serializer = Email_passwordsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif obj['type'] == "hash" and obj['wildcard'] == "false" and obj['regex'] == "false":
        pagination_class = LimitOffsetPagination
        paginator = pagination_class()
        queryset = Email_passwords.objects.filter(hash__exact=obj['query']).count()
        if queryset > max_limit:
            return Response(status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            queryset = Email_passwords.objects.filter(hash__exact=obj['query'])
        page = paginator.paginate_queryset(queryset, obj['request'])
        serializer = Email_passwordsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif obj['type'] == "ip" and obj['wildcard'] == "false" and obj['regex'] == "false":
        pagination_class = LimitOffsetPagination
        paginator = pagination_class()
        queryset = Email_passwords.objects.filter(ipaddress__exact=obj['query']).count()
        if queryset > max_limit:
            return Response(status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            queryset = Email_passwords.objects.filter(ipaddress__exact=obj['query'])
        page = paginator.paginate_queryset(queryset, obj['request'])
        serializer = Email_passwordsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif obj['type'] == "phone" and obj['wildcard'] == "false" and obj['regex'] == "false":
        pagination_class = LimitOffsetPagination
        paginator = pagination_class()
        queryset = Email_passwords.objects.filter(phonenumber__exact=obj['query']).count()
        if queryset > max_limit:
            return Response(status.HTTP_507_INSUFFICIENT_STORAGE)
        else:
            queryset = Email_passwords.objects.filter(phonenumber__exact=obj['query'])
        page = paginator.paginate_queryset(queryset, obj['request'])
        serializer = Email_passwordsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif obj['type'] == "domain" and obj['wildcard'] == "false" and obj['regex'] == "false":
        if obj['query'] in invalid_domains:
            return 'Invalid Domain'
        try:
            records = Email_passwords.objects.filter(domain__exact=obj['query']).values()
        except Exception as err:
            print(f'Other error occurred: {err}')
            records = []

    return records

def weLeak(obj):
    url = settings.WE_LEAK_URL
    key = settings.WE_LEAK_KEY
    headers = {'Authorization': 'Bearer '+key, "User-Agent": 'Tranchulas'}
    body = {'query': obj['query'], 'type': obj['type'], 'limit': 10000, 'wildcard': obj['wildcard'], 'regex': obj['regex']}
    try:
        res = requests.post(url, data=body, headers=headers)
    except Timeout:
        return []
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        return []
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
        return []
    if (res.status_code != 200):
        return []
    print(res)
    return res

def parseWeLeakResponse(response):
    realres = ''
    for each in response:
        each = str(each)
        if each[0] == "b":
            each = each [2:]
        if each[0] == "'":
            each = each [1:]
        each = each[:-1]
        each = each.replace('\\', '')
        each = each.replace('""', '"')
        realres = realres + each

    if 'Database' in realres:
        realres = realres.replace('Database', 'source')
    if 'Email' in realres:
        realres = realres.replace('Email', 'email')
    if 'Password' in realres:
        realres = realres.replace('Password', 'password')
    if 'First Name' in realres:
        realres = realres.replace('First Name', 'firstname')
    if 'Last Name' in realres:
        realres = realres.replace('Last Name', 'lastname')
    if 'Name' in realres:
        realres = realres.replace('Name', 'name')
    if 'Date of Birth' in realres:
        realres = realres.replace('Date of Birth', 'dateofbirth')
    if 'Username' in realres:
        realres = realres.replace('Username', 'username')
    if 'Hash' in realres:
        realres = realres.replace('Hash', 'hash')
    if 'Registered IP Address' in realres:
        realres = realres.replace('Registered IP Address', 'ipaddress')
    if 'Last IP Address' in realres:
        realres = realres.replace('Last IP Address', 'lastipaddress')
    # for phone number goes down
    if 'Phone' in realres:
        realres = realres.replace('Phone', 'phonenumber')
    if 'Salt' in realres:
        realres = realres.replace('Salt', 'salt')
    if 'Address' in realres:
        realres = realres.replace('Address', 'address')
    realres = str(realres)
    realres = json.loads(realres)
    #print(realres)
    return realres['Data']


def parseDbResponse(response):
    try:
        for each in response:
            for e in list(each):
                if each[e] == '':
                    each.pop(e, None)
                elif e == 'id' or e == '_id' or e == 'before_at' or e == 'after_at' or e == 'after_first_dot' or e == 'after_second_dot' or e == 'domain':
                    each.pop(e, None)
    except Exception as err:
        response = []
    return response

def parseLeakCheckResponse(response):
    final = []
    if 'result' in response:
        for each in response['result']:
            mydict = {}
            each['line'] = each['line'].split(':')
            if len(each['line']) == 2:
                if 'type' in response:
                    mydict['username'] = each['line'][0]
                else:
                    mydict['email'] = each['line'][0]
                mydict['password'] = each['line'][1]
                final.append(mydict)
    return final

def mergeResponse(obj):
    l = []
    obj['res1'] = list(obj['res1'])
    obj['res2'] = list(obj['res2'])
    for each in obj['res1']:
        for e in obj['res2']:
            if "email" in e and "password" in e and "email" in each and "password" in each:
                if e["email"].lower() == each["email"].lower() and e["password"] == each["password"]:
                    obj['res2'].remove(e)
                    break
            elif "username" in e and "password" in e and "username" in each and "password" in each:
                if e["username"] == each["username"] and e["password"] == each["password"]:
                    obj['res2'].remove(e)
                    break
    l.extend(obj['res1'])
    l.extend(obj['res2'])
    return l

@misc.checkRecordUniqueness
def storeInDb(each):
    # misc.validateSavageInEmailPassword(res)
    # for each in res:
    try:
        if "email" in each:
            each["before_at"], each["domain"] = misc.returnTwo(each["email"])
            each["email"] = each["email"].lower()
        if not (each == {}):
            e = Email_passwords(**each)
            e.save()
    except Exception as e:
        print(e)
        print('exception while storing in email_passwords table')


def storeInDbCaller(res):
    for each in res:
        storeInDb(each)
    # print('stored successfully check your DB')


def storeApiLog(typee, query, userid, username, useremail):
    try:
        l = ApiSearchLog(userid=userid, username=username, useremail=useremail, type=typee, search_term=query)
        l.save()
    except Exception as e:
        print(e)
        print('exception while storing api search logs in table')
    print("search log is saved successfully")

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAdminUser])
def download(request):
    file_path = request.data["path"]
    print(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response




def createReportForQuery(obj):
    max_limit = 10000
    if obj['wildcard'] == "false" and obj['regex'] == "true":
        print("yes regex thing")
        print('regex is', obj['query'])
        if misc.isDigitOrNumber(obj['query'][0]):
            obj['query'] = r'^' + obj['query']
        if misc.isDigitOrNumber(obj['query'][-1]):
            obj['query'] = obj['query'] + r'$'
        print('regex is', obj['query'])
        try:
            print('before counting')
            filter = obj['type'] + '__regex'
            queryset = Email_passwords.objects.filter(** {filter: obj['query']}).count()
            if queryset > max_limit:
                updateReportInstance(obj["fileid"], "MAX ALLOWED RECORDS LIMIT EXCEEDS", datetime.datetime.now())
                return
            elif queryset == 0:
                updateReportInstance(obj["fileid"], "No Records Found", datetime.datetime.now())
                return
            else:
                print('before actual response')
                queryset = Email_passwords.objects.filter(** {filter: obj['query']}).values()
        except Exception as err:
            print(f'Other error occurred: {err}')
            updateReportInstance(obj["fileid"], "failure", datetime.datetime.now())
            return

    elif obj['wildcard'] == "true" and obj['regex'] == "false":
        print("yes wildcard thing")
        print("obj['query'] ",obj['query'])
        print("obj[type] ",obj['type'])
        query_number = 2
        if obj['type'] == 'email':
            before_at, after_at = misc.returnTwo(obj['query'])
            before_at = misc.finalizeRegex(before_at, "email")
            after_at = misc.finalizeRegex(after_at, "email")
            print("before_at", before_at)
            print("after_at", after_at)
            if before_at != r'[a-zA-Z0-9\-_.]*' and after_at != r'[a-zA-Z0-9\-_.]*\.[a-zA-Z0-9\-_.]*':
                query_number = 1
            if after_at != r'[a-zA-Z0-9\-_.]*\.[a-zA-Z0-9\-_.]*':
                obj['type'] = 'domain'
                obj['query'] = after_at
            if before_at != r'[a-zA-Z0-9\-_.]*':
                obj['type'] = 'before_at'
                obj['query'] = before_at
        else:
            obj['query'] = misc.finalizeRegex(obj['query'], obj['type'])
            print('final regex is', obj['query'])

        filter = obj['type'] + '__regex'
        try:
            print('before counting')
            if query_number == 1:
                queryset = Email_passwords.objects.filter(before_at__regex=before_at,domain__regex=after_at).count()
            elif query_number == 2:
                print("executing right query 2")
                queryset = Email_passwords.objects.filter(** {filter: obj['query']}).count()
            if queryset > max_limit:
                updateReportInstance(obj["fileid"], "MAX ALLOWED RECORDS LIMIT EXCEEDS", datetime.datetime.now())
                return
            elif queryset == 0:
                updateReportInstance(obj["fileid"], "No Records Found", datetime.datetime.now())
                return
            else:
                print('before actual response')
                if query_number == 1:
                    queryset = Email_passwords.objects.filter(before_at__regex=before_at,domain__regex=after_at).values()
                elif query_number == 2:
                    print('executing right query again')
                    queryset = Email_passwords.objects.filter(** {filter: obj['query']}).values()
        except Exception as err:
            print(f'Other error occurred: {err}')
            updateReportInstance(obj["fileid"], "failure", datetime.datetime.now())
            return
    print(type(queryset))
    context = {}
    context['leakedpasswords'] = queryset
    context['endtime'] = str(misc.formatDate(datetime.datetime.now()))
    context['starttime'] = obj['starttime']
    stylesheet = misc.getPath(settings.BASE_DIR, "static/css/pdf.css")
    path = misc.getPath(settings.BASE_DIR, "search/templates/search")
    dest = misc.getPath(settings.BASE_DIR, "reports/" + obj['fileid'])
    env = Environment(loader=FileSystemLoader(searchpath=path))
    template = env.get_template("search_result.html")
    html_out = template.render(context)
    print(__file__)
    HTML(string=html_out, base_url=__file__).write_pdf(dest, stylesheets=[stylesheet])
    updateReportInstance(obj['fileid'], "success", datetime.datetime.now())
    views.sendReportCompletionEmail(obj['email'])
