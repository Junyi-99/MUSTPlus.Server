import sys
import traceback
from django.db.models import Avg
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mustplus.decorators import require_get, require_post
from services.authentication.decorators import validate
from settings import codes, messages
import requests
import json

# Author: Paul
# Last Modified: 06/03/2020

# port 0 关闸
# port 1 横琴
# 由 caller 来做判断
def __border_gate(port: int):
    info_list = []
    if port == 0:
        response = requests.post(
            'http://www.fsm.gov.mo/psp/pspmonitor/webservice.asmx/getStatus',
            headers={'Accept': 'application/json, text/javascript, */*; q=0.01',
                     'Accept-Encoding': 'gzip, deflate',
                     'Accept-Language': 'zh-CN,zh;q=0.9',
                     'Content-Type': 'application/json; charset=UTF-8',
                     'Referer': 'http://www.fsm.gov.mo/psp/pspmonitor/mobile/PortasdoCerco.aspx',
                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                     'X-Requested-With': 'XMLHttpRequest'},
            data={}
        )

        j = json.loads(response.text)
        j = json.loads(j["d"])

        for e in j["Rt"]:
            if e["Pn"] == "2" and e["Id"] == "D":
                if e["St"] == "1":
                    info_list.append("暢通")
                elif e["St"] == "2":
                    info_list.append("繁忙")
                elif e["St"] == "3":
                    info_list.append("擠擁")
                elif e["St"] == "4":
                    info_list.append("分流")
                elif e["St"] == "5":
                    info_list.append("暫停")
                elif e["St"] == "6":
                    info_list.append("黑屏")
                info_list.append(e["Ti"])
        return info_list
    elif port == 1:
        response = requests.post(
            'http://www.fsm.gov.mo/psp/pspmonitor/webservice.asmx/getStatus',
            headers={'Accept': 'application/json, text/javascript, */*; q=0.01',
                     'Accept-Encoding': 'gzip, deflate',
                     'Accept-Language': 'zh-CN,zh;q=0.9',
                     'Content-Type': 'application/json; charset=UTF-8',
                     'Referer': 'http://www.fsm.gov.mo/psp/pspmonitor/mobile/Cotai.aspx',
                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
                     'X-Requested-With': 'XMLHttpRequest'},
            data={}
        )

        j = json.loads(response.text)
        j = json.loads(j["d"])
        for e in j["Rt"]:
            if e["Pn"] == "5" and e["Id"] == "D":
                if e["St"] == "1":
                    info_list.append("暢通")
                elif e["St"] == "2":
                    info_list.append("繁忙")
                elif e["St"] == "3":
                    info_list.append("擠擁")
                elif e["St"] == "4":
                    info_list.append("分流")
                elif e["St"] == "5":
                    info_list.append("暫停")
                elif e["St"] == "6":
                    info_list.append("黑屏")
                info_list.append(e["Ti"])
        return info_list

@require_get
#@validate
def api_border(request, port):
    if port == 0:  # 关闸
        ret = __border_gate(0)
        print(ret)
        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK,
            "port": "Bordergate",
            "status": ret[0],
            "time": ret[1]
        })
    elif port == 1:  # 横琴
        ret = __border_gate(1)
        print(ret)
        return JsonResponse({
            "code": codes.OK,
            "msg": messages.OK,
            "port": "Taipa",
            "status": ret[0],
            "time": ret[1]
        })
    else:
        return JsonResponse({
             "code": codes.BORDERGATE_ERROR_PORT_ID,
             "msg" : messages.BORDERGATE_ERROR_PORT_ID,
        })