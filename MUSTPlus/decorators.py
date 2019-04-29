# 使用此装饰器，请保证函数的第一个参数为request
from django.http import HttpResponse
from django.shortcuts import render


def check_post(func):
    def wrapper(*args, **kw):
        if args[0].method != "POST":
            return HttpResponse({"code":0, "msg":""})
        else:
            return func(*args, **kw)
    return wrapper

def check_get(func):
    def wrapper(*args, **kw):
        if args[0].method != "GET":
            return HttpResponse({"code":0, "msg":""})
        else:
            return func(*args, **kw)
    return wrapper