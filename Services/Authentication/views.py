import base64
import json
import uuid
import re
import traceback
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt

from Services.Basic.models import Student, Faculty, Major, Program
from . import public_key_content, decrypt
from Settings import Codes, Messages
from MUSTPlus.decorators import require_get, require_post
from django.http import HttpResponse
from Services.Authentication.COES import COES


@require_get
def hash(request):
    token, cookies = COES.get_token_cookies()
    captcha = COES.captcha(cookies)
    ret = {
        "code": Codes.OK,
        "msg": Messages.OK,
        "key": public_key_content,
        "token": token,
        "cookies": cookies,
        "captcha": base64.b64encode(captcha).decode('utf-8')
    }
    return HttpResponse(json.dumps(ret))


def username_check(username: str):
    try:
        if len(username) != 18:
            return False
        m = re.search(r'\d{4}\w{4}-\w{4}-\d{4}', username)
        if m is None:
            return False
        return True
    except Exception as e:
        print(e)
        return False


def get_faculty_by_name(faculty: str) -> Faculty:
    try:
        r = Faculty.objects.get(name_zh=faculty)
        return r
    except ObjectDoesNotExist:
        print("!!! Not found Faculty")  # 写到日志里去
        return None
    except Exception as e:
        print(e)
        return None


@csrf_exempt
@require_post
def refresh(request):
    username = request.POST.get('username', None)
    if username is None:
        return HttpResponse(
            json.dumps({"code": Codes.MISSING_FIELD, "msg": Messages.MISSING_FIELD, "detail": "username"}))
    return refresh_student_information(username)


def refresh_student_information(username):
    try:
        stu = Student.objects.get(student_id=username)
        print("COES:COOKIE:", stu.coes_cookie)
        ret = COES.student_information(stu.coes_cookie)
        print(ret['name_zh'], ret['name_en'], ret['birthplace'])
        stu.name_zh = ret['name_zh']
        stu.name_en = ret['name_en']
        stu.gender = True if ret['gender'] == '男' else False

        stu.birthday = datetime.strptime(ret['birthday'], '%d/%m/%Y')
        stu.birthplace = ret['birthplace']
        stu.nationality = ret['nationality']
        try:
            stu.faculty = Faculty.objects.get(name_zh=ret['faculty'])
        except ObjectDoesNotExist:
            stu.faculty = None
            print("Can not find " + ret['faculty'])
        try:
            stu.program = Program.objects.get(name_zh=ret['program'])
        except ObjectDoesNotExist:
            stu.program = None
        try:
            stu.major = Major.objects.get(name_zh=ret['major'])
        except ObjectDoesNotExist:
            stu.major = None

        stu.save()

    except ObjectDoesNotExist:
        print("Exception in refresh_student_information():", "ObjectDoesNotExist")
        return HttpResponse(
            json.dumps({"code": Codes.PROFILE_REFRESH_USER_NOT_FOUND, "msg": Messages.PROFILE_REFRESH_USER_NOT_FOUND}))
    except Exception as e:

        print("Exception in refresh_student_information():", e)
        return HttpResponse(
            json.dumps({"code": Codes.INTERNAL_ERROR, "msg": Messages.INTERNAL_ERROR})
        )


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
def login(request):
    try:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        token = request.POST.get('token', None)
        cookies = request.POST.get('cookies', None)
        captcha = request.POST.get('captcha', None)
        check_list = (username, password, token, cookies, captcha)
        for i in range(5):
            if check_list[i] is None:
                return HttpResponse(
                    json.dumps({"code": Codes.LOGIN_FIELD_ERROR, "msg": Messages.LOGIN_FIELD_ERROR, "detail": i}))

        username = decrypt(base64.b64decode(username))
        password = decrypt(base64.b64decode(password))
        token = decrypt(base64.b64decode(token))
        cookies = decrypt(base64.b64decode(cookies))
        captcha = decrypt(base64.b64decode(captcha))

        print("username:", username)
        print("password:", password)
        print("token:", token)
        print("cookies:", cookies)
        print("captcha:", password)

        if not username_check(username):
            return HttpResponse(
                json.dumps({"code": Codes.LOGIN_USERNAME_INVALID, "msg": Messages.LOGIN_USERNAME_INVALID}))

        ret = COES.login(username, password, token, cookies, captcha)

        if ret == COES.LOGIN_SUCCESSFUL:
            print("User: %s, Login Successful" % (username,))
            try:
                stu = Student.objects.get(student_id=username)
                stu.token = str(uuid.uuid1())
                stu.coes_cookie = cookies
                stu.token_expired_time = datetime.now() + timedelta(hours=720)  # 720 hours = 1 month
                stu.save()
            except ObjectDoesNotExist:  # New user, update user data
                stu = Student(
                    student_id=username,
                    token=str(uuid.uuid1()),
                    coes_cookie=cookies,
                    token_expired_time=datetime.now() + timedelta(hours=720)
                )
                stu.save()
                refresh_student_information(username)
            COES.logout(cookies)
            return HttpResponse(json.dumps({"code": Codes.OK, "msg": Messages.OK}))
        else:
            print("Login failed")
            return HttpResponse(json.dumps({"code": Codes.LOGIN_PASSWORD_ERROR, "msg": Messages.LOGIN_PASSWORD_ERROR}))

    except Exception as e:
        # TODO: Using Logger to record the dangerous behavior
        print(e)
        if str(e) == "Incorrect padding":
            return HttpResponse(json.dumps({"code": Codes.LOGIN_RSA_ERROR, "msg": Messages.LOGIN_RSA_ERROR}))
        if str(e) == "Decryption failed":
            return HttpResponse(json.dumps({"code": Codes.LOGIN_RSA_ERROR, "msg": Messages.LOGIN_RSA_ERROR}))
        COES.logout(cookies)
        return HttpResponse(json.dumps({"code": Codes.INTERNAL_ERROR, "msg": Messages.INTERNAL_ERROR}))


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
def logout(request):
    return HttpResponse("")
