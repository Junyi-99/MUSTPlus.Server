import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from services.authentication.decorators import validate
from services.authentication.utility import get_student_object
from services.setting.controller import __setting_get
from services.setting.models import Setting
from services.student.models import Student
from settings import codes, messages

#@validate
def api_setting(request):
    if request.method == "GET":
        #stu = get_student_object(request)
        #if stu is None:
        #    return JsonResponse({
        #        "code": codes.AUTH_TOKEN_INVALID,
        #        "msg": messages.AUTH_TOKEN_INVALID
        #    })
        stu = Student.objects.get(token='e2092d74-a5b3-11ea-9a64-52540062710c')
        return __setting_get(stu)
    elif request.method == "POST":
        return JsonResponse({'code': 0, 'msg': ''})
    return JsonResponse({'code': codes.AUTH_REQUEST_METHOD_ERROR, 'msg': messages.AUTH_REQUEST_METHOD_ERROR})
