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
from services.basic.coes import login as coes_login
from services.basic.coes import student_info as stu_info
from services.basic.query import get_faculty, get_program, get_major
from services.student.models import Student
from settings import codes, messages
from settings.server import SEMESTER
from . import PUBLIC_KEY_CONTENT, decrypt
from .utility import get_student_object


@require_get
def get_hash(request):
    # dev_wyd = Student.objects.get(name_zh='王一丁')
    # dev_hqr = Student.objects.get(name_zh='黄启瑞')
    # dev_yzx = Student.objects.get(name_zh='严宗迅')
    # dev_hjy = Student.objects.get(name_zh='侯君宜')
    #
    # return JsonResponse({
    #     'code': codes.SYSTEM_MAINTENANCE,
    #     'msg': '系统维护中，暂时禁止用户登录',
    #     'developers': [
    #         {
    #             'name': '王一丁',
    #             'token': dev_wyd.token
    #         }, {
    #             'name': '黄启瑞',
    #             'token': dev_hqr.token
    #         }, {
    #             'name': '严宗迅',
    #             'token': dev_yzx.token
    #         }, {
    #             'name': '侯君宜',
    #             'token': dev_hjy.token
    #         }
    #     ]
    # })

    times = 999 # default is 0
    token = 'COES维护中'
    cookies = 'COES维护中'




    while times < 5 and not cookies:
        token, cookies = coes_login.get_token_cookies()
        times = times + 1
        print("Retry to get cookies")

    if not cookies:
        ret = {
            'code': codes.WARNING,
            'msg': '获取基本信息失败'
        }
    else:
        # captcha = coes_login.get_captcha(cookies)
        captcha = 'COES维护'
        with open(os.path.dirname(os.path.realpath(__file__))+'/captcha.png', 'rb') as f:
            captcha = f.read()
        ret = {
            'code': codes.OK,
            'msg': messages.OK,
            'key': PUBLIC_KEY_CONTENT,
            'token': token,
            'cookies': cookies,
            'captcha': base64.b64encode(captcha).decode('utf-8'),
        }

    return JsonResponse(ret)


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
def login(request):
    # dev_wyd = Student.objects.get(name_zh='王一丁')
    # dev_hqr = Student.objects.get(name_zh='黄启瑞')
    # dev_yzx = Student.objects.get(name_zh='严宗迅')
    # dev_hjy = Student.objects.get(name_zh='侯君宜')
    #
    # return JsonResponse({
    #     'code': codes.SYSTEM_MAINTENANCE,
    #     'msg': '系统维护中，暂时禁止用户登录',
    #     'developers':[
    #         {
    #             'name':'王一丁',
    #             'token':dev_wyd.token
    #         },{
    #             'name':'黄启瑞',
    #             'token':dev_hqr.token
    #         },{
    #             'name':'严宗迅',
    #             'token':dev_yzx.token
    #         },{
    #             'name':'侯君宜',
    #             'token':dev_hjy.token
    #         }
    #     ]
    # })

    cookies = ''
    try:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        token = request.POST.get('token', None)
        cookies = request.POST.get('cookies', None)
        captcha = request.POST.get('captcha', None)

        # print("USERNAME", username)
        # print("PASSWORD", password)
        # print("TOKEN", token)

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

        # 测试账号
        if username == '1' and password == '1':
            stu, created = Student.objects.update_or_create(
                student_id='1709853D-I011-0021',
                defaults={
                    'token': 'hjy',
                    'coes_token': 'Demo Account',
                    'coes_cookie': 'Demo Account',
                    'token_expired_time': datetime.now(tz=pytz.UTC) + timedelta(hours=720)
                })
            return JsonResponse({
                'code': codes.OK,
                'msg': messages.OK,
                'student_name': stu.name_zh,
                'token': stu.token
            })
        # 测试账号





        if not username_check(username):
            return JsonResponse({
                'code': codes.LOGIN_USERNAME_INVALID,
                'msg': messages.LOGIN_USERNAME_INVALID
            })




        # 测试账号
        if username == '1709853J-I011-0140' and password == '1':
            stu, created = Student.objects.update_or_create(
                student_id='1709853J-I011-0140',
                defaults={
                    'token': 'yzx',
                    'coes_token': 'Demo Account',
                    'coes_cookie': 'Demo Account',
                    'token_expired_time': datetime.now(tz=pytz.UTC) + timedelta(hours=720)
                })
            return JsonResponse({
                'code': codes.OK,
                'msg': messages.OK,
                'student_name': stu.name_zh,
                'token': stu.token
            })
        if username == '1709853J-I011-0053' and password == '1':
            stu, created = Student.objects.update_or_create(
                student_id='1709853J-I011-0053',
                defaults={
                    'token': 'hqr',
                    'coes_token': 'Demo Account',
                    'coes_cookie': 'Demo Account',
                    'token_expired_time': datetime.now(tz=pytz.UTC) + timedelta(hours=720)
                })
            return JsonResponse({
                'code': codes.OK,
                'msg': messages.OK,
                'student_name': stu.name_zh,
                'token': stu.token
            })
        # 测试账号




        ret = coes_login.login(username, password, token, cookies, captcha)

        if ret == coes_login.LOGIN_SUCCESSFUL:
            print('User: %s, Login Successful' % (username,))

            my_token = ''
            if username == '1709853D-I011-0021':
                my_token = 'hjy'
            elif username == '1709853J-I011-0053':
                my_token = 'hqr'
            elif username == '1709853J-I011-0140':
                my_token = 'yzx'
            elif username == '1709853J-I011-0152':
                my_token = 'wyd'
            if my_token == '':
                my_token = str(uuid.uuid1())

            stu, created = Student.objects.update_or_create(
                student_id=username,
                defaults={
                    #'token': str(uuid.uuid1()),
                    'token':my_token,
                    'coes_token': token,
                    'coes_cookie': cookies,
                    'token_expired_time': datetime.now(tz=pytz.UTC) + timedelta(hours=720)
                }
            )
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
        if ret == coes_login.LOGIN_STUDENT_ID_DOES_NOT_EXIST:
            ret_code = codes.LOGIN_USERNAME_INVALID
            ret_msg = messages.LOGIN_USERNAME_INVALID
        if ret == coes_login.LOGIN_OTHER_ERROR:
            ret_code = codes.LOGIN_OTHER_ERROR
            ret_msg = messages.LOGIN_OTHER_ERROR
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
def refresh_student_information(student: Student):
    try:
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

    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
