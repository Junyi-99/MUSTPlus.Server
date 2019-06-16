import base64
import re
import sys
import traceback
import uuid
from datetime import datetime, timedelta

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from mustplus.decorators import require_get, require_post
from services.authentication.decorators import validate
from services.basic.coes import login as coes_login
from services.basic.coes import student_info as stu_info
from services.basic.query import get_faculty, get_program, get_major
from services.student.models import Student
from settings import codes, messages
from . import PUBLIC_KEY_CONTENT, decrypt


@require_get
def get_hash(request):
    token, cookies = coes_login.get_token_cookies()
    captcha = coes_login.get_captcha(cookies)
    ret = {
        'code': codes.OK,
        'msg': messages.OK,
        'key': PUBLIC_KEY_CONTENT,
        'token': token,
        'cookies': cookies,
        'captcha': base64.b64encode(captcha).decode('utf-8')
    }
    return JsonResponse(ret)


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
def login(request):
    cookies = ''
    try:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        token = request.POST.get('token', None)
        cookies = request.POST.get('cookies', None)
        captcha = request.POST.get('captcha', None)

        check_list = (username, password, token, cookies, captcha)
        for i in range(5):
            if check_list[i] is None:
                return JsonResponse({
                    'code': codes.LOGIN_FIELD_ERROR,
                    'msg': messages.LOGIN_FIELD_ERROR,
                    'detail': i
                })

        username = decrypt(base64.b64decode(username))
        password = decrypt(base64.b64decode(password))
        token = decrypt(base64.b64decode(token))
        cookies = decrypt(base64.b64decode(cookies))
        captcha = decrypt(base64.b64decode(captcha))

        if not username_check(username):
            return JsonResponse({
                'code': codes.LOGIN_USERNAME_INVALID,
                'msg': messages.LOGIN_USERNAME_INVALID
            })

        ret = coes_login.login(username, password, token, cookies, captcha)

        if ret == coes_login.LOGIN_SUCCESSFUL:
            print('User: %s, Login Successful' % (username,))
            try:
                stu = Student.objects.get(student_id=username)
                stu.token = str(uuid.uuid1())
                stu.coes_token = token
                stu.coes_cookie = cookies
                stu.token_expired_time = datetime.now(tz=pytz.UTC) + timedelta(hours=720)  # 1 month
                stu.save()
            except ObjectDoesNotExist:  # New user, update user data
                stu = Student(
                    student_id=username,
                    token=str(uuid.uuid1()),
                    coes_token=token,
                    coes_cookie=cookies,
                    token_expired_time=datetime.now(tz=pytz.UTC) + timedelta(hours=720)
                )
                # stu.save()
                refresh_student_information(stu)
            # coes_login.logout(cookies)
            return JsonResponse({
                'code': codes.OK,
                'msg': messages.OK,
                'student_name': stu.name_zh,
                'token': stu.token
            })

        ret_code = codes.LOGIN_OTHER_ERROR
        ret_msg = messages.LOGIN_OTHER_ERROR
        ret_detail = ret
        if ret == coes_login.LOGIN_CAPTCHA_ERROR:
            ret_code = codes.LOGIN_CAPTCHA_ERROR
            ret_msg = messages.LOGIN_CAPTCHA_ERROR
        if ret == coes_login.LOGIN_OTHER_ERROR:
            ret_code = codes.LOGIN_FIELD_ERROR
            ret_msg = messages.LOGIN_FIELD_ERROR
        if ret == coes_login.LOGIN_PASSWORD_ERROR:
            ret_code = codes.LOGIN_PASSWORD_ERROR
            ret_msg = messages.LOGIN_PASSWORD_ERROR

        return JsonResponse({
            'code': ret_code,
            'msg': ret_msg,
            'detail': ret_detail
        })

    except Exception as exception:
        coes_login.logout(cookies)
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


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
@validate
def logout(request):
    return HttpResponse('')


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
def refresh_student_information(student: Student):
    print(student.coes_cookie)
    ret = stu_info.student_information(student.coes_cookie)
    print(ret)
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
