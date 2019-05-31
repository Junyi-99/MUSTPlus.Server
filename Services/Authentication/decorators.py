# 使用此装饰器，请保证函数的第一个参数为request
import json

from django.http import HttpResponse
# 强制 POST 方式请求
from django.utils.datastructures import MultiValueDictKeyError

from Settings import Codes, Messages

TOKEN_ERROR = json.dumps({"code": Codes.AUTH_TOKEN_INVALID, "msg": Messages.AUTH_TOKEN_INVALID})


def validate(func):
    def wrapper(*args, **kwargs):
        try:
            token = args[0].GET['token']
            time = args[0].GET['time']
            sign = args[0].GET['sign']
        except MultiValueDictKeyError:
            return HttpResponse(
                json.dumps({
                    "code": Codes.AUTH_VALIDATE_ARGUMENT_ERROR,
                    "msg": Messages.AUTH_VALIDATE_ARGUMENT_ERROR
                }))
        if args[0].method != "POST":
            return HttpResponse("")
        else:
            return func(*args, **kwargs)

    return wrapper
