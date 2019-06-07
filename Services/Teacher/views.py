import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from MUSTPlus.decorators import require_get
from Services.Authentication.decorators import validate
from Services.Teacher.models import Teacher, TeachCourse
from Settings import Codes, Messages


@require_get
@validate
def api_teacher(request, name_zh):
    try:
        teacher = Teacher.objects.get(name_zh=name_zh)
        teaches = TeachCourse.objects.filter(teacher=teacher).order_by('-intake')
        courses = []
        for teach in teaches:
            courses.append({
                "intake": teach.intake,
                "course_code": teach.course.course_code,
                "name_zh": teach.course.name_zh,
                "credit": teach.course.credit,
                "faculty": teach.course.faculty
            })
        return HttpResponse(json.dumps({
            "code": Codes.OK,
            "msg": Messages.OK,
            "name_zh": teacher.name_zh,
            "name_en": teacher.name_en,
            "faculty": teacher.faculty.name_zh,
            "avatar_url": teacher.avatar_url,
            "position": teacher.position,
            "email": teacher.email,
            "office_room": teacher.office_room,
            "office_hour": teacher.office_hour,
            "courses": courses
        }))
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({
            "code": Codes.TEACHER_ID_NOT_FOUNT,
            "msg": Messages.TEACHER_ID_NOT_FOUNT
        }))
