from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import User
from django.db.models import Count
from search.models import SearchLog
from django.contrib import messages
import datetime
from dateutil.relativedelta import relativedelta

# Create your views here.
@login_required(login_url='/login')
def index(request):
    print('user is superuser? ', request.user.is_superuser)
    if request.user.is_superuser:
        return redirect('/adminpanel')
    else:
        currentuser = User.objects.get(pk=request.user.id)
        today_search_logs = SearchLog.objects.filter(user=currentuser).order_by('-search_time')[:8]

        context = {
            "logs": today_search_logs
        }
        return render(request, "userdashboard/index.html", context)


@login_required(login_url='/login/')
def profile(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        company = request.POST.get('company')
        if firstname and lastname:
            User.objects.filter(id=request.user.id).update(first_name=firstname, last_name=lastname,company=company)
        messages.success(request, 'Your profile is updated successfully')
        return render(request, 'userdashboard/profile.html')
    else:
        return render(request, 'userdashboard/profile.html')


def showDoughnut1(request):
    l = []
    labels = ["Queries Consumed", "Queries Left"]
    totalqueries = getNumberOfQueriesFromPackage(request.user.subscription_plan)
    usedqueries = totalqueries - request.user.number_of_queries
    l.append(usedqueries)
    l.append(totalqueries - usedqueries)
    data = {"l": l, "labels": labels}
    print('yes i should be called')
    return JsonResponse(data, safe=False)


def showDoughnut2(request):
    join_date = request.user.date_joined
    print("joindate ", join_date)
    join_date = str(join_date)
    join_date = join_date[8:10]
    join_date = int(join_date)
    # print(join_date + relativedelta(months=1))
    # restrict_datetime = join_date + relativedelta(months=1)
    current_datetime = datetime.datetime.now(datetime.timezone.utc)
    print('below')
    # print(restrict_datetime)
    print(str(current_datetime))
    current_datetime = str(current_datetime)
    current_date = current_datetime[8:10]
    current_date = int(current_date)
    days = current_date - join_date
    if days >= 0:
        daysused = days
        daysleft = 30 - daysused
    else:
        days = days * -1
        daysleft = days
        daysused = 30 - daysleft

    print("current date ", current_date)
    l = []
    labels = ["Days Passed", "Days Left"]
    totalqueries = getNumberOfQueriesFromPackage(request.user.subscription_plan)
    usedqueries = totalqueries - request.user.number_of_queries
    l.append(daysused)
    l.append(daysleft)
    data = {"l": l, "labels": labels}
    print('yes i should be called')
    return JsonResponse(data, safe=False)


def getNumberOfQueriesFromPackage(key):
    myPackage = {"basic": 100, "advance": 150, "pro": 200}
    return myPackage[key.lower()]

def histogramChart(request):
    data = []
    labels = []
    currentuser = User.objects.get(pk=request.user.id)
    searchTypeList = SearchLog.objects.filter(user=currentuser).values("type").annotate(searchcount=Count("type"))
    for each in searchTypeList:
        labels.append(each["type"])
        data.append((each["searchcount"]))
    dataa = {"labels": labels, "data": data}
    return JsonResponse(dataa, safe=False)