import requests
import json
import re
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from lxml import etree

from MUSTPlus import codes, msg_zh
from MUSTPlus.models import Faculty
from MUSTPlus.models import Department
from MUSTPlus.models import Document
from MUSTPlus.models import Attachment
from MUSTPlus.models import Announcement

INTRANET_LOGIN = 'https://intranet.must.edu.mo/student/LoginServlet'
INTRANET_LOGOUT = 'https://intranet.must.edu.mo/student/Logout'
INTRANET_NEWS = 'https://intranet.must.edu.mo/student/jumpXtgNews.jsp'
INTRANET_MORE_NEWS = 'https://intranet.must.edu.mo/student/jumpMoreXtgNews.jsp'
INTRANET_VIEW_CONTENT = 'https://intranet.must.edu.mo/student/InfoServlet'
INTRANET_DOWN_CONTENT = 'https://intranet.must.edu.mo/student/DownloadFile'

# 职业素养
headers = {
    'User-Agent': 'MUSTPlus/5.0 (Server Spider 1.0; Ubuntu; x64)',
}


# such as: 1709853di011002
def login(username, password):
    data = {
        'lang': 'BIG5',
        'studno': username,
        'passwd': password,
        'submit': '提交'
    }

    r = requests.post(url=INTRANET_LOGIN, data=data, headers=headers)
    if 'mmLoadMenus' in r.text:
        print("Login successful")
        # TODO: Logger
        return r.cookies
    else:
        print("Login failed.")
        return 0


# 获取更多通告
def get_more_news(cookies):
    ret = requests.get(url=INTRANET_MORE_NEWS, headers=headers, cookies=cookies)
    return ret.text


# 获取通告
def get_news(cookies):
    ret = requests.get(url=INTRANET_NEWS, headers=headers, cookies=cookies)
    return ret.text


def faculty_name_id(name_zh):
    try:
        faculty = Faculty.objects.get(name_zh=name_zh)
        return faculty
    except ObjectDoesNotExist:
        return None


def department_name_id(name_zh):
    try:
        department = Department.objects.get(name_zh=name_zh)
        return department
    except ObjectDoesNotExist:
        return None


# modified
def view(faculty, department, date, id, news, deptType, lang, viewname, cookies) -> bool:
    try:
        ret = requests.post(INTRANET_VIEW_CONTENT,
                            data={'id': id, 'infoType': news,
                                  'deptType': deptType, 'langType': lang},
                            headers=headers, cookies=cookies)
        html = etree.HTML(ret.text)
        r = html.xpath('//body/table/tr/td/table/tr[4]/td/table/tr[2]/td/table')
        r = r[0]

        title = r.xpath("./tr[1]/td/b/font/text()")[0]
        content = r.xpath("./tr[2]/td")[0]
        content = etree.tostring(content, encoding='unicode')
        downloads = r.xpath("./tr/td/a")

        try:
            date = datetime.strptime(date, "%Y-%m-%d")
            announcement = Announcement.objects.get(title=title, content=content, faculty_id=faculty_name_id(faculty),
                                                    department_id=department_name_id(department), publish_time=date)
        except ObjectDoesNotExist:
            announcement = Announcement(title=title, content=content, faculty_id=faculty_name_id(faculty),
                                        department_id=department_name_id(department), publish_time=date)
            announcement.save()

        for d in downloads:
            try:
                Attachment.objects.get(title=d.text.strip(), url=d.attrib['onclick'], belongs_to=announcement)
            except ObjectDoesNotExist:
                attachment = Attachment(title=d.text.strip(), url=d.attrib['onclick'], belongs_to=announcement)
                attachment.save()

        return True
    except Exception as e:
        print("Exception in intranet.view", e)
        return False


def down(faculty, department, title, publish_time, url, dId, filename, cookies) -> bool:
    try:
        target = {'\\': '、', '/': '-', ':': '：', '*': '·',
                  '?': '？', '"': '\'', '<': '《', '>': '》', '|': '｜'}
        try:
            publish_time = datetime.strptime(publish_time, "%Y-%m-%d")
            document = Document.objects.get(faculty_id=faculty_name_id(faculty),
                                            department_id=department_name_id(department), title=title,
                                            publish_time=publish_time, url=url)
        except ObjectDoesNotExist as e:
            document = Document(faculty_id=faculty_name_id(faculty),
                                department_id=department_name_id(department), title=title,
                                publish_time=publish_time, url=url)
            document.save()
        return True
        # # save file
        # for k, v in target:
        #     filename = filename.replace(k, v)
        # filename += '.pdf'
        # r = requests.post(INTRANET_DOWN_CONTENT,
        #                   data={'dId': dId}, cookies=cookies)
        # # TODO: Change save path of the downloaded file
        # with open(filename, 'wb') as f:
        #     f.write(r.content)
        #     f.close()
        #     return True

    except Exception as e:
        print("Exception in intranet.down", e)
        return False

def proc_news_list(news_list, cookies):
    for e in news_list:
        if e['link'][0] == 'v':  # if viewContent()
            e['link'] = e['link'][13:-3].replace("'", "")
            args = e['link'].split(", ")
            print(datetime.strptime(e['date'], "%Y-%m-%d"))
            datetime.strptime(e['date'], "%Y-%m-%d")
            view(e['fac_dep'], e['fac_dep'], e['date'], args[0],
                 args[1], args[2], args[3], e['title'].strip(), cookies)
        if e['link'][0] == 'd':  # if downContent()
            dId = e['link'][13:-3]
            print(datetime.strptime(e['date'], "%Y-%m-%d"))
            down(e['fac_dep'], e['fac_dep'], e['title'].strip(),
                 e['date'], "", dId, e['title'].strip(), cookies)

        #print("Processed:", e['title'].strip())

def proc_more_news(s, cookies):
    html = etree.HTML(s)
    news = html.xpath("//span[@class='link_b']/a")
    news_list = []
    for e in news:
        title = e.text.strip().replace('\xa0', ' ')
        pos1 = title.find(')')
        pos2 = title.rfind('  20')
        news_list.append({
            'fac_dep': title[1:pos1],  # faculties or departments
            'title': title[pos1 + 2:pos2],
            'date': title[pos2 + 2:],
            'link': e.attrib['onclick'],
        })

    proc_news_list(news_list, cookies)


def proc_news(s, cookies):
    html = etree.HTML(s)

    faculties_departments = html.xpath("//tr/td[1]/text()")
    titles = html.xpath("//tr/td[2]/span/a/text()")
    links = html.xpath("//tr/td[2]/span/a/@onclick")
    dates = html.xpath("//tr/td[3]/text()")

    numbers = len(faculties_departments)
    if numbers != len(titles):
        raise Exception("Spider Error.")
    if numbers != len(links):
        raise Exception("Spider Error.")
    if numbers != len(dates):
        raise Exception("Spider Error.")

    news_list = []
    for i in range(0, len(faculties_departments)):
        news_list.append({
            'fac_dep': faculties_departments[i],  # faculties or departments
            'title': titles[i].strip(),
            'date': dates[i],
            'link': links[i],
        })

    proc_news_list(news_list, cookies)


def intranet(request):
    c = login()
    s = get_more_news(c)
    proc_more_news(s, c)
    # s = get_news(c)
    # proc_news(s, c)
    return HttpResponse(json.dumps({"code": codes.OK, "msg": msg_zh.OK_MSG}))

# s = getMoreNews(c)
# proc_more_news(s)
