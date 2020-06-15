import sys
import traceback
from datetime import datetime, timedelta

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from services.lost.models import LostRecord
from settings import codes, messages

LOST_STATUS_FINDING = 'finding'
LOST_STATUS_FOUND = 'found'


def __lost_get(f, c):

    lost = []

    current_time = int(datetime.now(tz=pytz.UTC).timestamp())
    if f > current_time:
        f = current_time

    if c < 0 or c > 20:
        c = 20
    # 转换成 timezone aware 的
    fdt = datetime(1970, 1, 1, tzinfo=pytz.UTC) + timedelta(seconds=f)
    #print(type(fdt),fdt)
    #print(type(datetime.now(tz=pytz.UTC)),datetime.now(tz=pytz.UTC))
    #print(fdt > datetime.now(tz=pytz.UTC))
    records = LostRecord.objects.filter(visible=True, publish_time__lt=fdt).order_by('-publish_time')[:c]

    for r in records:
        lost.append({
            'id':r.id,
            'student_nickname': r.student.nickname,
            'student_name_zh':r.student.name_zh,
            'student_avatar_url':r.student.avatar_url,
            'publish_time': datetime.strftime(r.publish_time, '%Y-%m-%d %H:%M UTC+0'),
            #'f_time': datetime.strftime(datetime.utcfromtimestamp(f), '%Y-%m-%d %H:%M UTC+0'),
            #'current_time': datetime.strftime(datetime.utcfromtimestamp(current_time), '%Y-%m-%d %H:%M UTC+0'),
            'content': r.content,
            'status': r.status
        })
    return JsonResponse({
        'code': codes.OK,
        'msg': messages.OK,
        'lost': lost
    })


def __lost_publish(student, description):
    try:

        if student is None:
            return JsonResponse({
                'code': codes.AUTH_TOKEN_INVALID,
                'msg':codes.AUTH_TOKEN_INVALID
            })

        record = LostRecord(student=student, content=description, status=LOST_STATUS_FINDING,
                            publish_time=datetime.now(tz=pytz.UTC), visible=True)
        record.save()
        return JsonResponse({
            'code': codes.OK,
            'msg': '挂失消息发布成功'
        })
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({
            'code': codes.INVALID_PARAM,
            'msg': '挂失消息发布失败'
        })


def __lost_update_status(student, lost_id, target_status):
    try:
        record = LostRecord.objects.get(id=lost_id)
        if record.student.student_id != student.student_id:
            return JsonResponse({
                'code': codes.LOST_AND_FOUND_PERMISSION_DENIED,
                'msg': messages.LOST_AND_FOUND_PERMISSION_DENIED
            })
        else:
            record.status = target_status
            record.save()
            return JsonResponse({
                'code': codes.OK,
                'msg': '状态已变更为'+target_status
            })
    except ObjectDoesNotExist:
        return JsonResponse(
            {'code': codes.LOST_AND_FOUND_NO_SUCH_RECORD, 'msg': messages.LOST_AND_FOUND_NO_SUCH_RECORD})


def __lost_delete(student, lost_id):
    try:
        record = LostRecord.objects.get(id=lost_id, visible=True)
        if record.student.student_id != student.student_id:
            return JsonResponse({
                'code': codes.LOST_AND_FOUND_PERMISSION_DENIED,
                'msg': messages.LOST_AND_FOUND_PERMISSION_DENIED
            })
        else:
            record.visible = False
            record.save()
            return JsonResponse({
                'code': codes.OK,
                'msg': '编号'+str(lost_id)+'的记录已被删除'
            })
    except ObjectDoesNotExist:
        return JsonResponse(
            {'code': codes.LOST_AND_FOUND_NO_SUCH_RECORD, 'msg': '没有编号为'+str(lost_id)+'的挂失记录'})

# 最多只返回最近的20条数据
# 防止一次返回太多卡死前端

def __lost_search(keywords : str):

    try:
        lost = []
        losts = LostRecord.objects.filter(content__contains=keywords).order_by('-publish_time')[:20]
        for r in losts:
            lost.append({
                'id': r.id,
                'student_nickname': r.student.nickname,
                'student_name_zh': r.student.name_zh,
                'student_avatar_url': r.student.avatar_url,
                'publish_time': datetime.strftime(r.publish_time, '%Y-%m-%d %H:%M UTC+0'),
                # 'f_time': datetime.strftime(datetime.utcfromtimestamp(f), '%Y-%m-%d %H:%M UTC+0'),
                # 'current_time': datetime.strftime(datetime.utcfromtimestamp(current_time), '%Y-%m-%d %H:%M UTC+0'),
                'content': r.content,
                'status': r.status
            })
        return JsonResponse({
            'code': codes.OK,
            'msg': messages.OK,
            'lost': lost
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'code': codes.OK,
            'msg': messages.OK,
            'lost': []
        })
    except Exception as exception:
        return JsonResponse({
            'code': codes.OK,
            'msg': messages.OK,
            'lost': []
        })
