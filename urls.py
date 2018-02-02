"""wxweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from wxweb.handle import handle
from wxweb.home import homePage
from wxweb.index import paintingShow
from wxweb.index import shareImage
from wxweb.index import uploadImage
from wxweb.index import showHisChat

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', homePage),
    url('^wx/?$', handle),
    url('^wx/index/?$', paintingShow),
    url('^wx/shareImage/?$', shareImage),
    url('^wx/uploadImg/?$', uploadImage),
    url('^wx/showHisChat/?$', showHisChat)
]
