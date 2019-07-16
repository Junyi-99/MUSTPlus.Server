import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse

from mustplus.decorators import require_get
from services.authentication.decorators import validate
from services.authentication.utility import get_student_object
from services.basic.coes.course_list import FACULTIES
from services.basic.coes.course_list import get_all_pages
from services.basic.coes.course_list import make_request
from services.basic.coes.course_list import process_course_list
from services.basic.models import Faculty
from services.basic.query import get_faculty
from services.course.models import Course
from services.course.models import CourseComment
from services.course.models import Schedule
from services.course.models import ThumbsDownCourseComment
from services.course.models import ThumbsUpCourseComment
from services.teacher.models import TeachCourse
from settings import codes, messages


def save_course(
        course_code: str,
        course_class: str,
        name_zh: str,
        name_en: str,
        credit: str,
        faculty: Faculty
) -> None:
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
                    save_course(
                        course["course_code"].strip(),
                        'EMPTY',
                        course['name_zh'].strip(),
                        course['name_en'].strip(),
                        course['credit'].strip(),
                        get_faculty(course['faculty'].strip())
                    )
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
    return HttpResponse()


@validate
def api_thumbs_down(request, course_id):
    if request.method == "POST":
        try:
            comment_id = int(request.GET.get("id", -1))
            comment = CourseComment.objects.get(id=comment_id, visible=True)
        except ObjectDoesNotExist:
            return JsonResponse({
                "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
                "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
            })
        try:
            student = get_student_object(request)
            tdcc = ThumbsDownCourseComment.objects.get(student=student, comment=comment)
        except ObjectDoesNotExist:
            tdcc = ThumbsDownCourseComment(student=student, comment=comment)
            comment.thumbs_down = comment.thumbs_down + 1
            comment.save()
            tdcc.save()

        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK
        })
    if request.method == "DELETE":
        try:
            comment_id = int(request.GET.get("id", -1))
            comment = CourseComment.objects.get(id=comment_id)
        except ObjectDoesNotExist:
            return JsonResponse({
                "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
                "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
            })
        try:
            stu = get_student_object(request)
            ThumbsDownCourseComment.objects.get(student=stu, comment=comment).delete()
            comment.thumbs_down = comment.thumbs_down - 1
            comment.save()
        except ObjectDoesNotExist:
            pass

        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK
        })
    return JsonResponse({
        "code": codes.AUTH_REQUEST_METHOD_ERROR,
        "msg": messages.AUTH_REQUEST_METHOD_ERROR
    })


@validate
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
    if request.method == "POST":
        pass
    if request.method == "GET":
        pass
    if request.method == "DELETE":
        pass
    pass


@validate
def api_thumbs_up(request, course_id):
    if request.method == "POST":
        try:
            comment_id = int(request.GET.get("id", -1))
            comment = CourseComment.objects.get(id=comment_id, visible=True)
        except ObjectDoesNotExist:
            return JsonResponse({
                "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
                "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
            })
        try:
            student = get_student_object(request)
            tdcc = ThumbsUpCourseComment.objects.get(student=student, comment=comment)
        except ObjectDoesNotExist:
            tdcc = ThumbsUpCourseComment(student=student, comment=comment)
            comment.thumbs_up = comment.thumbs_up + 1
            comment.save()
            tdcc.save()

        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK
        })
    if request.method == "DELETE":
        try:
            comment_id = int(request.GET.get("id", -1))
            comment = CourseComment.objects.get(id=comment_id)
        except ObjectDoesNotExist:
            return JsonResponse({
                "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
                "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
            })
        try:
            student = get_student_object(request)
            ThumbsUpCourseComment.objects.get(student=student, comment=comment).delete()
            comment.thumbs_up = comment.thumbs_up - 1
            comment.save()
        except ObjectDoesNotExist:
            pass

        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK
        })
    return JsonResponse({
        "code": codes.AUTH_REQUEST_METHOD_ERROR,
        "msg": messages.AUTH_REQUEST_METHOD_ERROR
    })


