import sys
import traceback
from datetime import datetime, time

import pytz
from django.core.exceptions import ObjectDoesNotExist

from services.basic.coes.gpa import get_gpa_list
from services.basic.models import ClassRoom
from services.course.models import Course, Schedule
from services.gpa.models import GPA
from django.http import JsonResponse
from services.student.models import Student, TakeCourse

# 获取缓存的课表
from services.teacher.models import Teacher, TeachCourse
from settings import messages, codes


def __timetable_cache(student: Student, intake: int, week: int):
    timetable = []
    # 看看都选了那些课
    takes = TakeCourse.objects.filter(student=student, intake=intake)
    for each_course in takes:
        # 每一个课程都有自己的安排（Schedule）
        #print(each_course.course.name_zh)
        schedules = Schedule.objects.filter(intake=intake, course=each_course.course)

        teachers = TeachCourse.objects.filter(intake=intake, course=each_course.course)
        teacher_str = ''
        for each_teacher in teachers:
            teacher_str = teacher_str + each_teacher.teacher.name_zh + "; "

        for each_schedule in schedules:
            #print(each_schedule.day_of_week, each_schedule.time_begin, each_schedule.time_end)
            timetable.append({
                # TODO: 其实 teacher 应该放到 schedule 里的
                "day": each_schedule.day_of_week,
                "time_begin": str(each_schedule.time_begin)[:-3],
                "time_end": str(each_schedule.time_end)[:-3],
                "course_code": each_schedule.course.course_code,
                "course_name_zh": each_schedule.course.name_zh,
                "course_class": each_schedule.course.course_class,
                "classroom": each_schedule.classroom.name_zh,
                "teacher": teacher_str[:-2], # -2 是为了删掉最后的 '; '
                "date_begin": str(each_schedule.date_begin)[5:],
                "date_end": str(each_schedule.date_end)[5:],
                "course_id": each_schedule.course.id
            })
    return timetable


# 更新课表缓存，及相关数据
def __timetable_update(student: Student, intake: int, week: int):
    from services.basic.coes.timetable import get_html, get_timetable
    # Get HTML source code
    source = get_html('', student.coes_cookie, intake, week)

    if source is None:
        tmtb = __timetable_cache(student, intake, week)
        if tmtb is None:
            tmtb = []
        return JsonResponse({
            'code': codes.TIMETABLE_COOKIE_EXPIRED,
            'msg': messages.TIMETABLE_COOKIE_EXPIRED,
            "timetable": tmtb
        })

    ret = ''

    try:
        ret = get_timetable(source)

        for each_ret in ret:
            # 创建课程
            course, created = Course.objects.update_or_create(
                course_code=each_ret['course_code'],
                course_class=each_ret['course_class'],
                defaults={
                    'name_zh': each_ret['course_name_zh']
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

            stu_take_course, created = TakeCourse.objects.get_or_create(intake=intake, student=student, course=course)
            if created:
                print('Create a new TakeCourse %s Take %s' % (str(student), str(course)))

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
