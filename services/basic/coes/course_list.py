import re

import requests
from lxml import etree

FACULTIES = {
    "FI": '資訊科技學院',
    "MSB": '商學院',
    "FL": '法學院',
    "FC": '中醫藥學院',
    "FT": '酒店與旅遊管理學院',
    "FA": '人文藝術學院',
    "FMD": '醫學院',
    "SP": '藥學院',
    "UIC": '國際學院',
    "PREU": '大學先修班',
    "GSCHN": '通識-中文',
    "GSENG": '通識-英文',
    "GSGS": '通識',
    "GSMAT": '通識-數學',
    "GSPE": '通識-體育',
    "SSI": '太空科學研究所',
    "ISCR": '社會和文化研究所',
    "MERI": '澳門環境研究院',
    "MISE": '澳門系統工程研究所'
}


def get_all_pages(html_source) -> int:
    matches = re.findall(r"gotoPage\(\d+\)", html_source)
    if matches:
        return int(matches[-1][9:-1])
    return -1


def make_request(token: str, page: int, faculty: str, cookies: str) -> str:
    url = "https://coes-stud.must.edu.mo/coes/CourseSearchForm.do"
    headers = {
        'Cookie': cookies
    }
    data = {
        'org.apache.struts.taglib.html.TOKEN': token,
        'page': page,
        'formAction': 'FORM_INIT',
        'faculty': faculty,
        'courseCode': ""
    }

    ret = requests.post(url=url, data=data, headers=headers)
    return ret.text


def process_course_list(html_source: str) -> list:
    tree = etree.HTML(html_source)
    trees = tree.xpath("//td[@class='data']/table[@class='main']/tr")
    trees = trees[1:]  # remove the first element
    result = []
    for each_tree in trees:
        record = each_tree.xpath("./td/text()")
        result.append({
            "course_code": record[0],
            "name_en": record[1],
            'name_zh': record[2],
            'credit': record[3],
            'faculty': FACULTIES[record[4]]
        })
    return result

# with open("save2.html", 'rb') as f:
#     s = f.read()
#     f.close()
# process_course_list(s)
