from accounts.models import IpWhiteList, IpBlackList
import datetime
from dateutil.relativedelta import relativedelta
import logging

from django.core.exceptions import PermissionDenied

try:
    from django.core.urlresolvers import resolve
except ImportError:
    from django.urls import resolve
from django.conf import settings
from django.http import Http404
from django import VERSION


# import ipware

class IpWhitelister():
    """
    Simple middlware to allow IP addresses via settings variables ALLOWED_IPS, ALLOWED_IP_RANGES.
    Made to be compatible with Django 1.9 and also 1.10+
    """

    logger = logging.getLogger(__name__)

    def __init__(self, get_response=None):
        self.get_response = get_response
        self.ALLOWED_IPS = self._get_config_var('whitelistips')
        self.RESTRICTED_IPS = self._get_config_var('blacklistips')

    def __call__(self, request):
        # print('its call function reporting')
        self.ALLOWED_IPS = self._get_config_var('whitelistips')
        self.RESTRICTED_IPS = self._get_config_var('blacklistips')
        # print(self.ALLOWED_IPS)
        # print(self.RESTRICTED_IPS)
        response = self.process_request(request)

        ''' agr response none nahi ha or  self.get_response jo ha wo true ha tab jo request ko 
        proceed karnay do warna nahi 
        '''
        # print('response here is')
        # print(response)
        # print('self.get_response here is')
        # print(self.get_response)
        if not response and self.get_response:
            response = self.get_response(request)

        return response

    def _get_config_var(self, name):
        """
        Get the whitelist ips from the database
        """

        if name == 'whitelistips':
            whiteips = IpWhiteList.objects.values('ipaddress')
            a = list(whiteips)
            return [each['ipaddress'] for each in a]
        elif name == 'blacklistips':
            blackips = IpBlackList.objects.values('ipaddress')
            a = list(blackips)
            return [each['ipaddress'] for each in a]

    def get_client_ip(self, request):
        """
        Get the incoming request's originating IP, looks first for X_FORWARDED_FOR header, which is provided by some
        PaaS platforms, since the Django REMOTE_ADDR is affected by internal routing.  Fallback to the REMOTE_ADDR if
        the header is not present
        """

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ips = x_forwarded_for.split(',')
            ips = map(str.strip, ips)
        else:
            ips = [request.META.get('REMOTE_ADDR')]

        '''
        ips = [request.COOKIES['ip']]
        print('IP from cookie is')
        '''
        # print(ips)
        return ips

    def process_request(self, request):
        # Get the app name
        # if this function returns the None then your request will proceed successfully
        app_name = resolve(request.path).app_name
        # print('the current request is for the app which name is in next line')
        if app_name == '':
            app_name = 'root'
        # print(app_name)
        # print('your django version is : ')
        # print(VERSION)
        # print(request.user.is_authenticated)
        request_ips = self.get_client_ip(request)
        request_ips = list(request_ips)
        if len(request_ips) == 1:
            # print('len of list inside if is ',len(request_ips))
            request_ip = str(request_ips[0])
        # print('current user ip address is')
        if (request.COOKIES.get('ip')):
            request_ip = request.COOKIES.get('ip')
        # print(request_ip)
        # print('current is superuser or not letsee in below line')
        # print(request.user.is_superuser)
        if app_name == 'userdashboard' and not request.user.is_superuser and 'doughnutchart' not in app_name and 'daychart' not in app_name and 'histogramchart' not in app_name:
            if request_ip in self.ALLOWED_IPS and request_ip not in self.RESTRICTED_IPS and request.user.is_authenticated:
                return None
            else:
                print("ip restriction")
                raise PermissionDenied()
        return None


class QueryMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        # One-time configuration and initialization.
        # print('i think middleware is also initiated')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        app_name = resolve(request.path).app_name
        # print("app_name in here is", app_name)
        if (request.user.is_authenticated and not request.user.is_superuser and app_name == "search"):
            if (request.user.date_joined and request.user.number_of_queries):
                join_date = request.user.date_joined
                # print(join_date)
                # print(join_date + relativedelta(months=1))
                restrict_datetime = join_date + relativedelta(months=1)
                current_datetime = datetime.datetime.now(datetime.timezone.utc)
                if (current_datetime < restrict_datetime):
                    pass
                else:
                    print("Your subscription is cancelled")
                    raise PermissionDenied()

                print(datetime.datetime.now())
                if request.user.number_of_queries < 1:
                    print("your queries are finished")
                    raise PermissionDenied()
                else:
                    pass
                    # print(request.user.number_of_queries)
        # print('middleware must be executed')
        # Code to be executed for each request/response after
        # the view is called.

        return response
