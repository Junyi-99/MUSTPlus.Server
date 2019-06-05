import json
import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Services.Authentication import utility
from Services.Authentication.decorators import validate
from Services.Basic.COES.Timetable import get_html, get_timetable
from Services.Course.models import Course
from Settings import Codes, Messages

# Default timetable intake
TIMETABLE_INTAKE = 1902


@csrf_exempt
@validate
def timetable(request):
    stu = utility.get_student_object(request)

    intake = int(request.GET.get("intake", TIMETABLE_INTAKE))
    week = int(request.GET.get('week', -1))
    if week == -1:
        return HttpResponse(json.dumps({"code": Codes.TIMETABLE_WEEK_INVALID, "msg": Messages.TIMETABLE_WEEK_INVALID}))

    s = get_html("", stu.coes_cookie, intake, week)
    if s is None:
        return HttpResponse(json.dumps({"code": Codes.TIMETABLE_COOKIE_EXPIRED,
                                        "msg": Messages.TIMETABLE_COOKIE_EXPIRED}))
    try:
        r = get_timetable(s)

        for e in r:
            #print(e)
            try:
                Course.objects.get(intake=intake, course_code=e['course_id'], course_class=e['course_class'])
            except ObjectDoesNotExist:
                course = Course(
                    intake=intake,
                    course_code=e['course_id'],
                    course_class=e['course_class'],
                    name_zh=e['course_name_zh'],
                )
                course.save()
                print("Create a new Course [%d %s %s %s]"
                      % (course.intake, course.course_code, course.course_class, course.name_zh))


        return HttpResponse(json.dumps(r))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"code": Codes.TIMETABLE_UNKNOWN_EXCEPTION,
                                        "msg": Messages.TIMETABLE_UNKNOWN_EXCEPTION}))
