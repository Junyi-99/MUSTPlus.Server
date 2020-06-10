from datetime import datetime

import pytz
from django.core.exceptions import ObjectDoesNotExist

from services.basic.coes.gpa import get_gpa_list
from services.basic.models import ClassRoom
from services.course.models import Course
from services.gpa.models import GPA
from django.http import JsonResponse
from services.student.models import Student, TakeCourse

# 获取并更新 GPA
from settings import codes, messages


def __gpa(student: Student) -> JsonResponse:
    gpa_list = get_gpa_list(student.coes_cookie)  # 获取最新数据
    # 更新数据库内的数据 BEGIN
    for g in gpa_list:
        GPA.objects.update_or_create(student=student, intake=g['course_intake'],
                                     defaults={
                                         'total_credit': g["total_credit"],
                                         'pass_credit': g["pass_credit"],
                                         'fail_credit': g["fail_credit"],
                                         'gpa_credit': g["gpa_credit"],
                                         'gpa': g["gpa"],
                                         'accum_gpa': g["accum_gpa"],
                                         'update_time': datetime.now(tz=pytz.UTC)
                                     })
        for d in g['details']:
            # TODO: 创建的时候一起把中文名也创建了
            c, created = Course.objects.update_or_create(course_code=d['course_code'], course_class=d['course_class'],
                                                         defaults={
                                                             'credit': d['course_credit'],
                                                             'name_zh':d['course_name_zh']
                                                         })
            clsrm, created = ClassRoom.objects.get_or_create(name_zh=d['exam_classroom'])
            TakeCourse.objects.update_or_create(
                intake=int(g["course_intake"]),
                student=student,
                course=c,
                defaults={
                    'grade': d['grade'],
                    'course_code': d['course_code'],
                    'course_class': d['course_class'],
                    'course_credit': d['course_credit'],
                    'exam_datetime': None,
                    'exam_seat': d['exam_seat'],
                    'exam_classroom': clsrm,
                    # 时间关系，不写 exam_classroom 相关的东西了
                    # 时间关系，不写 grade_point 转换相关的东西了
                })
    # 更新数据库内的数据 END

    # 返回数据库内的数据
    result = []
    gpa_list_db = GPA.objects.filter(student=student)  # 获取数据库内的数据

    for g in gpa_list_db:
        course_gp = TakeCourse.objects.filter(student=student, intake=g.intake)
        gp_detail = []
        for gp in course_gp:
            #print(gp, gp.course.credit)
            gp_detail.append({
                "course_code": gp.course.course_code,
                "course_name_zh": gp.course.name_zh,
                "credit": gp.course.credit,
                "grade": gp.grade,
                "exam_datetime": gp.exam_datetime,
                "exam_classroom": gp.exam_classroom.name_zh,
                "exam_seat": gp.exam_seat,
            })
        result.append({
            "course_intake": g.intake,
            "total_credit": g.total_credit,
            "pass_credit": g.pass_credit,
            "fail_credit": g.fail_credit,
            "gpa_credit": g.gpa_credit,
            "gpa": g.gpa,
            "accum_gpa": g.accum_gpa,
            "details": gp_detail
        })

    return JsonResponse({
        'code': codes.OK,
        'msg': messages.OK,
        'gpa': result
    })
