from django.urls import path
from gatherdumps import views

# TEMPLATE_TAGGING
app_name = 'gatherdumps'

urlpatterns=[
    
    path('',views.index, name='gathering_main'),
    path('cancel/', views.cancel_all, name="cancel_all"),
    #path('login/',v.index,name='l'),
]