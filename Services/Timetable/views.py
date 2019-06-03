import json
import sys
import traceback

from django.http import HttpResponse

from Services.Authentication import utility
from Services.Authentication.decorators import validate
from Services.Basic.COES.Timetable import get_html, get_timetable
from Services.Course.models import Course
from Settings import Codes, Messages


@validate
def timetable(request):
    stu = utility.get_student_object(request)
    intake = int(request.GET.get("intake", 1902))
    week = int(request.GET.get('week', 0))

    s = get_html("", stu.coes_cookie, intake, week)

    if s is None:
        return HttpResponse(json.dumps({"code": Codes.TIMETABLE_COOKIE_EXPIRED,
                                        "msg": Messages.TIMETABLE_COOKIE_EXPIRED}))
    try:
        r = get_timetable(s)

        for e in r:
            print(e)
            Course.objects.get(intake=intake, course_code=e['course_id'], course_class=e['course_class'])

        return HttpResponse(json.dumps(r))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"code": Codes.TIMETABLE_UNKNOWN_EXCEPTION,
                                        "msg": Messages.TIMETABLE_UNKNOWN_EXCEPTION}))
