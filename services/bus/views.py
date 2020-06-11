import sys
import traceback
import requests
import json

from django.http import JsonResponse

# author: hqr
def api_bus(request):
    try:
        bus_list = []
        response = requests.post(
            'https://bis.dsat.gov.mo:37013/ddbus/dynamic/station/v2',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
                'Accept-Language': 'zh-Hans;q=1.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'User-Agent': '',
                'Connection': 'keep-alive'
            },
            data={
                "BypassToken": "HuatuTesting0307",
                "HUID": "",
                "MAC": "",
                "action": "staCode",
                "appVer": "",
                "lang": "zh_cn",
                "mobile": "",
                "staCode": "10125",
            },
            verify=False,
            timeout=5
        )

        j = json.loads(response.text)
        for i in range(0, 8):
            dic = {}
            dic['direction'] = j[0]['data'][0]['routeDynamicinfo'][i]['dir']
            dic['bus_number'] = j[0]['data'][0]['routeDynamicinfo'][i]['routecode']
            dic['stop_count'] = j[0]['data'][0]['routeDynamicinfo'][i]['stopcounts']
            dic['station'] = 'wlkd'
            bus_list.append(dic)
        # weilongkeda

        response = requests.post(
            'https://bis.dsat.gov.mo:37013/ddbus/dynamic/station/v2',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
                'Accept-Language': 'zh-Hans;q=1.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'User-Agent': '',
                'Connection': 'keep-alive'
            },
            data={
                "BypassToken": "HuatuTesting0307",
                "HUID": "",
                "MAC": "",
                "action": "staCode",
                "appVer": "",
                "lang": "zh_cn",
                "mobile": "",
                "staCode": "10126",
            },
            verify=False,
            timeout=5
        )

        j = json.loads(response.text)
        for i in range(0, 7):
            dic = {}
            dic['direction'] = j[0]['data'][0]['routeDynamicinfo'][i]['dir']
            dic['bus_number'] = j[0]['data'][0]['routeDynamicinfo'][i]['routecode']
            dic['stop_count'] = j[0]['data'][0]['routeDynamicinfo'][i]['stopcounts']
            dic['station'] = 'tmgc'
            bus_list.append(dic)

        # tumugongcheng

        response = requests.post(
            'https://bis.dsat.gov.mo:37013/ddbus/dynamic/station/v2',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
                'Accept-Language': 'zh-Hans;q=1.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'User-Agent': '',
                'Connection': 'keep-alive'
            },
            data={
                "BypassToken": "HuatuTesting0307",
                "HUID": "",
                "MAC": "",
                "action": "staCode",
                "appVer": "",
                "lang": "zh_cn",
                "mobile": "",
                "staCode": "10143",
            },
            verify=False,
            timeout=5
        )

        j = json.loads(response.text)
        for i in range(0, 2):
            dic = {'direction': '', 'bus_number': '', 'stop_count': ''}
            dic['direction'] = j[0]['data'][0]['routeDynamicinfo'][i]['dir']
            dic['bus_number'] = j[0]['data'][0]['routeDynamicinfo'][i]['routecode']
            dic['stop_count'] = j[0]['data'][0]['routeDynamicinfo'][i]['stopcounts']
            dic['station'] = 'hydkd'
            bus_list.append(dic)
        ##huoyingdong keda

        response = requests.post(
            'https://bis.dsat.gov.mo:37013/ddbus/dynamic/station/v2',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
                'Accept-Language': 'zh-Hans;q=1.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'User-Agent': '',
                'Connection': 'keep-alive'
            },
            data={
                "BypassToken": "HuatuTesting0307",
                "HUID": "",
                "MAC": "",
                "action": "staCode",
                "appVer": "",
                "lang": "zh_cn",
                "mobile": "",
                "staCode": "10110",
            },
            verify=False,
            timeout=5
        )

        j = json.loads(response.text)
        for i in range(0, 2):
            dic = {'direction': '', 'bus_number': '', 'stop_count': ''}
            dic['direction'] = j[0]['data'][0]['routeDynamicinfo'][i]['dir']
            dic['bus_number'] = j[0]['data'][0]['routeDynamicinfo'][i]['routecode']
            dic['stop_count'] = j[0]['data'][0]['routeDynamicinfo'][i]['stopcounts']
            dic['station'] = 'jcdmlkdyy'
            bus_list.append(dic)
        ##jichangdamalukedayiyuan

        response = requests.post(
            'https://bis.dsat.gov.mo:37013/ddbus/dynamic/station/v2',
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip;q=1.0, compress;q=0.5',
                'Accept-Language': 'zh-Hans;q=1.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'User-Agent': '',
                'Connection': 'keep-alive'
            },
            data={
                "BypassToken": "HuatuTesting0307",
                "HUID": "",
                "MAC": "",
                "action": "staCode",
                "appVer": "",
                "lang": "zh_cn",
                "mobile": "",
                "staCode": "10127",
            },
            verify=False,
            timeout=5
        )

        j = json.loads(response.text)
        for i in range(0, 9):
            dic = {}
            dic['direction'] = j[0]['data'][0]['routeDynamicinfo'][i]['dir']
            dic['bus_number'] = j[0]['data'][0]['routeDynamicinfo'][i]['routecode']
            dic['stop_count'] = j[0]['data'][0]['routeDynamicinfo'][i]['stopcounts']
            dic['station'] = 'xhtd'
            bus_list.append(dic)
        ##xinhaotiandi
        return JsonResponse({'code': 0, 'msg': '', 'data': bus_list})
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return JsonResponse({'code': 0, 'msg': '', 'data': {'direction':'error','bus_number':'exception','stop_count':-1,'station':'none'}})