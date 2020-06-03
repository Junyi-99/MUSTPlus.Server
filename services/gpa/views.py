from django.http import HttpResponse, JsonResponse

from mustplus.decorators import require_get
from services.authentication import utility
from services.authentication.decorators import validate
from services.gpa.controller import __gpa
from settings import codes, messages


@require_get
#@validate
def api_gpa(request):
    stu = utility.get_student_object(request) # 有 validate 就不用再次验证 stu 是否为空
    if stu is None: # 这里写判断是为了方便调试
        return JsonResponse({
            "code": codes.AUTH_TOKEN_INVALID,
            "msg": messages.AUTH_TOKEN_INVALID
        })
    return __gpa(stu)