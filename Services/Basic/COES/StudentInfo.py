import requests
from lxml import etree

from Settings import URLS


def student_information(cookies) -> dict:
    headers = URLS.headers
    headers['Cookie'] = cookies
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
    result = {}  # 结果字典

    title1 = ('student_id', 'name_zh', 'name_en', 'gender',
              'birthday', 'birthplace', 'nationality')
    title2 = ('faculty', 'program', 'major', 'description',
              'remarks', 'require_credit', 'effective_intake')
    r1 = requests.get(url=URLS.COES_STUDENT_INFO_NAME_AND_BIRTHDAY, headers=headers)
    r2 = requests.get(url=URLS.COES_STUDENT_INFO_FACULTY_AND_MAJOR, headers=headers)
    html1 = etree.HTML(r1.text)
    html2 = etree.HTML(r2.text)
    info1 = html1.xpath("//td[@class='data']/table[1]")  # 注意这里是table[1]而不是table[1]/tbody，学校coes没有按照标准html写（妈的）
    info2 = html2.xpath("//td[@class='data']/table[1]")  # 注意这里是table[1]而不是table[1]/tbody，学校coes没有按照标准html写（妈的）
    for i in range(1, 8):
        result[title1[i - 1]] = info1[0].xpath("./tr[%d]/td[2]/text()" % (i,))[0].strip()
    for i in range(1, 8):
        result[title2[i - 1]] = info2[0].xpath("./tr[%d]/td[2]/text()" % (i,))[0].strip()
    return result
