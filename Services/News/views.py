import json

from django.http import HttpResponse

from Services.Authentication.decorators import validate
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


@validate
def news_banners(request):
    return HttpResponse(json.dumps({"code": Codes.OK, "msg": Messages.OK, "detail": "Passed"}))
