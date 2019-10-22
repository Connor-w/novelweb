"""connorshare URL Configuration

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
from django.urls import path, re_path, include
# xadmin的依赖
import xadmin
from django.views.static import serve

xadmin.autodiscover()
# xversion模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()
from connorshare import settings
from . import views


urlpatterns = [
    re_path('^login.html',views.LoginAPIView.as_view()),
    re_path('^register.html',views.RegisterAPIView.as_view()),
    re_path('^get_code/$',views.get_code),
    re_path('^site.html$',views.SiteAPIView.as_view()),
    re_path('^loginout$',views.loginout),



]
