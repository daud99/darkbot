import threading
from django.db.models import Count
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, get_object_or_404
from accounts.models import SubscribeRequest as RequestModel, User
from accounts.forms import UserCreateForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth.mixins import AccessMixin
from accounts.script import sendmail, iplisting
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from gatherdumps.models import CardDump, CardCvv, Email_passwords
from chartjs.views.lines import BaseLineChartView
from django.utils import timezone
from .forms import UploadFileForm
import datetime
from search.api.views import saveMonitorEmail, saveCurrentStatus, darkbotEmailReport
from search.models import Messages, MonitorDomain, Report, GlobalVar, ApiSearchLog
from fileparser.models import FolderSelectInfoModel, FileReadInfoModel
from fileparser.scripts.main import main
from  adminpanel.tasks import Monitoring, startDomainMonitoring, stopDomainMonitoring, startMainForFileParser
from search import tasks


def user_is_loggedin_and_superuser(func):
    def wrapper(*args):
        if not args[0].user.is_authenticated:
            messages.error(args[0], 'You are not Logged In')
            return HttpResponseRedirect('/login')
        elif not args[0].user.is_superuser:
            messages.error(args[0], 'Only superuser can access this route')
            return HttpResponseRedirect('/userdashboard')
        else:
            return func(args[0])
    return wrapper

@user_is_loggedin_and_superuser
def index(request):
    today_subscription_requests = RequestModel.objects.all().order_by('-created_request')[:5]
    today_search_logs = ApiSearchLog.objects.all().order_by('-search_time')[:8]
    context = {
        "requests": today_subscription_requests,
        "logs": today_search_logs
    }
    return render(request, "adminpanel/index.html", context)

@user_is_loggedin_and_superuser
def message(request):
    messages = Messages.objects.all()

    context = {
        'msgs': messages
    }
    return render(request,'adminpanel/message.html', context)

def deleteMessage(request,id):
    print("i am in delete message method")
    print(id)
    msg = get_object_or_404(Messages, id=id)
    msg.delete()
    msgs = Messages.objects.all()
    messages.success(request,'Message is successfully deleted!')
    context = {
        'msgs': msgs
    }
    return render(request,'adminpanel/message.html',context)

