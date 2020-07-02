from django.urls import path
from . import views
# TEMPLATE_TAGGING
app_name = 'api_trace'
urlpatterns = [
   path('group/assets/', views.GroupAssets.as_view(), name="groupassets"),
   path('group/reports/', views.GroupReports.as_view(), name="groupreports"),
   path('assets/', views.Assets.as_view(), name="assets"),
   path('reports/', views.Reports.as_view(), name="reports"),
   path('email/', views.EmailListView.as_view(), name="searchemail"),
   path('cvvbinno/', views.CvvSearchBinNo.as_view(), name="cvvbinno"),
   path('cvvcountry/', views.CvvSearchCountry.as_view(), name="cvvcountry"),
   path('cvvbankname/', views.CvvSearchBankName.as_view(), name="cvvbankname"),
   path('cvvownername/', views.CvvSearchOwnerName.as_view(), name="cvvownername"),
   path('cvvzipno/', views.CvvSearchZipNo.as_view(), name="cvvzipno"),
   path('cvvcity/', views.CvvSearchCity.as_view(), name="cvvcity"),
   path('dumpbinno/', views.DumpSearchBinNo.as_view(), name="dumpbinno"),
   path('dumpcountry/', views.DumpSearchCountry.as_view(), name="dumpcountry"),
   path('dumpbankname/', views.DumpSearchBankName.as_view(), name="dumpbankname"),
   path('getcleanpassword', views.getPasswordByUsername, name="passwordusername"),
   path('emailinbreaches', views.checkEmailBreaches, name="emailbreaches"),
   path('pastesearchemail', views.pasteSearch, name="pastesearchemail"),
   path('getemailsbysha', views.getEmailsByHash, name="emailbyhashpassword"),
   path('upload', views.FileUploadView.as_view(), name="monitorEmails"),
   path('domain', views.initializeSingleDomainReport, name="singledomainreport"),
   path('register/domain', views.registerDomains, name="registerdomains"),
   path('report/<str:file>/', views.DomainReportPrintView.as_view(), name="domainreport"),
   path('delete',views.deleteDomain, name="deletedomain"),
   path('celery/reportlab/email', views.celeryReport, name="report"),
   path('celery/reportlab/domain', views.celeryReportDomain, name="reportdomain"),
   path('search', views.search, name="search"),
   path('download', views.download, name="download"),
]