@require_get
@validate
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
                "date_begin": schedule.date_begin.strftime("%m-%d"),
                "date_end": schedule.date_end.strftime("%m-%d"),
                "time_begin": schedule.time_begin.strftime("%H:%M"),
                "time_end": schedule.time_end.strftime("%H:%M"),
                "day_of_week": schedule.day_of_week,
                "classroom": schedule.classroom.name_zh,
            })

        # 只取可见评论中的打分情况
        rank_avg = CourseComment.objects.filter(course=course, visible=True).aggregate(Avg('rank'))

        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK,
            "course_code": course.course_code,
            "course_class": course.course_class,
            "name_zh": course.name_zh,
            "name_en": course.name_en,
            "name_short": course.name_short,
            "credit": course.credit,
            "faculty": None if course.faculty is None else course.faculty.name_zh,
            # foreign key 允许 null 时候一定要这样写一个三目运算符！
            "teachers": teacher_list,
            "schedule": schedule_list,
            "rank": rank_avg['rank__avg']
        })
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            "code": codes.COURSE_UNKNOWN_ERROR,
            "msg": messages.COURSE_UNKNOWN_ERROR
        })


def swearing_filter(content: str) -> str:
    word_list = ['傻逼', '蠢逼', '狗日', '操逼', '屄', '做爱', '习近平', '共产党', '法轮功']
    for word in word_list:
        content = content.replace(word, '大笨蛋')
    return content


def publish_comment(course, student, rank, content):
    ret_code = codes.OK
    ret_msg = ""

    if content.strip() == "":
        ret_code = codes.COURSE_COMMENT_CONTENT_EMPTY
        ret_msg = messages.COURSE_COMMENT_CONTENT_EMPTY

    if len(content) > 16384:
        ret_code = codes.COURSE_COMMENT_CONTENT_TOO_LONG
        ret_msg = messages.COURSE_COMMENT_CONTENT_TOO_LONG

    if rank > 5 or rank <= 0:
        ret_code = codes.COURSE_COMMENT_RANK_INVALID
        ret_msg = messages.COURSE_COMMENT_RANK_INVALID

    if ret_code != codes.OK:
        return JsonResponse({
            "code": ret_code,
            "msg": ret_msg
        })

    content = swearing_filter(content)

    comment = CourseComment(course=course, student=student, rank=rank, content=content)
    comment.save()
    return JsonResponse({
        "code": ret_code,
        "msg": ret_msg
    })


def delete_comment(comment_id, student):
    try:

        course_comment = CourseComment.objects.get(id=comment_id)
        # TODO: filter also filt student otherwise anyone can delete comment
        print(student.name_zh)
        course_comment.visible = False
        course_comment.save()
        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
            "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
        })


@validate
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

            comments = CourseComment.objects.filter(
                course=course,
                visible=True
            ).order_by('-publish_time')
            comment_list = []
            for comment in comments:
                comment_list.append({
                    "comment_id": comment.id,
                    "student_id": comment.student.student_id,
                    "thumbs_up": comment.thumbs_up,
                    "thumbs_down": comment.thumbs_down,
                    "rank": comment.rank,
                    "content": comment.content,
                    "publish_time": comment.publish_time.strftime("%Y-%m-%d %H:%M:%S")
                })
            return JsonResponse({
                "code": codes.OK,
                "msg": messages.OK,
                "comment": comment_list
            })
        if request.method == "POST":  # publish course comment
            rank = int(request.POST.get("rank", 3))
            content = str(request.POST.get("content", ""))
            return publish_comment(course, student, rank, content)
        if request.method == "DELETE":
            comment_id = request.GET.get('id')
            return delete_comment(comment_id, student)
        return JsonResponse({
            "code": codes.AUTH_REQUEST_METHOD_ERROR,
            "msg": messages.AUTH_REQUEST_METHOD_ERROR
        })
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            "code": codes.COURSE_COMMENT_UNKNOWN_ERROR,
            "msg": messages.COURSE_COMMENT_UNKNOWN_ERROR
        })
