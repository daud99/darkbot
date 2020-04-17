from django.conf.urls import url
from django.urls import path
from userdashboard import views,rep
# TEMPLATE_TAGGING
app_name = 'userdashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('doughnutchart', views.showDoughnut1, name='doughnutchart'),
    path('daychart', views.showDoughnut2, name='doughnutchart2'),
    path('histogramchart', views.histogramChart, name='histogramchart'),
    path('output',rep.output),

]