import sys
import traceback

from django.http import JsonResponse


def api_lost(request):
    if request.method == "GET":
        # 获取一部分挂失数据（要支持分页功能）
        pass
    if request.method=="POST":
        # 发布一个挂失消息
        pass
    return JsonResponse({'code': 0, 'msg': ''})


def api_lost_specify(request, lost_id):
    if request.method=="GET":
        # 获取单条挂失的详细信息（没啥用，设计上就没对这种情况进行设计）
        pass
    if request.method=="POST":
        # 我们用 POST 来更新状态
        pass
    if request.method=="DELETE":
        # 检测是否有权限 DELETE
        pass

    return JsonResponse({'code': 0, 'msg': ''})
