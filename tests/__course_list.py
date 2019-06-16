import re

import requests
from lxml import etree

faculties = {
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


def __get_all_pages(html_source) -> int:
    r = re.findall(r"gotoPage\(\d+\)", html_source)
    if len(r) != 0:
        return int(r[-1][9:-1])
    return -1


def __make_request(token: str, page: int, faculty: str, cookies: str) -> str:
    headers = {
        'Cookie': cookies
    }

    URL = "https://coes-stud.must.edu.mo/coes/CourseSearchForm.do"
    data = {
        'org.apache.struts.taglib.html.TOKEN': token,
        'page': page,
        'formAction': 'FORM_INIT',
        'faculty': faculty,
        'courseCode': ""}
    r = requests.post(url=URL, data=data, headers=headers)
    return r.text


def __process_course_list(html_source: str) -> list:
    tree = etree.HTML(html_source)
    t = tree.xpath("//td[@class='data']/table[@class='main']/tr")
    t = t[1:]  # remove the first element
    result = []
    for each_t in t:
        record = each_t.xpath("./td/text()")
        result.append({
            "course_code": record[0],
            "name_en": record[1],
            'name_zh': record[2],
            'credit': record[3],
            'faculty': faculties[record[4]]
        })
    return result


def get_course_list(token: str, cookies: str) -> list:
    result = []
    for faculty in faculties:
        html_source = __make_request(token, 1, faculty, cookies)
        result.append(__process_course_list(html_source))
        for page in range(2, __get_all_pages(html_source) + 1):
            html_source = __make_request(token, page, faculty, cookies)
            result.append(__process_course_list(html_source))
    return result


result = get_course_list('', 'JSESSIONID=182DB03D67FA7ACE5C97EBAE5DBADDC9')
