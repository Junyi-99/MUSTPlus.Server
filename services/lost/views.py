import sys
import traceback

from django.http import JsonResponse


def api_settings(request):
    return JsonResponse({'code':0,'msg':''})