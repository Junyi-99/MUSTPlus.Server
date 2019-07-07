# 使用此装饰器，请保证函数的第一个参数为request
import hashlib
import json
import sys
import time
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone

from services.student.models import Student
from settings import codes, messages
from settings.server import AUTH_SECRET

TOKEN_ERROR = json.dumps({"code": codes.AUTH_TOKEN_INVALID, "msg": messages.AUTH_TOKEN_INVALID})


# 验证用户请求
# 通过 func 的第一个参数 request.GET 中的 token time sign 三个参数进行验证
def validate(func):
    def wrapper(*args, **kwargs):

        try:
            token_get = str(args[0].GET.get('token', ""))
            time_get = int(args[0].GET.get('time', 0))
            sign_get = str(args[0].GET.get('sign', ""))

            if (token_get == "") or (time_get == 0) or (sign_get == ""):
                raise ValueError

            # sort GET parameter list
            get_params = ""
            for element in sorted(args[0].GET):
                if element == 'sign':  # except `sign`
                    continue
                get_params = get_params + element + "=" + str(args[0].GET[element]) + "&"
            get_params = get_params[:-1]

            # sort POST parameter list
            post_params = ""
            for element in sorted(args[0].POST):
                post_params = post_params + element + "=" + str(args[0].POST[element]) + "&"
            post_params = post_params[:-1]

            # calculate sign
            param_list = get_params + post_params + AUTH_SECRET
            sign_calc = hashlib.md5(param_list.encode('utf-8')).hexdigest()

            # check sign
            if sign_calc != sign_get:
                print("Sign invalid!", "get:", sign_get, "require:", sign_calc)
                return JsonResponse({
                    "code": codes.AUTH_SIGN_VERIFICATION_FAILED,
                    "msg": messages.AUTH_SIGN_VERIFICATION_FAILED
                })

            # check time
            if abs(int(time.time()) - int(time_get)) > 5 * 60:
                print("Time invalid!", "now:", int(time.time()), "get:", time_get)
                return JsonResponse({
                    "code": codes.AUTH_TIME_INVALID,
                    "msg": messages.AUTH_TIME_INVALID
                })

            # check token

            obj_student = Student.objects.get(token=token_get)
            if obj_student.token_expired_time < timezone.now():
                print("Token", token_get, "expired")
                raise ObjectDoesNotExist

            return func(*args, **kwargs)
        except ObjectDoesNotExist:  # occurs only when Student does not exist
            return JsonResponse({
                "code": codes.AUTH_TOKEN_INVALID,
                "msg": messages.AUTH_TOKEN_INVALID
            })
        except ValueError:
            return JsonResponse({
                "code": codes.AUTH_VALIDATE_ARGUMENT_ERROR,
                "msg": messages.AUTH_VALIDATE_ARGUMENT_ERROR
            })
        except Exception as exception:
            print(exception)
            traceback.print_exc(file=sys.stdout)
            return JsonResponse({
                "code": codes.AUTH_UNKNOWN_ERROR,
                "msg": messages.AUTH_UNKNOWN_ERROR
            })

    return wrapper
