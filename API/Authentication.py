import json
from MUSTPlus.decorators import *
from django.http import HttpResponse

from . import private_key, public_key_content

@require_get
def hash(request):
    return HttpResponse(json.dumps({"code": 0, "msg": "", "key": public_key_content}))

@require_post
def login(request):



    return HttpResponse("")

@require_post
def logout(request):
    return HttpResponse("")
