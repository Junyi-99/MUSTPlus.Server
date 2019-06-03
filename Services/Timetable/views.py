import json
from django.http import HttpResponse

from Services.Authentication import utility
from Services.Authentication.decorators import validate
from Services.Basic.COES.Timetable import get_html, get_timetable
from Services.Course.models import Course


@validate
def timetable(request):
    stu = utility.get_student_object(request)
    intake = int(request.GET.get("intake", 1902))
    week = int(request.GET.get('week', 0))
    s = get_html("", stu.coes_cookie, intake, week)

    r = get_timetable(s)

    for e in r:
        print(e)
        Course.objects.get(course_code=e['course_id'], course_class=e['course_class'])

    return HttpResponse(json.dumps(r))
