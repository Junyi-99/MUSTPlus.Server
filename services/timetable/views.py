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
from settings import codes, messages

# Default timetable intake
TIMETABLE_INTAKE = 1902


@csrf_exempt
@validate
def timetable(request):
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
        return JsonResponse({
            'code': codes.TIMETABLE_COOKIE_EXPIRED,
            'msg': messages.TIMETABLE_COOKIE_EXPIRED
        })
    try:
        ret = get_timetable(source)

        for each_ret in ret:
            # 创建课程
            try:
                course = Course.objects.get(
                    course_code=each_ret['course_code'],
                    course_class=each_ret['course_class']
                )
            except ObjectDoesNotExist:
                course = Course(
                    course_code=each_ret['course_code'],
                    course_class=each_ret['course_class'],
                    name_zh=each_ret['course_name_zh'],
                )
                course.save()
                print('Create a new course [%s %s %s]'
                      % (course.course_code, course.course_class, course.name_zh))
            each_ret['course_id'] = course.id

            # 创建教室
            try:
                classroom = ClassRoom.objects.get(name_zh=each_ret['classroom'])
            except ObjectDoesNotExist:
                classroom = ClassRoom(name_zh=each_ret['classroom'])
                classroom.save()
                print('Create a new ClassRoom [%s]' % classroom.name_zh)

            date_begin = datetime.strptime(each_ret['date_begin'], '%m-%d')
            time_begin = datetime.strptime(each_ret['time_begin'], '%H:%M')
            date_end = datetime.strptime(each_ret['date_end'], '%m-%d')
            time_end = datetime.strptime(each_ret['time_end'], '%H:%M')

            # 创建日程
            try:
                schedule = Schedule.objects.get(
                    intake=intake,
                    date_begin=date_begin,
                    date_end=date_end,
                    time_begin=time_begin,
                    time_end=time_end,
                    day_of_week=each_ret['day'],
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
                    day_of_week=each_ret['day'],
                    course=course,
                    classroom=classroom
                )
                schedule.save()
                print('Create a new Schedule %d [DAY-%d %s-%s] for course [%s] at Classroom [%s]'
                      % (
                          intake,
                          int(schedule.day_of_week),
                          datetime.strftime(schedule.time_begin, '%H:%M'),
                          datetime.strftime(schedule.time_end, '%H:%M'),
                          schedule.course.course_code + '-' + schedule.course.name_zh,
                          schedule.classroom.name_zh
                      ))
            # 关联学生选课
            try:
                stu_take_course = TakeCourse.objects.get(intake=intake, student=stu, course=course)
            except ObjectDoesNotExist:
                stu_take_course = TakeCourse(intake=intake, student=stu, course=course)
                stu_take_course.save()
                print('Create a new TakeCourse %s Take %s'
                      % (
                          str(stu), str(course)
                      ))

            # 创建老师，关联老师教课
            teachers = each_ret['teacher'].split(',')
            for teacher in teachers:
                try:
                    teacher = Teacher.objects.get(name_zh=teacher)
                except ObjectDoesNotExist:
                    teacher = Teacher(name_zh=teacher)
                    teacher.save()
                    print('Create a new teacher %s' % (str(teacher)))
                try:
                    teacher_teach_course = TeachCourse.objects.get(
                        intake=intake,
                        teacher=teacher,
                        course=course
                    )
                except ObjectDoesNotExist:
                    teacher_teach_course = TeachCourse(
                        intake=intake,
                        teacher=teacher,
                        course=course
                    )
                    teacher_teach_course.save()
                    print('Create a new TeachCourse %s Teach %s' % (str(teacher), str(course)))

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
