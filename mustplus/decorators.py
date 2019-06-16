"""
Hey, PyLint? SHUT UP
"""
# 使用此装饰器，请保证函数的第一个参数为request
import json

from django.http import HttpResponse

from settings import codes, messages

JSON_REQUEST_METHOD_ERROR = json.dumps(
    {"code": codes.AUTH_REQUEST_METHOD_ERROR, "msg": messages.AUTH_REQUEST_METHOD_ERROR})


# 强制 POST 方式请求
def require_post(func):
    def wrapper(*args, **kw):
        if args[0].method != "POST":
            return HttpResponse(JSON_REQUEST_METHOD_ERROR)
        return func(*args, **kw)

    return wrapper


# 强制 GET 方式请求
def require_get(func):
    def wrapper(*args, **kw):
        if args[0].method != "GET":
            return HttpResponse(JSON_REQUEST_METHOD_ERROR)
        return func(*args, **kw)

    return wrapper


# 检查请求参数签名（保证请求安全）
def check_signature(func):
    def wrapper(*args, **kw):
        return func(*args, **kw)

    return wrapper


# 敏感词检查
def check_sensitive_words(func):
    def wrapper(*args, **kw):
        return func(*args, **kw)

    return wrapper
