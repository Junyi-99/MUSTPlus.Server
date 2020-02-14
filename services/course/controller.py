# controller.py 用来实现 views 中的功能
# views.py 像是 .h 文件
# 而 controller.py 则是 .c 文件

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from services.course.models import Course, Ftp, Comment, ThumbsUp, ThumbsDown, Schedule
from services.teacher.models import TeachCourse
from settings import codes, messages


def _swearing_filter(content: str) -> str:
    word_list = ['傻逼', '蠢逼', '狗日', '操逼', '屄', '做爱', '习近平', '共产党', '法轮功', '操你妈', '草泥马', '草你妈']
    for word in word_list:
        content = content.replace(word, '喵喵喵')
    return content


def _course_info(course: Course) -> JsonResponse:
    teacher_list = []
    teaches = TeachCourse.objects.filter(course=course).order_by('-intake')
    for teach in teaches:
        teacher_list.append({
            "name_zh": teach.teacher.name_zh,
            "name_en": teach.teacher.name_en,
            "position": teach.teacher.position,
            "email": teach.teacher.email,
            "office_room": teach.teacher.office_room,
            "avatar_url": teach.teacher.avatar_url
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
    rank_avg = Comment.objects.filter(course=course, visible=True).aggregate(Avg('rank'))
    if rank_avg['rank__avg'] is None:
        rank_avg['rank__avg'] = 2.5

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


def _ftp_post(course: Course, student, address, port, username, password) -> JsonResponse:
    ret_code = codes.OK
    ret_msg = ""
    obj = Ftp(course, student, address, port, username, password)
    obj.save()

    return JsonResponse({
        "code": ret_code,
        "msg": ret_msg
    })


def _ftp_get(course: Course, student) -> JsonResponse:
    try:
        ftp = Ftp.objects.filter(course=course, visible=True)
    except ObjectDoesNotExist:
        pass


def _comment_publish(course, student, rank, content) -> JsonResponse:
    ret_code = codes.OK
    ret_msg = ""

    if content.strip() == "":
        ret_code = codes.COURSE_COMMENT_CONTENT_EMPTY
        ret_msg = messages.COURSE_COMMENT_CONTENT_EMPTY

    if len(content) > 512:
        ret_code = codes.COURSE_COMMENT_CONTENT_TOO_LONG
        ret_msg = messages.COURSE_COMMENT_CONTENT_TOO_LONG

    if rank > 5 or rank < 0:
        ret_code = codes.COURSE_COMMENT_RANK_INVALID
        ret_msg = messages.COURSE_COMMENT_RANK_INVALID

    if ret_code != codes.OK:
        return JsonResponse({
            "code": ret_code,
            "msg": ret_msg
        })

    content = _swearing_filter(content)

    comment = Comment(course=course, student=student, rank=rank, content=content)
    comment.save()
    return JsonResponse({
        "code": ret_code,
        "msg": ret_msg
    })


def _comment_delete(comment_id, student) -> JsonResponse:
    try:
        course_comment = Comment.objects.get(id=comment_id, student=student)
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


def _comment_get(course: Course) -> JsonResponse:
    comments = Comment.objects.filter(
        course=course,
        visible=True
    ).order_by('-publish_time')
    comment_list = []
    for comment in comments:
        comment_list.append({
            "comment_id": comment.id,
            "nickname": comment.student.nickname,
            "name_zh": comment.student.name_zh,
            "student_id": comment.student.student_id,
            "thumbs_up": comment.thumbs_up,
            "thumbs_down": comment.thumbs_down,
            "rank": "%.2f" % (comment.rank,),
            "content": comment.content,
            "publish_time": comment.publish_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK,
        "comments": comment_list
    })


def _comment_thumbs_up(comment_id, student) -> JsonResponse:
    try:
        comment = Comment.objects.get(id=comment_id, visible=True)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
            "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
        })
    try:
        ThumbsUp.objects.get(student=student, comment=comment)
    except ObjectDoesNotExist:
        thumbs = ThumbsUp(student=student, comment=comment)
        comment.thumbs_up = comment.thumbs_up + 1
        comment.save()
        thumbs.save()

    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK
    })


def _comment_thumbs_up_cancel(comment_id, student) -> JsonResponse:
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
            "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
        })
    try:
        ThumbsUp.objects.get(student=student, comment=comment).delete()
        comment.thumbs_up = comment.thumbs_up - 1
        comment.save()
    except ObjectDoesNotExist:  # 就什么也不返回，默认就是成功取消
        pass

    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK
    })


def _comment_thumbs_down(comment_id, student) -> JsonResponse:
    try:
        comment = Comment.objects.get(id=comment_id, visible=True)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
            "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
        })
    try:
        ThumbsDown.objects.get(student=student, comment=comment)
    except ObjectDoesNotExist:
        thumbs = ThumbsDown(student=student, comment=comment)
        comment.thumbs_down = comment.thumbs_down + 1
        comment.save()
        thumbs.save()
    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK
    })


def _comment_thumbs_down_cancel(comment_id, student) -> JsonResponse:
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": codes.COURSE_COMMENT_ID_NOT_FOUND,
            "msg": messages.COURSE_COMMENT_ID_NOT_FOUND
        })
    try:
        ThumbsDown.objects.get(student=student, comment=comment).delete()
        comment.thumbs_down = comment.thumbs_down - 1
        comment.save()
    except ObjectDoesNotExist:  # 就什么也不返回，默认就是成功取消
        pass

    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK
    })
