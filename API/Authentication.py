from django.http import HttpResponse


def hash(request):
    return HttpResponse("Hello World")


def login(request):
    return HttpResponse("")


def logout(request):
    return HttpResponse("")
