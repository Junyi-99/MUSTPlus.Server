"""MUSTPlus URL Configuration

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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from Settings import Codes, Messages
from Spider import intranet

api_info = openapi.Info(
    title="Snippets API",
    default_version="2.0"
)

schema_view = get_schema_view(
    openapi.Info(
        title="MUSTPlus API",
        default_version='v1',
        description="MSUTPlus Android/iOS 共用 API。阅读本文档你可以了解到API的使用方法以及注意事项。",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="me@junyi.pw"),
        license=openapi.License(name="GPLv3"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url('admin/', admin.site.urls),
    path('intranet/update/normal', intranet.intranet_update_normal),
    path('intranet/update/more', intranet.intranet_update_more),

    path('auth/', include('Services.Authentication.urls')),
    path('basic/', include('Services.Basic.urls')),
    path('course/', include('Services.Course.urls')),
    path('news/', include('Services.News.urls')),
    path('teacher/', include('Services.Teacher.urls')),
    path('timetable/', include('Services.Timetable.urls')),
]


def handle_500(request):
    return HttpResponse(json.dumps({"code": Codes.INTERNAL_ERROR, "msg": Messages.INTERNAL_ERROR}))


def handle_404(request):
    return HttpResponse(json.dumps({"code": Codes.PAGE_NOT_FOUND, "msg": Messages.PAGE_NOT_FOUND}))


handler404 = handle_404
handler500 = handle_500
