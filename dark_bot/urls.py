"""dark_bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from dark_bot import views
from django.contrib.auth import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    # path('', v.LoginView.as_view(redirect_authenticated_user=True), name="login1"), # cemment this line for uni
    path('contact/', views.contact, name="contact"),
    path('search/', include('search.urls')),
    path('user/', include('accounts.urls')),
    path('adminpanel/', include('adminpanel.urls')),
    path('login/', v.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path('logout/',v.LogoutView.as_view(next_page='/'),name="logout"),
    path('userdashboard/',include('userdashboard.urls')),
    path('gatherdata/', include('gatherdumps.urls')),
    path('api/user/', include('accounts.api.urls')),
    path('api/trace/', include('search.api.urls')),
    path('download/', views.download, name="download"),
    # path('dashboard/', include('dashboard.urls')),
]