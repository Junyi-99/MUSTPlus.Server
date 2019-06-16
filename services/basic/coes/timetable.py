import re
import sys
import traceback
from typing import Optional

import requests
from lxml import etree

from settings import urls


# 获取网页源代码（COES_Token, COES_Cookies, 学期，周）
def get_html(token: str, cookies: str, intake: int, week: int = 0) -> Optional[str]:
    url = 'https://coes-stud.must.edu.mo/coes/AcademicRecordsForm.do'
    data = {
        'org.apache.struts.taglib.html.TOKEN': token,
        'formAction': 'Timetable',
        'intake': intake,
        'x': 53,
        'y': 12,
    }
    headers = urls.headers
    headers['Cookie'] = cookies

    print("intake", intake)
    print("week", week)

    if week != 0:  # 如果 week 等于 0，请求参数里不应该有 week
        data['week'] = week
    ret = requests.post(url=url, headers=headers, data=data)

    if 'doTimetable' in ret.text:
        return ret.text
    return None


# 获取周列表（网页源代码）：可选择的周列表
def get_week_list(html_source: str) -> list:
    html = etree.HTML(html_source)
    options = html.xpath("//select/option")
    result = []
    for option in options:
        sublist = option.text.split(' ')
        result.append({
            'week': sublist[0][1:-1],
            'value': option.attrib['value'],
            'date_from': sublist[1],
            'date_to': sublist[3]
        })
    return result


# 获取时间表（网页源代码）
def get_timetable(html_source: str) -> list:
    try:
        result = []
        month = ['\u4e00\u6708', '\u4e8c\u6708', '\u4e09\u6708',
                 '\u56db\u6708', '\u4e94\u6708', '\u516d\u6708',
                 '\u4e03\u6708', '\u516b\u6708', '\u4e5d\u6708',
                 '\u5341\u6708', '\u5341\u4e00\u6708', '\u5341\u4e8c\u6708']
        with open("save.html", 'wb') as file:
            file.write(html_source.encode('utf-8'))
            file.close()

        course_list = re.findall(r'timetable.add\([\s\S]*?\);', html_source)

        for each_course in course_list:
            sp2 = each_course.replace("timetable.add(", '').replace("'", ''). \
                replace('\r', '').replace('\n ', '').replace(');', '').split(',')

            # 将中文月份转换到数字 这里要反向迭代，因为 '十二月' 会在正向迭代的时候 被 '二月' 先替换
            for i in range(len(month) - 1, -1, -1):
                sp2[-1] = sp2[-1].replace(month[i], "%d-" % (i + 1))
            print(sp2)
            pos_plus = sp2[-1].find('+')

            # Multi-teacher condition
            teacher = ""
            for i in range(7, len(sp2) - 1):
                teacher = teacher + sp2[i] + ","

            result.append({
                'day': sp2[0].strip(),
                'time_begin': sp2[1].strip(),
                'time_end': sp2[2].strip(),
                'course_code': sp2[3].strip(),
                'course_name_zh': sp2[4].strip(),
                'course_class': sp2[5].strip(),
                'classroom': sp2[6].strip(),
                'teacher': teacher[:-1].strip(),
                'date_begin': sp2[-1][:pos_plus].strip(),
                'date_end': sp2[-1][pos_plus + 5:].strip()
            })
        return result
    except Exception as exception:
        print(exception)
        traceback.print_exc(file=sys.stdout)
        return []
# Usage:
# s = get_html()
# get_week_list(s)
# get_timetable(s.decode('utf-8'))