@user_is_loggedin_and_superuser
def profile(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        if firstname and lastname:
            User.objects.filter(id=request.user.id).update(first_name=firstname,last_name=lastname)
        messages.success(request,'Your profile is updated successfully')
        return render(request,'adminpanel/profile.html')
    else:
        return render(request,'adminpanel/profile.html')



class RequestListView(AccessMixin,ListView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            messages.error(request,'You are not Logged In')
            return self.handle_no_permission()
        if not request.user.is_superuser:
            # Redirect the user to somewhere else - add your URL here
            messages.error(request,'Only superuser is allowed to access this route')
            return HttpResponseRedirect('/login')
        return super().dispatch(request, *args, **kwargs)
    context_object_name = 'requests_list'
    model = RequestModel

class RequestDetailView(AccessMixin,CreateView,DetailView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            messages.error(request, 'You are not Logged In')
            return self.handle_no_permission()
        if not request.user.is_superuser:
            # Redirect the user to somewhere else - add your URL here
            messages.error(request, 'Only superuser is allowed to access this route')
            return HttpResponseRedirect('/userdashboard')
        return super().dispatch(request, *args, **kwargs)
    form_class = UserCreateForm
    # success_url = self.get_success_url()
    template_name = 'accounts/signup.html'
    context_object_name = 'request'
    model = RequestModel
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        return reverse_lazy('adminpanel:delete', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        yahopass = form.cleaned_data['password2']
        # print('password before form .save function called',form.cleaned_data['password2'])
        self.object = form.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        iplisting.addip(self.object.ip_address,self.object.email)
        subject = 'Darkbot Credentials'
        from_email = sendmail.EMAIL_HOST_USER
        to_list = [self.object.email,'daudahmed@zoho.com']
        context = {
            'email': self.object.email,
            'password': yahopass
        }
        html_message = render_to_string('email_template.html', context)
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email, to_list, html_message=html_message)
        messages.success(self.request, 'Credentials are successfully sended')
        return HttpResponseRedirect(self.get_success_url())

class RequestDeleteView(AccessMixin,SuccessMessageMixin,DeleteView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # This will redirect to the login view
            messages.error(request, 'You are not Logged In')
            return self.handle_no_permission()
        if not request.user.is_superuser:
            # Redirect the user to somewhere else - add your URL here
            messages.error(request, 'Only superuser is allowed to access this route')
            return HttpResponseRedirect('/userdashboard')
        return super().dispatch(request, *args, **kwargs)
    model = RequestModel
    success_url = reverse_lazy('adminpanel:request')
    success_message = 'The cerrosponding subscription request is removed'


# here goes below the visualization shit

class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July","August","September","October","November","December"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Email", "Password", "Domain", "Any", "Hash", "IP", "Username", "phone"]

    def get_data(self):
        """Return 3 datasets to plot."""
        emailSearchList = countEachSearchNumber("email")
        passSearchList = countEachSearchNumber("password")
        domainSearchList = countEachSearchNumber("domain")
        anySearchList = countEachSearchNumber("searchengine")
        hashSearchList = countEachSearchNumber("hash")
        ipSearchList = countEachSearchNumber("ip")
        usernameSearchList = countEachSearchNumber("username")
        phoneSearchList = countEachSearchNumber("phone")
        return [emailSearchList, passSearchList, domainSearchList, anySearchList, hashSearchList, ipSearchList, usernameSearchList, phoneSearchList]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()


def countEachSearchNumber(type_of_search):
    year = datetime.datetime.today().year
    monthCountList = [0,0,0,0,0,0,0,0,0,0,0,0]
    relevantSearch = ApiSearchLog.objects.filter(type__iexact=type_of_search).filter(search_time__year=year)
    for each in relevantSearch:
        currentMonth = extract_month(str(each.search_time))
        if currentMonth == "01":
            monthCountList[0] += 1
        elif currentMonth == "02":
            monthCountList[1] += 1
        elif currentMonth == "03":
            monthCountList[2] += 1
        elif currentMonth == "04":
            monthCountList[3] += 1
        elif currentMonth == "05":
            monthCountList[4] += 1
        elif currentMonth == "06":
            monthCountList[5] += 1
        elif currentMonth == "07":
            monthCountList[6] += 1
        elif currentMonth == "08":
            monthCountList[7] += 1
        elif currentMonth == "09":
            monthCountList[8] += 1
        elif currentMonth == "10":
            monthCountList[9] += 1
        elif currentMonth == "11":
            monthCountList[10] += 1
        elif currentMonth == "12":
            monthCountList[11] += 1
    return monthCountList



def extract_month(date):
    return date[5:7]

def DoughnutChart(request):
    l = []
    labels = []
    topFiveAgents = ApiSearchLog.objects.values("userid").annotate(searchcount=Count("userid")).order_by('-searchcount')
    for each in topFiveAgents:
        l.append(each["searchcount"])
        currentUser = ApiSearchLog.objects.filter(userid=each['userid']).first()
        labels.append(currentUser.useremail)
        print(each["searchcount"])
    if(len(l)>4):
        totalSearch = sum(l)
        l = l[:3]
        l.append(totalSearch-sum(l))
        labels = labels[:3]
        labels.append("Others")


    print("l")
    print(l)
    data = {"l":l,"labels":labels}
    print('yes i should be called')
    return JsonResponse(data,safe=False)

def HistogramChart(request):
    data = []
    labels = []
    searchTypeList = ApiSearchLog.objects.values("type").annotate(searchcount=Count("type"))
    for each in searchTypeList:
        labels.append(each["type"])
        data.append((each["searchcount"]))
    dataa = { "labels":labels, "data": data}
    return JsonResponse(dataa,safe=False)


def PolarChart(request):
    totalIndexEmails = Email_passwords.objects.all().count()
    totalCardDumps = CardDump.objects.all().count()
    totalCardCvvs = CardCvv.objects.all().count()
    data = [totalIndexEmails, totalCardDumps, totalCardCvvs]
    labels = ["Credentials", "Card Dump", "Card Cvv"]
    dataa = {"labels": labels, "data": data}
    return JsonResponse(dataa, safe=False)

def ActiveUserChart(request):
    l = []
    active_users = Session.objects.filter(expire_date__gte=timezone.now()).count()
    total_users = User.objects.all().count()
    labels = ['Active Users', "InActive Users"]
    print("active users are", active_users)
    l.append(active_users)
    l.append(total_users-active_users)
    data = {"l": l, "labels": labels}
    return JsonResponse(data, safe=False)

@user_is_loggedin_and_superuser
def monitorEmail(request):
    print("monitoremailfunction")
    globalvars = GlobalVar.objects.filter(id=1)[0]
    breaker = globalvars.emailmonitoring
    if request.method == "POST":
        print('request is post')
        on = request.POST.get('on')
        off = request.POST.get('off')
        print("on", on)
        print("off", off)
        switch = False
        if on == "Turn On Email Monitoring":
            # switch = True
            # startMonitor(False)
            Monitoring.delay(False)
            breaker = False
            messages.success(request, 'Live Email Monitoring started')
        if off == "Turn Off Email Monitoring":
            # switch = False
            # startMonitor(True)
            Monitoring.delay(True)
            breaker = True
            messages.success(request, 'Live Email Monitoring is successfully turned off')

    context = {
        "on": not breaker
    }
    return render(request, 'adminpanel/monitor.html', context)

def showReports(request):
    reports = Report.objects.all()
    context = {
        "reports": reports
    }
    return render(request, 'adminpanel/view-reports.html', context)


@user_is_loggedin_and_superuser
def monitorDomain(request):
    print("monitorDomain method")
    globalvars = GlobalVar.objects.filter(id=1)[0]
    breaker = globalvars.domainmonitoring
    if request.method == "POST":
        print('request is post')
        on = request.POST.get('on')
        off = request.POST.get('off')
        print("on", on)
        print("off", off)

        if on == "Turn On Domain Monitoring":
            breaker = False
            messages.success(request, 'Live Domain Monitoring started')
            startDomainMonitoring.delay()
        if off == "Turn Off Domain Monitoring":
            breaker = True
            stopDomainMonitoring.delay()
            messages.success(request, 'Live Domain Monitoring is successfully turned off')

        context = {
            "on1": not breaker
        }
        return render(request, 'adminpanel/monitor.html', context)


@user_is_loggedin_and_superuser
def monitor(request):
    globalvars = GlobalVar.objects.filter(id=1)[0]
    breaker = globalvars.emailmonitoring
    breaker1 = globalvars.domainmonitoring
    context = {
        "on": not breaker,
        "on1": not breaker1
    }
    return render(request, 'adminpanel/monitor.html', context)

def generateReport(request):
    print("yes here")
    domains = MonitorDomain.objects.all()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], request.user.id, request.user.email)
            # creatingEmailMonitoringReport.delay(request.FILES['file'], request.user.id)
            #p1 = threading.Thread(target=handle_uploaded_file, args=[request.FILES['file'], request.user.id, request.user.email])
            #p1.start()
            messages.success(request, 'You will received the email when your report is ready!')
            # print(request.FILES['file'])
            # return HttpResponseRedirect('/adminpanel/generate/report')
    else:
        form = UploadFileForm()
        print('generated successfully')


    context = {
        'domains': domains,
        'form': form
    }
    return render(request, 'adminpanel/generate-report.html', context)


def handle_uploaded_file(f, userid, email):
    fileid = str(datetime.datetime.now())
    for chunk in f.chunks():
        chunk = str(chunk)
        emails = chunk.replace("b'", "")
        emails = emails.replace("\\n\'", "")
        emails = emails.replace("'", "")
        emails = emails.split(' ')
        for email in emails:
            if email == " ":
                print("space found")
            else:
                if "@" in email:
                    try:
                        currentEmail = saveMonitorEmail(email, userid, fileid)
                        saveCurrentStatus(email, currentEmail)
                    except Exception as e:
                        print('exception in handling upload file')
                        print(e)
    else:
        print("for loop is finished now lets create report")
        print("fileid = "+fileid)
        print("userid ",userid)
        darkbotEmailReport(fileid, userid)
        saveReport(fileid,userid, "Email Monitoring")
        sendReportCompletionEmail(email)

def domainReport(request):
    domains = MonitorDomain.objects.all()
    form = UploadFileForm()
    if request.method == 'POST':
        domain = request.POST.get("domain")
        print("domain is")
        print(domain)
        #t1 = threading.Thread(target=darkbotDomainReport, args=[domain, request.user.id, request.user.email])
        #t1.start()
        messages.success(request, 'You will received the email when your report is ready!')
        # darkbotDomainReport(domain, request.user.id, request.user.email)
        tasks.creatingDomainMonitoringReport.delay(domain, request.user.id, request.user.email)
        #saveReport(domain, request.user.id, "Domain Monitoring")
    context = {
        'domains': domains,
        'form': form
    }
    return render(request, 'adminpanel/generate-report.html', context)


def saveReport(fileid, userid, type):
    report = Report(fileid=fileid,userid=userid,report_type=type)
    report.save()

def fileParser(request):
    if request.method == 'POST':
        folder_path = request.POST.get('folder_path')

        if folder_path == "" or folder_path == None or len(folder_path) < 5 or r'/' not in folder_path:
            messages.error(request, 'In appropriate path is entered!')
        else:
            try:
                fsi = FolderSelectInfoModel.objects.get(folder_path__exact=folder_path)
                if fsi.status == True:
                    messages.error(request, 'The parser for the respective folder is already running')
                    return render(request, 'adminpanel/fileParser.html')
                fri = FileReadInfoModel.objects.get(folder=fsi)
            except Exception as e:
                print(e)
                messages.error(request, 'Respective folder selector info or file read info missing in DB')
                return render(request, 'adminpanel/fileParser.html')

            # main(folder_path)
            startMainForFileParser.delay(folder_path)
            messages.success(request, "started successfully")

    return render(request, 'adminpanel/fileParser.html')

def test(request):
    globalvars = GlobalVar.objects.filter(id=1)[0]
    print(globalvars)
    # print(globalvars["emailmonitoring"])
    globalvars.emailmonitoring
    return render(request, 'adminpanel/view-reports.html')

def sendReportCompletionEmail(email):
    subject = 'Darkbot Report ALert'
    from_email = sendmail.EMAIL_HOST_USER
    to_list = [email, 'daudahmed@zoho.com']
    context = {
        "message": "Your report is ready you can download it now"
    }
    html_message = render_to_string('report_email.html', context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, to_list, html_message=html_message)