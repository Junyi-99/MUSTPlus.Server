import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from services.authentication.decorators import validate
from services.basic.models import Department, Faculty
from services.news.models import Announcement, Document, Attachment
from settings import codes, messages


# 选择 [begin, begin+count] 范围的数据
# begin ∈ [1, n]
# department 和 faculty 谁不为 None 表示选择谁
# 如果二者都为 None 说明选择的是全部
def news_argument(begin: int, count: int, department: str = None, faculty: str = None) -> dict:
    ann = []
    doc = []
    if department is not None:
        try:
            dep = Department.objects.get(name_zh=department)
            # 按照发布时间从最近到最远排序
            ann = Announcement.objects.filter(department=dep).order_by('-publish_time')
            # 按照发布时间从最近到最远排序
            doc = Document.objects.filter(department=dep).order_by('-publish_time')
        except ObjectDoesNotExist:
            pass
    elif faculty is not None:
        try:
            fac = Faculty.objects.get(name_zh=faculty)
            # 按照发布时间从最近到最远排序
            ann = Announcement.objects.filter(faculty=fac).order_by('-publish_time')
            # 按照发布时间从最近到最远排序
            doc = Document.objects.filter(faculty=fac).order_by('-publish_time')
        except ObjectDoesNotExist:
            pass
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
        count = len(result) - begin + 1

    news_list = []  # 存放结果
    for i in range(begin - 1, begin - 1 + count):
        ret = result[i]

        if ret.department is not None:
            fac_dep = ret.department.name_zh
        elif ret.faculty is not None:
            fac_dep = ret.faculty.name_zh
        else:
            fac_dep = "Unknown"

        if isinstance(ret, Announcement):
            attachment_list = []
            attachments = Attachment.objects.filter(belongs_to=ret)
            for attachment in attachments:
                attachment_list.append({'title': attachment.title, 'url': attachment.url})

            news_list.append({
                "fac_dep": fac_dep,
                "title": ret.title,
                "date": ret.publish_time.strftime('%Y-%m-%d'),
                "type": True,  # True: viewDownload
                "content": ret.content,
                'attachment_list': attachment_list
            })
        if isinstance(ret, Document):
            news_list.append({
                "fac_dep": fac_dep,
                "title": ret.title,
                "date": ret.publish_time.strftime('%Y-%m-%d'),
                "type": False,  # True: viewDownload
                "url": ret.url,
            })

    return {
        "code": codes.OK,
        "msg": messages.OK,
        "records": i_length + j_length,
        "news_list": news_list,
    }


@validate
def news_department(request, department_name_zh):
    try:
        begin = int(request.GET['from'])
        count = int(request.GET['count'])
    except ValueError:
        begin = 1
        count = 20
    try:
        ret = news_argument(begin, count, department_name_zh, None)
        return JsonResponse(ret)
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            "code": codes.NEWS_UNKNOWN_ERROR,
            "msg": messages.NEWS_UNKNOWN_ERROR
        })


@validate
def news_faculty(request, faculty_name_zh):
    try:
        begin = int(request.GET.get('from', 1))
        count = int(request.GET.get('count', 20))
    except ValueError:
        begin = 1
        count = 20
    try:
        ret = news_argument(begin, count, None, faculty_name_zh)
        return JsonResponse(ret)
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            "code": codes.NEWS_UNKNOWN_ERROR,
            "msg": messages.NEWS_UNKNOWN_ERROR
        })


@validate
def news_all(request):
    try:
        begin = int(request.GET.get('from', 1))
        count = int(request.GET.get('count', 20))
    except ValueError:
        begin = 1
        count = 20
    try:
        ret = news_argument(begin, count, None, None)
        print(ret)
        return JsonResponse(ret)
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            "code": codes.NEWS_UNKNOWN_ERROR,
            "msg": messages.NEWS_UNKNOWN_ERROR
        })


@validate
def news_banners(request):
    print(type(request))
    return JsonResponse({
        "code": codes.OK,
        "msg": messages.OK,
        "detail": "Passed"
    })
