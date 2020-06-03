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
    for e in tables:
        if len(e.xpath("./td[3]/text()")) == 0:
            continue
        result.append({
            "course_intake": str(e.xpath("./td[3]/text()")[0]).strip(),
            "total_credit": str(e.xpath("./td[5]/text()")[0]).strip(),
            "pass_credit": str(e.xpath("./td[7]/text()")[0]).strip(),
            "fail_credit": str(e.xpath("./td[9]/text()")[0]).strip(),
            "gpa_credit": str(e.xpath("./td[11]/text()")[0]).strip(),
            "gpa": str(e.xpath("./td[13]/text()")[0]).strip(),
            "accum_gpa": str(e.xpath("./td[15]/text()")[0]).strip()
        })
    return result