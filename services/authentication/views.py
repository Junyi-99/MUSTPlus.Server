import base64
import os
import re
import sys
import traceback
import uuid
from datetime import datetime, timedelta

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt

from mustplus.decorators import require_get, require_post
from services.authentication.decorators import validate
from services.basic.coes import login2 as coes_login
from services.basic.coes import student_info as stu_info
from services.basic.query import get_faculty, get_program, get_major
from services.student.models import Student
from settings import codes, messages
from settings.server import SEMESTER
from . import PUBLIC_KEY_CONTENT, decrypt
from .utility import get_student_object


@require_get
def get_hash(request):
    with open(os.path.dirname(os.path.realpath(__file__)) + '/captcha.png', 'rb') as f:
        captcha = f.read()
    return JsonResponse({
        'code': codes.OK,
        'msg': messages.OK,
        'key': PUBLIC_KEY_CONTENT,
        'captcha': base64.b64encode(captcha).decode('utf-8'),
    })

# 预计 2020 年 12 月 废弃当前接口，启用新登入方式
@csrf_exempt
@require_post
def login(request):
    return JsonResponse({
        'code': codes.SYSTEM_MAINTENANCE,
        'msg': '旧版本登入接口已不再支持，请升级您的 MUST+ 以获得更好的体验。很抱歉给您的学习生活带来不便。',
    })


# Junyi, 2020/10/11, finished
# 登陆i.must.edu.mo，存cookie到model里的coes_cookies字段
@csrf_exempt
@require_post
def login2(request):
    try:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username is None or password is None:
            return JsonResponse({
                'code': codes.LOGIN_FIELD_ERROR,
                'msg': messages.LOGIN_FIELD_ERROR,
            })

        username = decrypt(base64.b64decode(username))
        password = decrypt(base64.b64decode(password))
        if not username_check(username):
            return JsonResponse({
                'code': codes.LOGIN_USERNAME_INVALID,
                'msg': messages.LOGIN_USERNAME_INVALID
            })

        ret, cookies = coes_login.login(username, password)

        if ret == coes_login.LOGIN_SUCCESSFUL:
            print('User: %s, Login Successful' % (username,))
            stu, created = Student.objects.update_or_create(
                student_id=username,
                defaults={
                    'token': str(uuid.uuid1()),
                    'coes_cookie': cookies,
                    'token_expired_time': datetime.now(tz=pytz.UTC) + timedelta(hours=720)
                }
            )

            refresh_student_information(stu)
            # TODO: 先返回登入成功，在后台刷新用户信息（任务队列设想）
            return JsonResponse({
                'code': codes.OK,
                'msg': messages.OK,
                'student_name': stu.name_zh,
                'token': stu.token
            })

        ret_code = codes.LOGIN_OTHER_ERROR
        ret_msg = messages.LOGIN_OTHER_ERROR

        return JsonResponse({
            'code': ret_code,
            'msg': ret_msg,
            'detail': 'unknown error'
        })

    except Exception as exception:
        traceback.print_exc(file=sys.stdout)
        ret_code = codes.INTERNAL_ERROR
        ret_msg = messages.INTERNAL_ERROR
        if str(exception) == 'Incorrect padding' or str(exception) == 'Decryption failed':
            ret_code = codes.LOGIN_RSA_ERROR
            ret_msg = messages.LOGIN_RSA_ERROR
        return JsonResponse({
            'code': ret_code,
            'msg': ret_msg
        })


@csrf_exempt
@require_post
# @validate
def logout(request):
    stu = get_student_object(request)
    if stu is not None:
        stu.token = ''
        stu.coes_cookie = ''
        stu.coes_token = ''
        stu.save()
    return JsonResponse({
        'code': codes.OK,
        'msg': messages.OK
    })


def username_check(username: str):
    try:
        if len(username) != 18:
            return False
        match = re.search(r'\d{4}\w{4}-\w{4}-\d{4}', username)
        if match is None:
            return False
        return True
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return False


# 刷新用户信息
# Feature: 自动更新 Faculty Program Major 之间的关系（不存在自动创建，且保证依赖关系正确）
# 由外部 caller 去 handle exception
def refresh_student_information(student: Student):

    ret = stu_info.student_information(student.coes_cookie)
    student.name_zh = ret['name_zh']
    student.name_en = ret['name_en']
    student.gender = (ret['gender'] == '男')
    student.birthday = datetime.strptime(ret['birthday'], '%d/%m/%Y')
    student.birthplace = ret['birthplace']
    student.nationality = ret['nationality']

    # 检查faculty、program、major是否存在，不存在则自动创建
    student.faculty = get_faculty(ret['faculty'], True)
    student.program = get_program(ret['program'], True, student.faculty)
    student.major = get_major(ret['major'], True, student.program)
    student.save()

    # from services.timetable.controller import __timetable_update
    from services.gpa.controller import __gpa
    __gpa(student)
