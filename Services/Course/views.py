import json
import sys
import time
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from MUSTPlus.decorators import require_get
from Services.Authentication.decorators import validate
from Services.Authentication.utility import get_student_object
from Services.Basic.COES.CourseList import faculties, make_request, process_course_list, get_all_pages
from Services.Basic.models import Faculty
from Services.Basic.query import get_faculty
from Services.Course.models import Course, CourseComment, Schedule
from Services.Teacher.models import TeachCourse
from Settings import Codes, Messages


def save_course(course_code: str, course_class: str, name_zh: str, name_en: str, credit: str, faculty: Faculty):
    try:
        Course.objects.get(course_code, course_class)
    except ObjectDoesNotExist:
        course = Course(
            course_code,
            course_class,
            name_zh,
            name_en,
            credit,
            faculty,
        )
        course.save()


@validate
def init(request):
    try:
        student = get_student_object(request)
        token = student.coes_token
        cookie = student.coes_cookie

        for faculty in faculties:
            print("Now faculty: ", faculty)
            html = make_request(token, 1, faculty, cookie)
            pages = get_all_pages(html)

            for page in range(1, pages + 1):  # 这里为什么要多循环一次（从1开始不从2开始）呢，因为少循环一次会让代码变丑很多
                print("Page", page)
                html_source = make_request(token, page, faculty, cookie)
                course_list = process_course_list(html_source)
                for course in course_list:
                    save_course(
                        course["course_code"].strip(),
                        'EMPTY',
                        course['name_zh'].strip(),
                        course['name_en'].strip(),
                        course['credit'].strip(),
                        get_faculty(course['faculty'].strip())
                    )


    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
    return HttpResponse()


@require_get
@validate
def api_course(request, course_id):
    # 无论如何都要先判断一下 course_id 是否正确
    try:
        course = Course.objects.get(course_id=course_id)
        pass
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"code": Codes.COURSE_ID_NOT_FOUNT, "msg": Messages.COURSE_ID_NOT_FOUNT}))
    try:
        teacher_list = []
        teaches = TeachCourse.objects.filter(course=course).order_by('-intake')
        for teach in teaches:
            teacher_list.append({
                "name_zh": teach.teacher.name_zh,
                "name_en": teach.teacher.name_en,
                "position": teach.teacher.position,
                "email": teach.teacher.email,
                "office_room": teach.teacher.office_room,
                "avatar": teach.teacher.avatar_url
            })

        schedule_list = []
        schedules = Schedule.objects.filter(course=course)
        for schedule in schedules:
            schedule_list.append({
                "intake": schedule.intake,
                "date_begin": time.strftime("%m-%d", schedule.date_begin),
                "date_end": time.strftime("%m-%d", schedule.date_end),
                "time_begin": time.strftime("%H:%M", schedule.time_begin),
                "time_end": time.strftime("%H:%M", schedule.time_end),
                "day_of_week": schedule.day_of_week,
                "classroom": schedule.classroom.name_zh,
            })

        print("AVG", CourseComment.objects.aggregate('rank'))
        return HttpResponse(json.dumps({
            "code": Codes.OK,
            "msg": Messages.OK,
            "course_code": course.course_code,
            "course_class": course.course_class,
            "name_zh": course.name_zh,
            "name_en": course.name_en,
            "name_short": course.name_short,
            "credit": course.credit,
            "faculty": course.faculty.name_zh,
            "teachers": teacher_list,
            "schedule": schedule_list,
            "rank": "to be implemented"
        }))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({
            "code": Codes.COURSE_UNKNOWN_ERROR,
            "msg": Messages.COURSE_UNKNOWN_ERROR
        }))


@validate
def api_comment(request, course_id):
    # 无论如何都要先判断一下 course_id 是否正确
    try:
        course = Course.objects.get(course_id=course_id)
        pass
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({"code": Codes.COURSE_ID_NOT_FOUNT, "msg": Messages.COURSE_ID_NOT_FOUNT}))

    try:
        if request.method == "GET":  # get course comment

            comments = CourseComment.objects.filter(course=course).order_by('-publish_time')
            com_list = []
            for comment in comments:
                com_list.append({
                    "comment_id": comment.id,
                    "student_id": comment.student.student_id,
                    "thumbs_up": comment.thumbs_up,
                    "thumbs_down": comment.thumbs_down,
                    "rank": comment.rank,
                    "content": comment.content,
                    "publish_time": time.strftime("%Y-%m-%d", comment.publish_time)
                })
            return HttpResponse(json.dumps({
                "code": Codes.OK,
                "msg": Messages.OK,
                "comment": com_list
            }))
        elif request.method == "POST":  # publish course comment
            rank = int(request.POST.get("rank", 3))
            content = str(request.POST.get("content", ""))
            student = get_student_object(request)
            comment = CourseComment(course=course, student=student, rank=rank, content=content)
            comment.save()
            return HttpResponse(json.dumps({
                "code": Codes.OK,
                "msg": Messages.OK
            }))
        elif request.method == "DELETE":
            try:
                comment_id = request.DELETE.get('id')
                course_comment = CourseComment.objects.get(id=comment_id)
                course_comment.visible = False
                course_comment.save()
                return HttpResponse(json.dumps({
                    "code": Codes.OK,
                    "msg": Messages.OK
                }))
            except ObjectDoesNotExist:
                return HttpResponse(json.dumps({
                    "code": Codes.COURSE_COMMENT_ID_NOT_FOUND,
                    "msg": Messages.COURSE_COMMENT_ID_NOT_FOUND
                }))
        else:
            return HttpResponse(json.dumps({
                "code": Codes.AUTH_REQUEST_METHOD_ERROR,
                "msg": Messages.AUTH_REQUEST_METHOD_ERROR
            }))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({
            "code": Codes.COURSE_COMMENT_UNKNOWN_ERROR,
            "msg": Messages.COURSE_COMMENT_UNKNOWN_ERROR
        }))
