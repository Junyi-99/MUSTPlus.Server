import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from lxml import etree

from services.basic.query import get_faculty, get_department
from services.basic.views import init_faculties, init_departments
from services.news.models import Document, Announcement, Attachment
from settings import codes, messages, urls


# such as: 1709853di011002
def login(username, password):
    init_faculties(None)
    init_departments(None)
    data = {
        'lang': 'BIG5',
        'studno': username,
        'passwd': password,
        'submit': '提交'
    }

    r = requests.post(url=urls.INTRANET_LOGIN, data=data, headers=urls.headers)
    if 'mmLoadMenus' in r.text:
        print("Login successful")
        # TODO: Logger
        return r.cookies
    else:
        print("Login failed.")
        return 0


# 获取更多通告
def get_more_news(cookies):
    ret = requests.get(url=urls.INTRANET_MORE_NEWS, headers=urls.headers, cookies=cookies)
    return ret.text


# 获取通告
def get_news(cookies):
    ret = requests.get(url=urls.INTRANET_NEWS, headers=urls.headers, cookies=cookies)
    return ret.text


# modified
def view(faculty, department, date, id, news, deptType, lang, viewname, cookies) -> bool:
    try:
        ret = requests.post(urls.INTRANET_VIEW_CONTENT,
                            data={'id': id, 'infoType': news,
                                  'deptType': deptType, 'langType': lang},
                            headers=urls.headers, cookies=cookies)
        html = etree.HTML(ret.text)
        table = html.xpath('//body/table/tr/td/table/tr[4]/td/table/tr[2]/td/table')[0]
        title = viewname
        content = table.xpath("./tr[2]/td")[0]
        content = etree.tostring(content, encoding='unicode')
        downloads = table.xpath("./tr/td/a")

        try:
            date = datetime.strptime(date, "%Y-%m-%d")
            announcement = Announcement.objects.get(title=title, content=content,
                                                    faculty_id=get_faculty(faculty, False),
                                                    department_id=get_department(department, False), publish_time=date)
        except ObjectDoesNotExist:
            announcement = Announcement(title=title, content=content, faculty_id=get_faculty(faculty, False),
                                        department_id=get_department(department, False), publish_time=date)
            announcement.save()

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
            document = Document.objects.get(faculty_id=get_faculty(faculty, False),
                                            department_id=get_department(department, False), title=title,
                                            publish_time=publish_time, url=url)
        except ObjectDoesNotExist:
            document = Document(faculty_id=get_faculty(faculty, False),
                                department_id=get_department(department, False), title=title,
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
        title = e['title']
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
# 结果直接存在数据库里（proc_news_list实现了自动去重，不用担心数据库元素重复）
def proc_more_news(s, cookies):
    soup = BeautifulSoup(s, 'html.parser')
    ret = soup.find_all(attrs={'class': 'link_b'})

    news_list = []
    for e in ret:
        e = e.find('a')
        t = str(e)
        pos1 = t.find('>')
        pos2 = t.rfind('<')
        title = t[pos1 + 1:pos2].replace('\xa0', '').strip()
        pos1 = title.find(')')
        news_list.append({
            'fac_dep': title[1:pos1].strip(),  # faculties or departments
            'title': title[pos1 + 1:-10].strip(),
            'date': title[-10:].strip(),
            'url': str(e['onclick'].strip()),
        })
    proc_news_list(news_list, cookies)


# 爬取 一般 通告（内容较少，intranet 响应速度较快）
# 结果直接存在数据库里（proc_news_list实现了自动去重，不用担心数据库元素重复）
def proc_news(s, cookies):
    html = etree.HTML(s)

    faculties_departments = html.xpath("//tr/td[1]/text()")
    titles = html.xpath("//tr/td[2]/span/a/text()")
    links = html.xpath("//tr/td[2]/span/a/@onclick")
    dates = html.xpath("//tr/td[3]/text()")

    news_list = []
    for i in range(0, len(faculties_departments)):
        news_list.append({
            'fac_dep': faculties_departments[i].strip(),  # faculties or departments
            'title': titles[i].strip(),
            'date': dates[i].strip(),
            'url': links[i].strip(),
        })

    proc_news_list(news_list, cookies)


def intranet_update_normal(request):
    try:
        c = login(request.GET['username'], request.GET['password'])
        s = get_news(c)
        proc_news(s, c)
        return HttpResponse(json.dumps({"code": codes.OK, "msg": messages.OK}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({"code": codes.INTERNAL_ERROR, "msg": messages.INTERNAL_ERROR}))


def intranet_update_more(request):
    try:
        c = login(request.GET['username'], request.GET['password'])
        s = get_more_news(c)
        proc_more_news(s, c)
        return HttpResponse(json.dumps({"code": codes.OK, "msg": messages.OK}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({"code": codes.INTERNAL_ERROR, "msg": messages.INTERNAL_ERROR}))
