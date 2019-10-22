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
xadmin.autodiscover()
# xversion模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from book import views


urlpatterns = [
    re_path(r'^(?P<pk>\d+).html', views.book_info),
    re_path(r'^vote/(?P<book_pk>\d+)$', views.vote),
    re_path(r'^category/(?P<pk>\d*).html', views.category),
    re_path(r'^search/(?P<book_name>.*).html', views.search),
    re_path(r'^section/(?P<book_pk>\d+)/(?P<num>\d*)/(?P<num2>\d*).html', views.section),
    re_path(r'^catalog/(?P<book_pk>\d+).html', views.catalog),
    re_path(r'^video.html', views.video),
    re_path(r'^ranking.html', views.ranking),
    re_path(r'^book_rack/(?P<book_pk>\d+)', views.book_rack),


    # re_path(r'^(?P<pk>).html', views.index),
]
