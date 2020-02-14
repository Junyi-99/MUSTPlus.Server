from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from mustplus.decorators import require_get
from services.authentication.decorators import validate
from services.moments.models import Moment, Comment, ThumbsUp
from settings import codes, messages


# 获取 Moment 列表
@require_get
@validate
def api_moment(request):
    try:
        try:
            begin = int(request.GET.get('from', 1))
        except ValueError:
            begin = 0

        moments = Moment.objects.filter(publish_time__lte=begin).order_by('-publish_time')[:10]

        moment_list = []
        for m in moments:
            forwarding = {}
            if m.forwarding is not None:
                forwarding = {
                    "id": m.forwarding.id,
                    "student": m.forwarding.student.get_name(),
                    "forwarding": None,
                    "content": m.forwarding.content,
                    "publish_time": m.forwarding.publish_time
                }
            else:
                forwarding = None
            moment_list.append({
                "student": m.student.get_name(),
                "forwarding": forwarding,
                "content": m.content,
                "thumbs_up": m.thumbs_up,
                "publish_time": m.publish_time,
                "pics": m.pics
            })

        return JsonResponse({
            'code': codes.OK,
            'msg': messages.OK,
            'moments': moments
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'code': codes.TEACHER_ID_NOT_FOUNT,
            'msg': messages.TEACHER_ID_NOT_FOUNT
        })


# 获取单条 Moment 详情
@require_get
@validate
def api_moment_id(request, moment_id):
    try:
        moment = Moment.objects.get(id=moment_id, visible=True)  # 只能看到 visible 为 True 的

        forwarding = {}
        if moment.forwarding is not None:
            forwarding = {
                "id": moment.forwarding.id,
                "student": moment.forwarding.student.get_name(),
                "forwarding": None,
                "content": moment.forwarding.content,
                "publish_time": moment.forwarding.publish_time
            }
        else:
            forwarding = None
        return JsonResponse({
            'code': codes.OK,
            'msg': messages.OK,
            'moment': {
                "student": moment.student.get_name(),
                "forwarding": forwarding,
                "content": moment.content,
                "thumbs_up": moment.thumbs_up,
                "publish_time": moment.publish_time,
                "pics": moment.pics
            }
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'code': codes.MOMENT_DOES_NOT_EXIST,
            'msg': messages.MOMENT_DOES_NOT_EXIST
        })
