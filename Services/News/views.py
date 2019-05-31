import json
import time
import hashlib
from datetime import datetime
import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError

from Services.Basic.models import Student
from Services.News.models import Announcement, Document, Attachment
from Settings import Codes, Messages


# 选择 [begin, begin+count] 范围的数据
# begin ∈ [1, n]
# department 和 faculty 谁不为 None 表示选择谁
# 如果二者都为 None 说明选择的是全部
def news_argument(begin: int, count: int, department: int = None, faculty: int = None) -> dict:
    if department is not None:
        ann = Announcement.objects.filter(department_id=department).order_by('-publish_time')  # 按照发布时间从最近到最远排序
        doc = Document.objects.filter(department_id=department).order_by('-publish_time')  # 按照发布时间从最近到最远排序
    elif faculty is not None:
        ann = Announcement.objects.filter(faculty_id=faculty).order_by('-publish_time')  # 按照发布时间从最近到最远排序
        doc = Document.objects.filter(faculty_id=faculty).order_by('-publish_time')  # 按照发布时间从最近到最远排序
    else:
        ann = Announcement.objects.all().order_by('-publish_time')  # 按照发布时间从最近到最远排序
        doc = Document.objects.all().order_by('-publish_time')  # 按照发布时间从最近到最远排序

    # 按照时间对 Announcement 和 Document 排序
    i, j, i_length, j_length = 0, 0, len(ann), len(doc)
    result = []
    while i < i_length and j < j_length:  # 先一起排序
        if ann[i].publish_time > doc[j].publish_time:
            result.append(ann[i])
            i = i + 1
        else:
            result.append(doc[j])
            j = j + 1
    while i < i_length:  # 如果 Announcement 没排完，把剩下的 Announcement 附在后面
        result.append(ann[i])
        i = i + 1
    while j < j_length:  # 如果 Document 没排完，把剩下的 Document 附在后面
        result.append(doc[j])
        j = j + 1

    # 参数过滤，防止请求超出数据范围
    if begin <= 0:
        begin = 1
    elif begin > len(result):
        begin = len(result)
    if count < 0:
        count = 0
    elif count > 20:
        count = 20
    if begin + count > len(result):
        count = len(result) - begin

    news = []  # 存放结果
    for i in range(begin - 1, begin - 1 + count):
        r = result[i]
        if r.department is not None:
            fac_dep = r.department.name_zh
        elif r.faculty is not None:
            fac_dep = r.faculty.name_zh
        else:
            fac_dep = "Unknown"

        if isinstance(r, Announcement):
            attachments = []
            try:
                attach = Attachment.objects.filter(belongs_to=r)
                for a in attach:
                    attachments.append({'title': a.title, 'url': a.url})
            except Exception as e:
                print("Exception in all_news Announcement:", e)

            news.append({
                "fac_dep": fac_dep,
                "title": r.title,
                "date": r.publish_time.strftime('%Y-%m-%d'),
                "type": True,  # True: viewDownload
                "content": r.content,
                'attachments': attachments
            })
        if isinstance(r, Document):
            news.append({
                "fac_dep": fac_dep,
                "title": r.title,
                "date": r.publish_time.strftime('%Y-%m-%d'),
                "type": False,  # True: viewDownload
                "url": r.url,
            })

    ret = {
        "code": Codes.OK,
        "msg": Messages.OK,
        "records": i_length + j_length,
        "news": news,
    }
    return ret


def news_department(request, department_id):
    try:
        begin = int(request.GET['from'])
        count = int(request.GET['count'])
    except Exception as e:
        begin = 0
        count = 20
    ret = news_argument(begin, count, department_id, None)
    return HttpResponse(json.dumps(ret))


def news_faculty(request, faculty_id):
    try:
        begin = int(request.GET['from'])
        count = int(request.GET['count'])
    except Exception as e:
        begin = 0
        count = 20
    ret = news_argument(begin, count, None, faculty_id)
    return HttpResponse(json.dumps(ret))


def news_all(request):
    try:
        begin = int(request.GET['from'])
        count = int(request.GET['count'])
    except Exception as e:
        begin = 0
        count = 20
    ret = news_argument(begin, count, None, None)
    return HttpResponse(json.dumps(ret))


def news_banners(request):
    try:
        token_get = str(request.GET.get('token', None))
        time_get = int(request.GET.get('time', 0))
        sign_get = str(request.GET.get('sign', None))
        print(token_get, time_get, sign_get)
        # sort GET parameter list
        get_para = ""
        for e in sorted(request.GET):
            if e == 'sign':  # except `sign`
                continue
            get_para = get_para + e + "=" + request.GET[e] + "&"
        get_para = get_para[:-1]

        # sort POST parameter list
        post_para = ""
        for e in sorted(request.POST):
            post_para = post_para + e + "=" + request.POST[e] + "&"
        post_para = post_para[:-1]

        # calculate sign
        param_list = get_para + post_para
        sign_calc = hashlib.md5(param_list.encode('utf-8')).hexdigest()

        # check sign
        if sign_calc != sign_get:
            print("Not Equal!", sign_get, sign_calc)
            return HttpResponse(json.dumps(
                {"code": Codes.AUTH_SIGN_VERIFICATION_FAILED, "msg": Messages.AUTH_SIGN_VERIFICATION_FAILED}))
        else:
            print("Equal!")

        # check time
        # if abs(int(time.time()) - int(time_get)) > 5 * 60:
        #     print("Time error", int(time.time()), time_get)
        #     return HttpResponse(json.dumps({"code": Codes.AUTH_TIME_INVALID, "msg": Messages.AUTH_TIME_INVALID}))
        # else:
        #     print("Time OK!")

        # check token
        try:
            stu = Student.objects.get(token=token_get)
            print(timezone.now())

            if stu.token_expired_time < timezone.now():
                return HttpResponse(json.dumps({"code": Codes.AUTH_TOKEN_INVALID, "msg": Messages.AUTH_TOKEN_INVALID}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"code": Codes.AUTH_TOKEN_INVALID, "msg": Messages.AUTH_TOKEN_INVALID}))



    except ValueError:
        return HttpResponse(
            json.dumps({
                "code": Codes.AUTH_VALIDATE_ARGUMENT_ERROR,
                "msg": Messages.AUTH_VALIDATE_ARGUMENT_ERROR
            }))

    return HttpResponse(json.dumps({"code": Codes.OK, "msg": Messages.OK}))
