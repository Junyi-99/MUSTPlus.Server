import json
from django.http import HttpResponse

from Services.Authentication import utility
from Services.Authentication.decorators import validate
from Services.Basic.COES.Timetable import get_html, get_timetable


@validate
def timetable(request):
    stu = utility.get_student_object(request)
    intake = int(request.GET.get("intake", 1902))
    week = int(request.GET.get('week', 0))
    s = get_html("", stu.coes_cookie, intake, week)

    r = get_timetable(s)
    return HttpResponse(json.dumps(r))
