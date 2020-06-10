import sys
import traceback
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from services.authentication import utility
from services.authentication.decorators import validate
from services.basic.coes.timetable import get_html, get_timetable
from services.basic.models import ClassRoom
from services.course.models import Course, Schedule
from services.student.models import TakeCourse
from services.teacher.models import TeachCourse, Teacher
from services.timetable.controller import __timetable_cache
from settings import codes, messages

# Default timetable intake
TIMETABLE_INTAKE = 1902


@csrf_exempt
#@validate
def api_timetable(request):
    ret = []
    stu = utility.get_student_object(request)

    intake = int(request.GET.get('intake', TIMETABLE_INTAKE))
    week = int(request.GET.get('week', -1))
    if week == -1:
        return JsonResponse({
            'code': codes.TIMETABLE_WEEK_INVALID,
            'msg': messages.TIMETABLE_WEEK_INVALID
        })

    # Get HTML source code
    source = get_html('', stu.coes_cookie, intake, week)

    if source is None:

        tmtb = __timetable_cache(stu, intake, week)
        if tmtb is None:
            tmtb=[]

        return JsonResponse({
            'code': codes.TIMETABLE_COOKIE_EXPIRED,
            'msg': messages.TIMETABLE_COOKIE_EXPIRED,
            "timetable":tmtb
        })
    try:
        ret = get_timetable(source)

        for each_ret in ret:
            # 创建课程
            course, created = Course.objects.update_or_create(
                    course_code=each_ret['course_code'],
                    course_class=each_ret['course_class'],
                    defaults={
                        'name_zh' : each_ret['course_name_zh']
                    })

            if created:
                print('Create a new course [%s %s %s]'
                      % (course.course_code, course.course_class, course.name_zh))

            each_ret['course_id'] = course.id

            # 创建教室
            classroom, created = ClassRoom.objects.get_or_create(name_zh=each_ret['classroom'])
            if created:
                print('Create a new ClassRoom [%s]' % classroom.name_zh)

            date_begin = datetime.strptime(each_ret['date_begin'], '%m-%d')
            time_begin = datetime.strptime(each_ret['time_begin'], '%H:%M')
            date_end = datetime.strptime(each_ret['date_end'], '%m-%d')
            time_end = datetime.strptime(each_ret['time_end'], '%H:%M')

            # 创建日程

            schedule, created = Schedule.objects.get_or_create(
                intake=intake,
                date_begin=date_begin,
                date_end=date_end,
                time_begin=time_begin,
                time_end=time_end,
                day_of_week=each_ret['day'],
                course=course,
                classroom=classroom
            )
            if created:
                print('Create a new Schedule %d [DAY-%d %s-%s] for course [%s] at Classroom [%s]'
                      % (intake, int(schedule.day_of_week),
                         datetime.strftime(schedule.time_begin, '%H:%M'),
                         datetime.strftime(schedule.time_end, '%H:%M'),
                         schedule.course.course_code + '-' + schedule.course.name_zh,
                         schedule.classroom.name_zh))
            # 关联学生选课

            stu_take_course, created = TakeCourse.objects.get_or_create(intake=intake, student=stu, course=course)
            if created:
                print('Create a new TakeCourse %s Take %s' % (str(stu), str(course)))

            # 创建老师，关联老师教课
            teachers = each_ret['teacher'].split(',')
            for teacher in teachers:
                te, created = Teacher.objects.get_or_create(name_zh=teacher)
                if created:
                    print('Create a new teacher %s' % (str(te)))

                teacher_teach_course, created = TeachCourse.objects.get_or_create(
                    intake=intake,
                    teacher=te,
                    course=course
                )
                if created:
                    print('Create a new TeachCourse %s Teach %s' % (str(te), str(course)))

        return JsonResponse({
            'code': codes.OK,
            'msg': messages.OK,
            'timetable': ret
        })
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            'code': codes.TIMETABLE_UNKNOWN_EXCEPTION,
            'msg': messages.TIMETABLE_UNKNOWN_EXCEPTION,
            'timetable': ret
        })
