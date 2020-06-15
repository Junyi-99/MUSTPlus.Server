import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from services.authentication.decorators import validate
from services.authentication.utility import get_student_object
from services.setting.controller import __setting_get, __setting_set
from services.setting.models import Setting
from services.student.models import Student
from settings import codes, messages


@csrf_exempt
# @validate
def api_setting(request):
    if request.method == "GET":
        stu = get_student_object(request)
        if stu is None:
           return JsonResponse({
               "code": codes.AUTH_TOKEN_INVALID,
               "msg": messages.AUTH_TOKEN_INVALID
           })
        return __setting_get(stu)
    elif request.method == "POST":
        try:
            stu = get_student_object(request)
            if stu is None:
                return JsonResponse({
                    "code": codes.AUTH_TOKEN_INVALID,
                    "msg": messages.AUTH_TOKEN_INVALID
                })
            setting = str(request.POST.get("setting", ''))
            value = int(request.POST.get("value", 0))
            if value == 0:
                return __setting_set(stu, setting, False)
            else:
                return __setting_set(stu, setting, True)
        except ValueError:
            return JsonResponse({'code': codes.INVALID_PARAM, 'msg': messages.INVALID_PARAM})

    return JsonResponse({'code': codes.AUTH_REQUEST_METHOD_ERROR, 'msg': messages.AUTH_REQUEST_METHOD_ERROR})
