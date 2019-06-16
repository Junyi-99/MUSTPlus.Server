"""mustplus URL Configuration

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
import json

from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

from settings import codes, messages
from spider import intranet

urlpatterns = [
    url('admin/', admin.site.urls),
    path('intranet/update/normal', intranet.intranet_update_normal),
    path('intranet/update/more', intranet.intranet_update_more),

    path('auth/', include('services.authentication.urls')),
    path('basic/', include('services.basic.urls')),
    path('course/', include('services.course.urls')),
    path('news/', include('services.news.urls')),
    path('teacher/', include('services.teacher.urls')),
    path('timetable/', include('services.timetable.urls')),
]


def handle_500():
    return HttpResponse(json.dumps({"code": codes.INTERNAL_ERROR, "msg": messages.INTERNAL_ERROR}))


def handle_404():
    return HttpResponse(json.dumps({"code": codes.PAGE_NOT_FOUND, "msg": messages.PAGE_NOT_FOUND}))


handler404 = handle_404
handler500 = handle_500
