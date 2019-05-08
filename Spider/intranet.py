import requests
import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from lxml import etree

from Settings import Codes, Messages, URLS
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


# such as: 1709853di011002
def login(username, password):
    data = {
        'lang': 'BIG5',
        'studno': username,
        'passwd': password,
        'submit': '提交'
    }

    r = requests.post(url=INTRANET_LOGIN, data=data, headers=URLS.headers)
    if 'mmLoadMenus' in r.text:
        print("Login successful")
        # TODO: Logger
        return r.cookies
    else:
        print("Login failed.")
        return 0


# 获取更多通告
def get_more_news(cookies):
    ret = requests.get(url=INTRANET_MORE_NEWS, headers=URLS.headers, cookies=cookies)
    return ret.text


# 获取通告
def get_news(cookies):
    ret = requests.get(url=INTRANET_NEWS, headers=URLS.headers, cookies=cookies)
    return ret.text


# Get Faculty object by giving name
def faculty_name_id(name_zh):
    try:
        faculty = Faculty.objects.get(name_zh=name_zh)
        return faculty
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        print("Exception in faculty_name_id(%s): %s" % (name_zh, e))
        return None


# Get a Department object by giving name
def department_name_id(name_zh):
    try:
        department = Department.objects.get(name_zh=name_zh)
        return department
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        print("Exception in department_name_id(%s): %s" % (name_zh, e))
        return None


# modified
def view(faculty, department, date, id, news, deptType, lang, viewname, cookies) -> bool:
    try:
        ret = requests.post(INTRANET_VIEW_CONTENT,
                            data={'id': id, 'infoType': news,
                                  'deptType': deptType, 'langType': lang},
                            headers=URLS.headers, cookies=cookies)
        html = etree.HTML(ret.text)
        table = html.xpath('//body/table/tr/td/table/tr[4]/td/table/tr[2]/td/table')[0]
        title = table.xpath("./tr[1]/td/b/font/text()")[0]
        content = table.xpath("./tr[2]/td")[0]
        content = etree.tostring(content, encoding='unicode')
        downloads = table.xpath("./tr/td/a")

        try:
            date = datetime.strptime(date, "%Y-%m-%d")
            announcement = Announcement.objects.get(title=title, content=content, faculty_id=faculty_name_id(faculty),
                                                    department_id=department_name_id(department), publish_time=date)
        except ObjectDoesNotExist:
            announcement = Announcement(title=title, content=content, faculty_id=faculty_name_id(faculty),
                                        department_id=department_name_id(department), publish_time=date)
            announcement.save()
            # print("New Announcement saved:" + title, announcement.id)

        for d in downloads:
            try:
                Attachment.objects.get(title=d.text.strip(), url=d.attrib['onclick'], belongs_to=announcement)
            except ObjectDoesNotExist:
                attachment = Attachment(title=d.text.strip(), url=d.attrib['onclick'], belongs_to=announcement)
                attachment.save()
                # print("New Attachment saved:" + title, attachment.id)
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
        except ObjectDoesNotExist:
            document = Document(faculty_id=faculty_name_id(faculty),
                                department_id=department_name_id(department), title=title,
                                publish_time=publish_time, url=url)
            document.save()
            # print("New Document saved:" + title, document.id)
        return True
        # # save file

        # for k, v in target.items():
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


# 处理 news_list 列表
def proc_news_list(news_list, cookies):
    for e in news_list:
        url = e['url']
        fd = e['fac_dep']
        title = e['title'].strip()
        date = e['date']

        if url[0] == 'v':  # if viewContent('', '', '');
            url = url[13:-3].replace("'", "")
            # Explain: [13:-3]
            # len("viewContent('") = 13, len("');") = 3
            args = url.split(", ")
            view(fd, fd, date, args[0], args[1], args[2], args[3], title, cookies)

        if url[0] == 'd':  # if downContent('');
            d_id = url[13:-3]
            down(fd, fd, title, date, url, d_id, title, cookies)


# 爬取 “更多” 通告（返回内容较多，intranet 响应速度较慢）
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
            'url': e.attrib['onclick'],
        })

    proc_news_list(news_list, cookies)


# 爬取 一般 通告（内容较少，intranet 响应速度较快）
def proc_news(s, cookies):
    html = etree.HTML(s)

    faculties_departments = html.xpath("//tr/td[1]/text()")
    titles = html.xpath("//tr/td[2]/span/a/text()")
    links = html.xpath("//tr/td[2]/span/a/@onclick")
    dates = html.xpath("//tr/td[3]/text()")

    news_list = []
    for i in range(0, len(faculties_departments)):
        news_list.append({
            'fac_dep': faculties_departments[i],  # faculties or departments
            'title': titles[i],
            'date': dates[i],
            'url': links[i],
        })

    proc_news_list(news_list, cookies)


def intranet_update_normal(request):
    try:
        c = login(request.GET['username'], request.GET['password'])
        s = get_news(c)
        proc_news(s, c)
        return HttpResponse(json.dumps({"code": Codes.OK, "msg": Messages.OK_MSG}))
    except Exception as e:
        return HttpResponse(json.dumps({"code": Codes.INTERNAL_ERROR, "msg": Messages.INTERNAL_ERROR_MSG}))


def intranet_update_more(request):
    try:
        c = login(request.GET['username'], request.GET['password'])
        s = get_more_news(c)
        proc_more_news(s, c)
        return HttpResponse(json.dumps({"code": Codes.OK, "msg": Messages.OK_MSG}))
    except Exception as e:
        return HttpResponse(json.dumps({"code": Codes.INTERNAL_ERROR, "msg": Messages.INTERNAL_ERROR_MSG}))
