import requests
from lxml import etree

from Settings import URLS


# 获取网页源代码（COES_Token, COES_Cookies, 学期，周）
def get_html(token: str, cookies: str, intake: int, week: int = 0) -> str:
    headers = URLS.headers
    headers['Cookie'] = cookies
    data = {
        'org.apache.struts.taglib.html.TOKEN': token,
        'formAction': 'Timetable',
        'intake': intake,
        'week': week,  # 第几周
        'x': 53,
        'y': 12,
    }
    r = requests.post(URLS.COES_TIMETABLE, headers=headers, data=data)
    return r.text


# 获取周列表（网页源代码）：可选择的周列表
def get_week_list(html_source: str) -> list:
    html = etree.HTML(html_source)
    options = html.xpath("//select/option")
    result = []
    for e in options:
        r = e.text.split(' ')
        result.append({
            'week': r[0][1:-1],
            'value': e.attrib['value'],
            'date_from': r[1],
            'date_to': r[3]
        })
    return result


# 获取时间表（网页源代码）
def get_timetable(html_source: str) -> list:
    result = []
    month = ['\u4e00\u6708', '\u4e8c\u6708', '\u4e09\u6708',
             '\u56db\u6708', '\u4e94\u6708', '\u516d\u6708',
             '\u4e03\u6708', '\u516b\u6708', '\u4e5d\u6708',
             '\u5341\u6708', '\u5341\u4e00\u6708', '\u5341\u4e8c\u6708']

    pos1 = html_source.find('timetable.add')
    pos2 = html_source.find('timetable.dra', pos1)
    content = html_source[pos1:pos2]
    content = content.replace('timetable.add(', '')
    content = content.strip()[:-2]  # 这里有个 -2 是为了防止多 split 出来一个元素
    sp1 = content.split(');')

    for s1 in sp1:

        sp2 = s1.replace("'", '').replace('\r\n ', '').split(',')

        for i in range(len(month)):  # 将中文月份转换到数字
            sp2[8] = sp2[8].replace(month[i], "%d-" % (i + 1))

        pos_plus = sp2[8].find('+')
        result.append({
            'day': sp2[0].strip(),
            'time_begin': sp2[1],
            'time_end': sp2[2],
            'course_id': sp2[3],
            'course_name_zh': sp2[4],
            'course_class': sp2[5],
            'classroom': sp2[6],
            'teacher': sp2[7],
            'date_begin': sp2[8][:pos_plus],
            'date_end': sp2[8][pos_plus + 5:]
        })

    return result

# s = get_html()
# get_week_list(s)
# get_timetable(s.decode('utf-8'))
