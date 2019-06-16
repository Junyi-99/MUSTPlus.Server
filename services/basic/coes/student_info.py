import requests
from lxml import etree

from settings import urls


def student_information(cookies) -> dict:
    headers = urls.headers
    headers['Cookie'] = cookies
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
    result = {}  # 结果字典

    title1 = ('student_id', 'name_zh', 'name_en', 'gender',
              'birthday', 'birthplace', 'nationality')
    title2 = ('faculty', 'program', 'major', 'description',
              'remarks', 'require_credit', 'effective_intake')
    url_birthday = 'https://coes-stud.must.edu.mo/coes/StudentInfo.do'
    url_study = 'https://coes-stud.must.edu.mo/coes/StudyPlanGroup.do'
    ret1 = requests.get(url=url_birthday, headers=headers)
    ret2 = requests.get(url=url_study, headers=headers)
    with open('ret1.html', 'wb') as f:
        f.write(ret1.text.encode('utf-8'))
        f.close()
    with open('ret2.html', 'wb') as f:
        f.write(ret2.text.encode('utf-8'))
        f.close()
    html1 = etree.HTML(ret1.text)
    html2 = etree.HTML(ret2.text)
    info1 = html1.xpath("//td[@class='data']/table[1]")
    info2 = html2.xpath("//td[@class='data']/table[1]")
    print(info1, info2)
    # 注意这里是table[1]而不是table[1]/tbody，学校coes没有按照标准html写（妈的）
    for i in range(1, 8):
        text_list = info1[0].xpath("./tr[%d]/td[2]/text()" % (i,))
        text = ""
        for txt in text_list:
            text = text + txt
        result[title1[i - 1]] = text.strip()
    for i in range(1, 8):
        text_list = info2[0].xpath("./tr[%d]/td[2]/text()" % (i,))
        text = ""
        for txt in text_list:
            text = text + txt
        result[title2[i - 1]] = text.strip()
        # xpath 对于多行文本会搞出来的 list 可能有好多元素，所以我们要拼接一下
    return result
