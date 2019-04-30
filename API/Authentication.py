import json
import base64

from django.views.decorators.csrf import csrf_exempt

from MUSTPlus.decorators import *
from django.http import HttpResponse

from . import private_key, public_key_content, decrypt
from MUSTPlus.codes import *
from MUSTPlus.msg_zh import *


# Author: Junyi
# Time: 2019/4/30
# Status: finished
@require_get
def hash(request):
    return HttpResponse(json.dumps({"code": 0, "msg": "", "key": public_key_content}))


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']

        print(username)
        print(decrypt(base64.b64decode(password)))
    except Exception as e:
        return HttpResponse(json.dumps({"code": INTERNAL_ERROR, "msg": INTERNAL_ERROR_MSG}))

    return HttpResponse("")


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
def logout(request):
    return HttpResponse("")
