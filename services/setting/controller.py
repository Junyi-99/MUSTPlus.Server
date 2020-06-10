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
        if f.name == 'id' or f.name == 'student' or f.name=='nt_others': # nt_others 需要传入 str 类型数据，但set这个api只接受boolean数据，暂时不单独判断一条others
            continue
        settings[f.name] = f.value_from_object(set)
    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK,
        "settings": settings
    })

def __setting_set(stu: Student, setting: str, value) -> JsonResponse:
    set, created = Setting.objects.get_or_create(student=stu)

    for f in set._meta.get_fields():
        if f.name == setting:
            setattr(set, setting, value)
            set.save()
            return JsonResponse({
                "code": codes.OK,
                "msg": messages.OK,
            })
    return JsonResponse({
        "code": codes.SETTING_NO_SUCH_SETTING,
        "msg": messages.SETTING_NO_SUCH_SETTING,
    })
