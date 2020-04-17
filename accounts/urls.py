from django.urls import path
from accounts import views
from dark_bot import views as v
# TEMPLATE_TAGGING
app_name = 'accounts'

urlpatterns=[
    # path('register/', views.register, name="register"),
    # path('signup/',views.SignUp.as_view(),name='signup'),
    path('subcribe/',views.SubscribeMakeRequest.as_view(),name="subscribe"),
    path('testing',views.get_client_ip),
    path('login/',v.index,name='l'),

]