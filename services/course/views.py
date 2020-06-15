import sys
import traceback

from django.db.models import Avg
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from mustplus.decorators import require_get, require_post
from services.authentication.decorators import validate
from services.authentication.utility import get_student_object
from services.basic.coes.course_list import FACULTIES
from services.basic.coes.course_list import get_all_pages
from services.basic.coes.course_list import make_request
from services.basic.coes.course_list import process_course_list
from services.basic.query import get_faculty
from services.course.controller import *
from services.course.controller import _ftp_get, _comment_thumbs_up_cancel, _comment_thumbs_up, \
    _comment_thumbs_down_cancel, _comment_thumbs_down, _comment_get, _comment_publish, _comment_delete, _course_info
from services.course.models import Course
from services.course.models import Comment
from services.course.models import Schedule
from services.teacher.models import TeachCourse
from settings import codes, messages


#@validate
def init(request):
    try:
        stu = get_student_object(request)
        token = stu.coes_token
        cookie = stu.coes_cookie

        for faculty in FACULTIES:
            print("Now faculty: ", faculty)
            html = make_request(token, 1, faculty, cookie)
            pages = get_all_pages(html)

            for page in range(1, pages + 1):  # 这里为什么要多循环一次（从1开始不从2开始）呢，因为少循环一次会让代码变丑很多
                print("Page", page)
                html_source = make_request(token, page, faculty, cookie)
                course_list = process_course_list(html_source)
                for course in course_list:
                    try:
                        Course.objects.get(course["course_code"].strip(), 'EMPTY')
                    except ObjectDoesNotExist:
                        course = Course(
                            course["course_code"].strip(),
                            'EMPTY',
                            course['name_zh'].strip(),
                            course['name_en'].strip(),
                            course['credit'].strip(),
                            get_faculty(course['faculty'].strip()),
                        )
                        course.save()

    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
    return HttpResponse()


#@validate
def api_ftp(request, course_id):
    # TODO: FTP功能
    # 无论如何都要先判断一下 course_id 是否正确
    try:
        course = Course.objects.get(id=course_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": codes.COURSE_ID_NOT_FOUNT,
            "msg": messages.COURSE_ID_NOT_FOUNT
        })
    if request.method == "GET":
        student = get_student_object(request)
        return _ftp_get(course, student)
    if request.method == "POST":
        pass
    if request.method == "DELETE":
        pass


@csrf_exempt
#@validate
def api_comment(request, course_id):
    # 无论如何都要先判断一下 course_id 是否正确
    try:
        course = Course.objects.get(id=course_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": codes.COURSE_ID_NOT_FOUNT,
            "msg": messages.COURSE_ID_NOT_FOUNT
        })

    student = get_student_object(request)

    try:
        if request.method == "GET":  # get course comment
            return _comment_get(course)

        if request.method == "POST":  # publish course comment
            rank = float(request.POST.get("rank", 2.5))
            content = str(request.POST.get("content", ""))
            return _comment_publish(course, student, rank, content)

        if request.method == "DELETE":
            comment_id = request.GET.get('id')
            return _comment_delete(comment_id, student)

        return JsonResponse({
            "code": codes.AUTH_REQUEST_METHOD_ERROR,
            "msg": messages.AUTH_REQUEST_METHOD_ERROR
        })
    except Exception as exception:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            "code": codes.COURSE_COMMENT_UNKNOWN_ERROR,
            "msg": messages.COURSE_COMMENT_UNKNOWN_ERROR
        })


@require_post
#@validate
def api_thumbs_up(request):
    if request.method == "POST":
        comment_id = int(request.GET.get("id", -1))
        student = get_student_object(request)
        return _comment_thumbs_up(comment_id, student)

    if request.method == "DELETE":
        comment_id = int(request.GET.get("id", -1))
        student = get_student_object(request)
        return _comment_thumbs_up_cancel(comment_id, student)

    return JsonResponse({
        "code": codes.AUTH_REQUEST_METHOD_ERROR,
        "msg": messages.AUTH_REQUEST_METHOD_ERROR
    })


#@validate
def api_thumbs_down(request):
    if request.method == "POST":
        comment_id = int(request.GET.get("id", -1))
        student = get_student_object(request)
        return _comment_thumbs_down(comment_id, student)

    if request.method == "DELETE":
        comment_id = int(request.GET.get("id", -1))
        student = get_student_object(request)
        return _comment_thumbs_down_cancel(comment_id, student)

    return JsonResponse({
        "code": codes.AUTH_REQUEST_METHOD_ERROR,
        "msg": messages.AUTH_REQUEST_METHOD_ERROR
    })


@require_get
#@validate
def api_course(request, course_id):
    # 无论如何都要先判断一下 course_id 是否正确
    try:
        course = Course.objects.get(id=course_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": codes.COURSE_ID_NOT_FOUNT,
            "msg": messages.COURSE_ID_NOT_FOUNT
        })

    try:
        return _course_info(course)
    except Exception as exception:
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            "code": codes.COURSE_COMMENT_UNKNOWN_ERROR,
            "msg": messages.COURSE_COMMENT_UNKNOWN_ERROR
        })
