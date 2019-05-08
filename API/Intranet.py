import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from MUSTPlus.models import Document
from MUSTPlus.models import Announcement
from MUSTPlus.models import Attachment
from Settings import Codes
from Settings import Messages

@csrf_exempt
def news_all(request):
    try:
        begin = int(request.GET['from'])
        count = int(request.GET['count'])
    except Exception as e:
        begin = 0
        count = 20

    announcements = Announcement.objects.all().order_by('-publish_time')  # 按照发布时间从最近到最远排序
    documents = Document.objects.all().order_by('-publish_time')  # 按照发布时间从最近到最远排序

    # 按照时间对 Announcement 和 Document 排序
    i, j, i_length, j_length = 0, 0, len(announcements), len(documents)
    result = []
    while i < i_length and j < j_length:  # 先一起排序
        if announcements[i].publish_time > documents[j].publish_time:
            result.append(announcements[i])
            i = i + 1
        else:
            result.append(documents[j])
            j = j + 1
    while i < i_length:  # 如果 Announcement 没排完，把剩下的 Announcement 附在后面
        result.append(announcements[i])
        i = i + 1
    while j < j_length:  # 如果 Document 没排完，把剩下的 Document 附在后面
        result.append(documents[i])
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
        if r.department_id is not None:
            fac_dep = r.department_id.name_zh
        elif r.faculty_id is not None:
            fac_dep = r.faculty_id.name_zh
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
        "msg": Messages.OK_MSG,
        "records": i_length + j_length,
        "news": news,
    }
    return HttpResponse(json.dumps(ret))
