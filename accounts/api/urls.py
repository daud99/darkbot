from django.urls import path
from rest_framework.authtoken import views as v
from . import views



# TEMPLATE_TAGGING
app_name = 'accounts_api'

urlpatterns = [
    # this route will verify the credentials and see if user is the superuser if it is superuser then it will send the token
    path('getToken/', v.obtain_auth_token, name="gettoken"),
]