import json
import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from Services.Authentication.decorators import validate
from Services.Basic.models import Department, Faculty
from Services.News.models import Announcement, Document, Attachment
from Settings import Codes, Messages


# 选择 [begin, begin+count] 范围的数据
# begin ∈ [1, n]
# department 和 faculty 谁不为 None 表示选择谁
# 如果二者都为 None 说明选择的是全部
def news_argument(begin: int, count: int, department: str = None, faculty: str = None) -> dict:
    if department is not None:
        try:
            dep = Department.objects.get(name_zh=department)
            ann = Announcement.objects.filter(department=dep).order_by('-publish_time')  # 按照发布时间从最近到最远排序
            doc = Document.objects.filter(department=dep).order_by('-publish_time')  # 按照发布时间从最近到最远排序
        except ObjectDoesNotExist:
            pass
    elif faculty is not None:
        try:
            fac = Faculty.objects.get(name_zh=faculty)
            ann = Announcement.objects.filter(faculty=fac).order_by('-publish_time')  # 按照发布时间从最近到最远排序
            doc = Document.objects.filter(faculty=fac).order_by('-publish_time')  # 按照发布时间从最近到最远排序
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
    print(begin, count)
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


user_response = openapi.Response('descr124iption', )


@swagger_auto_schema(method='get', responses={123: user_response}, tags=['News'])
@api_view(['GET'])
@validate
def news_department(request, department_name_zh):
    try:
        begin = int(request.GET['from'])
        count = int(request.GET['count'])
    except Exception as e:
        begin = 1
        count = 20
    try:
        ret = news_argument(begin, count, department_name_zh, None)
        return HttpResponse(json.dumps(ret))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({
            "code": Codes.NEWS_UNKNOWN_ERROR,
            "msg": Messages.NEWS_UNKNOWN_ERROR
        }))


@api_view(['GET'])
@validate
def news_faculty(request, faculty_name_zh):
    try:
        begin = int(request.GET['from'])
        count = int(request.GET['count'])
    except Exception as e:
        begin = 1
        count = 20
    try:
        ret = news_argument(begin, count, None, faculty_name_zh)
        return HttpResponse(json.dumps(ret))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({
            "code": Codes.NEWS_UNKNOWN_ERROR,
            "msg": Messages.NEWS_UNKNOWN_ERROR
        }))


@api_view(['GET'])
@validate
def news_all(request):
    try:
        begin = int(request.GET['from'])
        count = int(request.GET['count'])
    except Exception as e:
        begin = 1
        count = 20
    try:
        ret = news_argument(begin, count, None, None)
        return HttpResponse(json.dumps(ret))
    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
        return HttpResponse(json.dumps({
            "code": Codes.NEWS_UNKNOWN_ERROR,
            "msg": Messages.NEWS_UNKNOWN_ERROR
        }))


@validate
def news_banners(request):
    print(type(request))
    return HttpResponse(json.dumps({"code": Codes.OK, "msg": Messages.OK, "detail": "Passed"}))
