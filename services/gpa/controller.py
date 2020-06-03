from datetime import datetime

import pytz
from django.core.exceptions import ObjectDoesNotExist

from services.basic.coes.gpa import get_gpa_list
from services.gpa.models import GPA
from django.http import JsonResponse
from services.student.models import Student

# 获取并更新 GPA
from settings import codes, messages


def __gpa(student: Student) -> JsonResponse:
    gpa_list = get_gpa_list(student.coes_cookie)  # 获取最新数据

    # 更新数据库内的数据 BEGIN
    for e in gpa_list:
        try:
            gpa = GPA.objects.get(
                student=student,
                intake=e["course_intake"],
            )
            gpa.total_credit = e["total_credit"]
            gpa.pass_credit = e["pass_credit"]
            gpa.fail_credit = e["fail_credit"]
            gpa.gpa_credit = e["gpa_credit"]
            gpa.gpa = e["gpa"]
            gpa.accum_gpa = e["accum_gpa"]
            gpa.update_time = datetime.now(tz=pytz.UTC)
            gpa.save()
        except ObjectDoesNotExist:
            gpa = GPA(
                student=student,
                intake=e["course_intake"],
                total_credit=e["total_credit"],
                pass_credit=e["pass_credit"],
                fail_credit=e["fail_credit"],
                gpa_credit=e["gpa_credit"],
                gpa=e["gpa"],
                accum_gpa=e["accum_gpa"],
            )
            gpa.save()
    # 更新数据库内的数据 END

    # 返回数据库内的数据
    result = []
    gpa_list_db = GPA.objects.get(student=student)  # 获取数据库内的数据
    for e in gpa_list_db:
        result.append({
            "course_intake": e.intake,
            "total_credit": e.total_credit,
            "pass_credit": e.pass_credit,
            "fail_credit": e.fail_credit,
            "gpa_credit": e.gpa_credit,
            "gpa": e.gpa,
            "accum_gpa": e.accum_gpa
        })
    return JsonResponse({
        'code': codes.OK,
        'msg': messages.OK,
        'gpa': result
    })
