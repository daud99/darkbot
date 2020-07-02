from django.urls import path
from search import views

# TEMPLATE_TAGGING
app_name='search'

urlpatterns=[
    path('',views.search,name="searchi"),
    path('results/',views.search_result,name="result"),
    path('load/',views.load,name="load"),
    path('breach/',views.breach_result,name="breach"),
    path('pwned',views.pwned_breach,name="pwned"),
    path('cvv',views.get_cvv, name="get_cvv"),
    path('dumps', views.get_dump,name="get_dump"),
    path('pastes', views.get_paste,name="get_paste"),
    path('emails', views.get_pass_email, name="get_pass_mail"),
]