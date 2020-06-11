import sys
import traceback
from datetime import datetime

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from services.authentication import utility
from services.authentication.decorators import validate
from services.lost.controller import __lost_update_status, __lost_delete, __lost_publish, __lost_get
from services.lost.models import LostRecord
from settings import codes, messages


@csrf_exempt
# @validate
def api_lost(request):
    if request.method == "GET":
        # 获取一部分挂失数据（要支持分页功能）
        # 需要的参数：
        #          from:  10位UTC时间戳，什么时间之前的挂失数据
        #          count: 你想要获取多少条 from 之前的挂失数据，最大20，最小0
        # 要么这俩参数都不写，要么就都写，不存在只有一个 from 没有 count， 或者只有 count 没有 form 的情况
        # 要是这俩参数都不写的话，默认
        #     from = current time stamp
        #     count = 20
        try:
            f = int(request.GET.get('from', int(datetime.now(tz=pytz.UTC).timestamp())))
            c = int(request.GET.get('count', 20))
            return __lost_get(f, c)
        except ValueError:
            return JsonResponse({'code': codes.INVALID_PARAM, 'msg': messages.INVALID_PARAM})

    if request.method == "POST":
        # 发布一条挂失消息
        # 需要的参数：
        #          description
        # 只需要一个参数就够了，不需要"丢失"还是"捡到"
        # 至于是丢失还是捡到，直接在前端拼接好字符串传给后端
        stu = utility.get_student_object(request)
        description = str(request.POST.get('description', 'no description here'))
        return __lost_publish(stu, description)
    return JsonResponse({'code': codes.AUTH_REQUEST_METHOD_ERROR, 'msg': messages.AUTH_REQUEST_METHOD_ERROR})


@csrf_exempt
# @validate
def api_lost_specify(request, lost_record_id):
    if request.method == "POST":
        # 我们用 POST 来更新状态。用来更新挂失的状态（从寻找中到已找到，从已找到到寻找中）
        stu = utility.get_student_object(request)
        target = request.POST.get('target', 'finding')
        return __lost_update_status(stu, lost_record_id, target)  # 内部执行权限检查

    if request.method == "DELETE":
        stu = utility.get_student_object(request)
        # 删除一条挂失记录，一般是删除自己的
        # 虽然说是删除，其实是 visible = false
        # 记得检测是否有权限 DELETE
        stu = utility.get_student_object(request)
        return __lost_delete(stu, lost_record_id)  # 内部执行权限检查

    return JsonResponse({'code': codes.AUTH_REQUEST_METHOD_ERROR, 'msg': messages.AUTH_REQUEST_METHOD_ERROR})
