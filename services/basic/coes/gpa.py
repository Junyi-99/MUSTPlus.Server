import re
import sys
import json
import traceback
from typing import Optional
import urllib3
import requests
from lxml import etree
from settings import urls

# 移除安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ensure_float(data: str)->float:
    try:
        return float(data)
    except ValueError:
        return float(0)

def proc(xpath_result: list):
    if len(xpath_result) == 0:
        return ""
    else:
        return str(xpath_result[0]).strip()

def proc2(xpath_result: list):
    if len(xpath_result) < 2:
        return ""
    else:
        return str(xpath_result[1]).strip()


def get_html(cookies: str) -> Optional[str]:
    url = 'https://coes-stud.must.edu.mo/coes/AcademicRecordsForm.do'
    data = {}
    headers = urls.headers
    headers['Cookie'] = cookies
    ret = requests.post(url=url, headers=headers, data=data, verify=False)
    if 'GPA' in ret.text:
        return ret.text
    return None


def get_gpa_list(coes_cookie: str) -> list:
    html_source = get_html(coes_cookie)
    if html_source is None:
        return []

    html = etree.HTML(html_source)

    # 注意这里是 table/tr 而不是 table/tbody，学校 coes 没有按照标准 html 写 （妈的）
    tables = html.xpath("//td[@class='data']/table[@class='main']/tr")

    result = []
    for i in range(0, len(tables), 2):
        print(i, i + 1)
        course_gp_list = []

        course_list = tables[i + 1].xpath("./td/table/tr[@class='blackfont']")
        for j in range(0, len(course_list)):
            course_gp_list.append({
                "course_code": proc(course_list[j].xpath("./td[3]/text()")),
                "course_name_zh": proc2(course_list[j].xpath("./td[4]/text()")),
                "course_class": proc(course_list[j].xpath("./td[5]/text()")),
                "course_credit": proc(course_list[j].xpath("./td[6]/text()")),
                "grade": proc(course_list[j].xpath("./td[8]/span/text()")),
                "exam_datetime": proc(course_list[j].xpath("./td[11]/text()")),
                "exam_classroom": proc(course_list[j].xpath("./td[12]/text()")),
                "exam_seat": proc2(course_list[j].xpath("./td[12]/text()")),
            })
        # print(course_gp_list)
        result.append({
            "course_intake": int(str(tables[i].xpath("./td[3]/text()")[0]).strip()),
            "total_credit": ensure_float(proc(tables[i].xpath("./td[5]/text()"))),
            "pass_credit": ensure_float(proc(tables[i].xpath("./td[7]/text()"))),
            "fail_credit": ensure_float(proc(tables[i].xpath("./td[9]/text()"))),
            "gpa_credit": ensure_float(proc(tables[i].xpath("./td[11]/text()"))),
            "gpa": ensure_float(proc(tables[i].xpath("./td[13]/text()"))),
            "accum_gpa": ensure_float(proc(tables[i].xpath("./td[15]/text()"))),
            "details": course_gp_list
        })
    return result