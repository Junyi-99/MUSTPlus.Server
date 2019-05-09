import base64

from django.views.decorators.csrf import csrf_exempt

from MUSTPlus.decorators import *
from django.http import HttpResponse

from . import public_key_content, decrypt
from Settings import Codes, Messages


# Author: Junyi
# Time: 2019/4/30
# Status: finished
@require_get
def hash(request):
    return HttpResponse(json.dumps({"code": Codes.OK, "msg": Messages.OK_MSG, "key": public_key_content}))


# TODO: finish this check function
def username_check(username: str):
    if len(username) != 18:
        return False


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        password = decrypt(base64.b64decode(password))
        print("username:", username)
        print("password:", password)

        if not username_check(username):
            return HttpResponse(json.dumps({"code": Codes.LOGIN_USERNAME_INVALID, "msg": Messages.LOGIN_USERNAME_INVALID_MSG}))
        # TODO: CHECK PASSWORD
    except Exception as e:
        # TODO: Using Logger to record the dangerous behavior
        if str(e) == "Incorrect padding":
            return HttpResponse(json.dumps({"code": Codes.LOGIN_RSA_ERROR, "msg": Messages.LOGIN_RSA_ERROR_MSG}))
        return HttpResponse(json.dumps({"code": Codes.INTERNAL_ERROR, "msg": Messages.INTERNAL_ERROR_MSG}))

    return HttpResponse(username + ", " + password)


# Author: Junyi
# Time: 2019/4/30
# Status: unfinished
@csrf_exempt
@require_post
def logout(request):
    return HttpResponse("")
