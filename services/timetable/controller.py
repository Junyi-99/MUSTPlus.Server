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
def __timetable_cache(student: Student, intake: int, week: int):
    timetable = []
    # 看看都选了那些课
    takes = TakeCourse.objects.filter(student=student,intake=intake)
    for each_course in takes:
        # 每一个课程都有自己的安排（Schedule）
        print(each_course.course.name_zh)
        schedules = Schedule.objects.filter(intake=intake, course=each_course.course)
        for each_schedule in schedules:
            print(each_schedule.day_of_week, each_schedule.time_begin, each_schedule.time_end)
            timetable.append({
                # TODO: 其实 teacher 应该放到 schedule 里的
                "day": each_schedule.day_of_week,
                "time_begin": str(each_schedule.time_begin)[:-3],
                "time_end": str(each_schedule.time_end)[:-3],
                "course_code": each_schedule.course.course_code,
                "course_name_zh": each_schedule.course.name_zh,
                "course_class": each_schedule.course.course_class,
                "classroom": each_schedule.classroom.name_zh,
                "teacher": None,
                "date_begin": str(each_schedule.date_begin)[5:],
                "date_end": str(each_schedule.date_end)[5:],
                "course_id": each_schedule.course.id
            })
    return timetable