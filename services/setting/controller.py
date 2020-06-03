from django.core.exceptions import ObjectDoesNotExist
from django.db.models import BooleanField
from django.http import JsonResponse

from services.setting.models import Setting
from services.student.models import Student
from settings import codes, messages


def __setting_get(stu: Student) -> JsonResponse:
    set, created = Setting.objects.get_or_create(student=stu)
    settings = {}
    for f in set._meta.get_fields():
        if f.name == 'id' or f.name == 'student':
            continue
        settings[f.name] = f.value_from_object(set)
    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK,
        "settings": settings
    })

def __setting_set(stu: Student, settings: dict) -> JsonResponse:
    set = Setting.objects.update_or_create(student=stu)
    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK,
    })
