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

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

from Settings import Codes, Messages
from Spider import intranet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('intranet/update/normal', intranet.intranet_update_normal),
    path('intranet/update/more', intranet.intranet_update_more),
    path('auth/', include('Services.Authentication.urls')),
    path('basic/', include('Services.Basic.urls')),
    path('news/', include('Services.News.urls')),
]


def handle_500(request):
    return HttpResponse(json.dumps({"code": Codes.INTERNAL_ERROR, "msg": Messages.INTERNAL_ERROR}))


def handle_404(request):
    return HttpResponse(json.dumps({"code": Codes.PAGE_NOT_FOUND, "msg": Messages.PAGE_NOT_FOUND}))


handler404 = handle_404
handler500 = handle_500
