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

from services.bus.views import api_bus
from services.setting.views import api_setting
from services.timetable.views import api_timetable
from services.gpa.views import api_gpa


urlpatterns = [
    url('admin/', admin.site.urls),
    path('intranet/update/normal', intranet.intranet_update_normal),
    path('intranet/update/more', intranet.intranet_update_more),
    path('student/', include('services.student.urls'),name='学生信息'),
    path('auth/', include('services.authentication.urls'), name='鉴权服务'),
    path('basic/', include('services.basic.urls'), name='基本数据(API)'),
    path('course/', include('services.course.urls'), name='课程信息'),
    path('news/', include('services.news.urls'), name='新闻资讯'),
    path('teacher/', include('services.teacher.urls'), name='教师信息'),
    path('border/', include('services.border.urls'), name='关闸信息'),
    path('lost/', include('services.border.urls'), name='失物招领'),
    path('timetable', api_timetable, name='课程表'),
    path('setting', api_setting, name='用户设置'),
    path('bus', api_bus, name='巴士报站'),
    path('gpa', api_gpa, name='学生GPA'),
]

def handle_500(request, *args, **kwargs):
    return HttpResponse(content=json.dumps(
        {
            "code": codes.INTERNAL_ERROR,
            "msg": messages.INTERNAL_ERROR
        }
    ), status=500)


def handle_404(request, *args, **kwargs):
    return HttpResponse(content=json.dumps(
        {
            "code": codes.PAGE_NOT_FOUND,
            "msg": messages.PAGE_NOT_FOUND
        }
    ), status=404)


handler404 = handle_404
handler500 = handle_500
