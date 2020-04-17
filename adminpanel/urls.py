from django.conf.urls import url
from django.urls import path
from adminpanel import views,rep

# TEMPLATE_TAGGING


app_name = 'adminpanel'
urlpatterns = [
    path('message', views.message, name='message'),
    path('message/delete/<int:id>/', views.deleteMessage, name='deletemsg'),
    path('profile/',views.profile,name='profile'),
    path('', views.index, name='dashboard'),
    path('email/monitoring',views.monitorEmail, name="emailmonitoring"),
    path('domain/monitoring',views.monitorDomain, name="domainmonitoring"),
    path('monitoring',views.monitor, name="monitoring"),
    path('subscription/request', views.RequestListView.as_view(login_url='/login'), name='request'),
    url('subscription/(?P<pk>\d+)/$', views.RequestDetailView.as_view(login_url='/login'), name='detail'),
    url('subscription/deleterequest/(?P<pk>\d+)/$', views.RequestDeleteView.as_view(login_url='/login'), name='delete'),
    url('linechart', views.LineChartJSONView.as_view(), name="linechart"),
    url('doughnutchart', views.DoughnutChart, name="doughnutchart"),
    url('histogramchart', views.HistogramChart, name="histogramchart"),
    url('polarchart', views.PolarChart, name="polarchart"),
    url('activeuserchart', views.ActiveUserChart, name="activeuserchart"),
    path('output', rep.output),
    path('generate/report',views.generateReport, name="reportgeneration"),
    path('report/domain',views.domainReport, name="domainreport"),
    path('show/report',views.showReports, name="showreports"),
    path('test',views.test, name="test"),

]