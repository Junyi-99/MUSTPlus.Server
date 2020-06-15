import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from mustplus.decorators import require_get
from services.authentication.decorators import validate
from services.authentication.utility import get_student_object
from services.basic.models import Department, Faculty
from services.news.models import Announcement, Document, Attachment
from settings import codes, messages


@require_get
#@validate
def student_me(request):
    stu = get_student_object(request)
    if stu is None:
        return JsonResponse({
            "code": codes.STUDENT_INVALID,
            "msg": messages.STUDENT_INVALID
        })
    else:
        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK,
            "student_id": stu.student_id,
            "name_zh": stu.name_zh,
            "name_en": stu.name_en,
            "nickname": stu.nickname,
            "sign": stu.sign,
            "gender": stu.gender,
            "birthday": stu.birthday,
            "birthplace": stu.birthplace,
            "nationality": stu.nationality,
            "avatar_url": stu.avatar_url,
            "experience": stu.experience,  # 用户经验
            "token": stu.token,  # MUSTPlus Token
            "token_expired_time": stu.token_expired_time,  # token expired time
            "faculty": stu.faculty.name_zh,
            "program": stu.program.name_zh,
            "major": stu.major.name_zh
        })


@require_get
#@validate
def student_get(request, student_id):
    pass
