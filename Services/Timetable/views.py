import json
import sys
import traceback
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Services.Authentication import utility
from Services.Authentication.decorators import validate
from Services.Basic.COES.Timetable import get_html, get_timetable
from Services.Basic.models import ClassRoom
from Services.Course.models import Course, Schedule
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
            try:
                course = Course.objects.get(intake=intake, course_code=e['course_id'], course_class=e['course_class'])
            except ObjectDoesNotExist:
                a = """"{
                    'day': sp2[0].strip(),
                    'time_begin': sp2[1],
                    'time_end': sp2[2],
                    'classroom': sp2[6],
                    'teacher': sp2[7],
                    
                }"""
                course = Course(
                    intake=intake,
                    course_code=e['course_id'],
                    course_class=e['course_class'],
                    name_zh=e['course_name_zh'],
                )
                course.save()
                print("Create a new Course [%d %s %s %s]"
                      % (course.intake, course.course_code, course.course_class, course.name_zh))
            try:
                classroom = ClassRoom.objects.get(name_zh=e['classroom'])
            except ObjectDoesNotExist:
                classroom = ClassRoom(name_zh=e['classroom'])
                classroom.save()
                print("Create a new ClassRoom [%s]" % classroom.name_zh)

            date_start = datetime.strptime(e['date_begin'], '%m-%d')
            time_start = datetime.strptime(e['time_begin'], '%H:%M')
            date_end = datetime.strptime(e['date_end'], '%m-%d')
            time_end = datetime.strptime(e['time_end'], '%H:%M')

            try:
                schedule = Schedule.objects.get(date_start=date_start, date_end=date_end,
                                                time_start=time_start, time_end=time_end,
                                                day_of_week=e['day'], course=course, classroom=classroom)
            except ObjectDoesNotExist:
                schedule = Schedule(date_start=date_start, date_end=date_end,
                                    time_start=time_start, time_end=time_end,
                                    day_of_week=e['day'], course=course, classroom=classroom)
                schedule.save()
                print("Create a new Schedule [DAY-%d %s-%s] of Course [%s] at Classroom [%s]" % (
                    int(schedule.day_of_week), datetime.strftime(schedule.time_start, "%H:%M"),
                    datetime.strftime(schedule.time_end, "%H:%M"),
                    schedule.course.course_code + "-" + schedule.course.name_zh,
                    schedule.classroom.name_zh))

        return HttpResponse(json.dumps(r))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({"code": Codes.TIMETABLE_UNKNOWN_EXCEPTION,
                                        "msg": Messages.TIMETABLE_UNKNOWN_EXCEPTION}))
