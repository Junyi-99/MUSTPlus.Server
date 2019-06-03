# 使用此装饰器，请保证函数的第一个参数为request
import hashlib
import json
import time

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# 强制 POST 方式请求
from django.utils import timezone

from Services.Student.models import Student
from Settings import Codes, Messages

TOKEN_ERROR = json.dumps({"code": Codes.AUTH_TOKEN_INVALID, "msg": Messages.AUTH_TOKEN_INVALID})


# 验证用户请求
# 通过 func 的第一个参数 request.GET 中的 token time sign 三个参数进行验证
def validate(func):
    def wrapper(*args, **kwargs):

        try:
            token_get = str(args[0].GET.get('token', ""))
            time_get = int(args[0].GET.get('time', 0))
            sign_get = str(args[0].GET.get('sign', ""))
            if (token_get is "") or (time_get == 0) or (sign_get is ""):
                return HttpResponse(json.dumps({
                    "code": Codes.AUTH_VALIDATE_ARGUMENT_ERROR,
                    "msg": Messages.AUTH_VALIDATE_ARGUMENT_ERROR
                }))
            print(token_get, time_get, sign_get)

            # sort GET parameter list
            get_para = ""
            for e in sorted(args[0].GET):
                if e == 'sign':  # except `sign`
                    continue
                get_para = get_para + e + "=" + args[0].GET[e] + "&"
            get_para = get_para[:-1]

            # sort POST parameter list
            post_para = ""
            for e in sorted(args[0].POST):
                post_para = post_para + e + "=" + args[0].POST[e] + "&"
            post_para = post_para[:-1]

            # calculate sign
            param_list = get_para + post_para
            sign_calc = hashlib.md5(param_list.encode('utf-8')).hexdigest()

            # check sign
            if sign_calc != sign_get:
                print("Sign invalid!", "get:", sign_get, "require:", sign_calc)
                return HttpResponse(json.dumps(
                    {"code": Codes.AUTH_SIGN_VERIFICATION_FAILED, "msg": Messages.AUTH_SIGN_VERIFICATION_FAILED}))

            # check time
            if abs(int(time.time()) - int(time_get)) > 5 * 60:
                print("Time invalid!", "now:", int(time.time()), "get:", time_get)
                return HttpResponse(json.dumps({"code": Codes.AUTH_TIME_INVALID, "msg": Messages.AUTH_TIME_INVALID}))

            # check token
            try:
                stu = Student.objects.get(token=token_get)
                if stu.token_expired_time < timezone.now():
                    print("Token", token_get, "expired")
                    return HttpResponse(
                        json.dumps({"code": Codes.AUTH_TOKEN_INVALID, "msg": Messages.AUTH_TOKEN_INVALID}))
            except ObjectDoesNotExist:
                return HttpResponse(json.dumps({"code": Codes.AUTH_TOKEN_INVALID, "msg": Messages.AUTH_TOKEN_INVALID}))

            return func(*args, **kwargs)

        except ValueError:
            return HttpResponse(
                json.dumps({
                    "code": Codes.AUTH_VALIDATE_ARGUMENT_ERROR,
                    "msg": Messages.AUTH_VALIDATE_ARGUMENT_ERROR
                }))
        except Exception as e:
            # TODO: Logger
            print(e)
            return HttpResponse(json.dumps({"code": Codes.AUTH_UNKNOWN_ERROR, "msg": Messages.AUTH_UNKNOWN_ERROR}))

    return wrapper
