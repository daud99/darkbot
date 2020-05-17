from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Country, CardDump, CardCvv, Email_passwords, CardMarket, Checkpoint, CrawlerAccess
from gatherdumps.scripts.common.check_crawler_access import check_start_permission, check_cancel_permission
from gatherdumps.scripts.common.check_crawler_access import check_breaker_state, update_breaker_state
from gatherdumps.tasks import crawl_markets
from gatherdumps.scripts.celery_related import crawler_handlers
from gatherdumps.scripts.dumpsCollectors.dump_csv import read_cvvs
from fileparser.scripts.main import main

# from gatherdumps.models import dumps
# Create your views here.
driver = None
email_pass_seek_point = 0
data = None


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
    print('idher ha')
    global driver

    link = "gatherdumps/dumps_search.html"
    if request.method == 'POST':
        print("Received post request")
        marketplace = request.POST.get('marketplace')
        action = request.POST.get('categ')
        countries = Country.objects.all()

        if marketplace == "1" and action == '1':
            if (check_start_permission(100) == False):
                messages.warning(request, "You are Not Allowed to start that Crawler")
                return HttpResponseRedirect('/gatherdata')
            else:

                identity = int(marketplace + action)
                crawl_markets.delay(identity)
                messages.success(request, 'Process pushed to Queue')
                return HttpResponseRedirect('/gatherdata')
                # data.close()

        if marketplace == "1" and action == '2':
            if (check_start_permission(100) == False):
                messages.warning(request, "You are Not Allowed to start that Crawler")
                return HttpResponseRedirect('/gatherdata')

            else:

                identity = int(marketplace + action)
                crawl_markets.delay(identity)
                messages.success(request, 'Process pushed to Queue')
                return HttpResponseRedirect('/gatherdata')
                # data.close()

        if marketplace == "2" and action == '1':
            if (check_start_permission(100) == False):
                messages.warning(request, "You are Not Allowed to start that Crawler")
                return HttpResponseRedirect('/gatherdata')

            else:

                identity = int(marketplace + action)
                crawl_markets.delay(identity)
                messages.success(request, 'Process pushed to Queue')
                return HttpResponseRedirect('/gatherdata')
                # data.close()

        if marketplace == "2" and action == '2':
            if (check_start_permission(100) == False):
                messages.warning(request, "You are Not Allowed to start that Crawler")
                return HttpResponseRedirect('/gatherdata')

            else:
                identity = int(marketplace + action)
                crawl_markets.delay(identity)
                messages.success(request, 'Process pushed to Queue')
                return HttpResponseRedirect('/gatherdata')
                # data.close()

        if marketplace == "4" and action == "3":
            if (check_start_permission(200) == False):
                messages.warning(request, "You are Not Allowed to start that Crawler")
                return HttpResponseRedirect('/gatherdata')
            else:
                identity = int(marketplace + action)
                crawl_markets.delay(identity)
                messages.success(request, 'Process pushed to Queue')
                return HttpResponseRedirect('/gatherdata')
                # data.close()

        if marketplace == "5" and action == "3":
            if (check_start_permission(300) == False):
                messages.warning(request, "You are Not Allowed to start that Crawler")
                return HttpResponseRedirect('/gatherdata')
            # crawler_handlers.daud_collect_email_passwords(300)
            identity = int(marketplace + action)
            crawl_markets.delay(identity)
            messages.success(request, 'Process pushed to Queue')
            return HttpResponseRedirect('/gatherdata')
            # data.close()

        if marketplace == "5" and action == "4":
            print("main should be running")
            main("/daud/Desktop/test/")
            # if (check_start_permission(300) == False):
            #     messages.warning(request, "You are Not Allowed to start that Crawler")
            #     return HttpResponseRedirect('/gatherdata')
            # # crawler_handlers.daud_collect_email_passwords(300)
            # identity = int(marketplace + action)
            # crawl_markets.delay(identity)
            # messages.success(request, 'Process pushed to Queue')
            return HttpResponseRedirect('/gatherdata')

        else:
            print(marketplace, action)
            messages.warning(request, 'You have chosen wrong option')
        if marketplace == "6" and action == "5":
            read_cvvs("/home/darkbot/Documents/finalcvv.csv", "cvv")
            messages.success(request, 'completed')
            return HttpResponseRedirect('/gatherdata')

        else:
            print(marketplace, action)
            messages.warning(request, 'You have chosen wrong option')

        if marketplace == "6" and action == "6":
            read_cvvs("/home/darkbot/Documents/finaldump.csv", "dump")
            messages.success(request, 'completed')
            return HttpResponseRedirect('/gatherdata')

        else:
            print(marketplace, action)
            messages.warning(request, 'You have chosen wrong option')
    return render(request, link)


@user_is_loggedin_and_superuser
def get_brocard_dumps(request):
    pass


@user_is_loggedin_and_superuser
def cancel_all(request):
    global data, driver
    if (request.method == 'POST'):

        option_val = request.POST.get('cancel-option')
        if (option_val == "1"):

            close_dumps_driver()
            close_email_pass_collector()
            close_mail_crawler()
            messages.success(request, 'closed all crawlers and readers')
        elif (option_val == "2"):

            close_mail_crawler()
            messages.success(request, 'closed Email Cralwer over Indexed Forums')
        elif (option_val == "3"):
            close_email_pass_collector()
            messages.success(request, 'closed Email pass miners')
        elif (option_val == "4"):
            close_dumps_driver()
            messages.success(request, 'closed Dumps Collectors')
        else:
            messages.warning(request, 'Wrong Option Selected')
        return HttpResponseRedirect('/gatherdata')
    else:

        messages.warning(request, 'Nothing Can be Done Here')
        return HttpResponseRedirect('/gatherdata')


def close_mail_crawler():
    if (check_cancel_permission(200) == True):
        try:
            access_point = CrawlerAccess.objects.get(Access_identity__exact=400)
            access_point.authorize_access = False
            access_point.save()
        except Exception as e:
            print(e)
    else:
        print('No Permission to close mail crawler')


def close_email_pass_collector():
    # global data
    if (check_cancel_permission(300) == True):
        update_breaker_state(300, True)
    else:
        print('No Permission to close mail pass crawler')


def close_dumps_driver():
    # global driver
    if (check_cancel_permission(100) == True):
        update_breaker_state(100, True)
    else:
        print('No permission to close dumps crawler')
