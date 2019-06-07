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
from Services.Student.models import TakeCourse
from Services.Teacher.models import TeachCourse, Teacher
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

    # Get HTML source code
    s = get_html("", stu.coes_cookie, intake, week)
    if s is None:
        return HttpResponse(json.dumps({"code": Codes.TIMETABLE_COOKIE_EXPIRED,
                                        "msg": Messages.TIMETABLE_COOKIE_EXPIRED}))
    try:
        r = get_timetable(s)

        for e in r:
            # 创建课程
            try:
                course = Course.objects.get(course_code=e['course_id'], course_class=e['course_class'])
            except ObjectDoesNotExist:
                course = Course(
                    course_code=e['course_id'],
                    course_class=e['course_class'],
                    name_zh=e['course_name_zh'],
                )
                course.save()
                print("Create a new Course [%s %s %s]"
                      % (course.course_code, course.course_class, course.name_zh))
            # 创建教室
            try:
                classroom = ClassRoom.objects.get(name_zh=e['classroom'])
            except ObjectDoesNotExist:
                classroom = ClassRoom(name_zh=e['classroom'])
                classroom.save()
                print("Create a new ClassRoom [%s]" % classroom.name_zh)

            date_begin = datetime.strptime(e['date_begin'], '%m-%d')
            time_begin = datetime.strptime(e['time_begin'], '%H:%M')
            date_end = datetime.strptime(e['date_end'], '%m-%d')
            time_end = datetime.strptime(e['time_end'], '%H:%M')

            # 创建日程
            try:
                schedule = Schedule.objects.get(
                    intake=intake,
                    date_begin=date_begin,
                    date_end=date_end,
                    time_begin=time_begin,
                    time_end=time_end,
                    day_of_week=e['day'],
                    course=course,
                    classroom=classroom
                )
            except ObjectDoesNotExist:
                schedule = Schedule(
                    intake=intake,
                    date_begin=date_begin,
                    date_end=date_end,
                    time_begin=time_begin,
                    time_end=time_end,
                    day_of_week=e['day'],
                    course=course,
                    classroom=classroom
                )
                schedule.save()
                print("Create a new Schedule %d [DAY-%d %s-%s] for Course [%s] at Classroom [%s]"
                      % (
                          intake,
                          int(schedule.day_of_week),
                          datetime.strftime(schedule.time_begin, "%H:%M"),
                          datetime.strftime(schedule.time_end, "%H:%M"),
                          schedule.course.course_code + "-" + schedule.course.name_zh,
                          schedule.classroom.name_zh
                      ))
            # 关联学生选课
            try:
                stu_take_course = TakeCourse.objects.get(intake=intake, student=stu, course=course)
            except ObjectDoesNotExist:
                stu_take_course = TakeCourse(intake=intake, student=stu, course=course)
                stu_take_course.save()
                print("Create a new TakeCourse %s Take %s"
                      % (
                          str(stu), str(course)
                      ))

            # 创建老师，关联老师教课
            teachers = e['teacher'].split(',')
            for t in teachers:
                try:
                    teacher = Teacher.objects.get(name_zh=t)
                except ObjectDoesNotExist:
                    teacher = Teacher(name_zh=t)
                    teacher.save()
                    print("Create a new Teacher %s" % (str(teacher)))
                try:
                    teacher_teach_course = TeachCourse.objects.get(intake=intake, teacher=teacher, course=course)
                except ObjectDoesNotExist:
                    teacher_teach_course = TeachCourse(intake=intake, teacher=teacher, course=course)
                    teacher_teach_course.save()
                    print("Create a new TeachCourse %s Teach %s" % (str(teacher), str(course)))

        return HttpResponse(json.dumps(r))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps(
            {
                "code": Codes.TIMETABLE_UNKNOWN_EXCEPTION,
                "msg": Messages.TIMETABLE_UNKNOWN_EXCEPTION
            }
        ))
