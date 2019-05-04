import requests
import json
import re
from lxml import etree

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
        #TODO: Logger
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


def view(id, news, deptType, lang, viewname, cookies) -> bool:
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
        links = []
        for e in downloads:
            links.append({
                'title': e.text.strip(),
                'link': e.attrib['onclick'],

            })
            print(e.text.strip(), e.attrib['onclick'])
            # TODO: Saving data to database
        return True
    except Exception as e:
        print("Exception", e)
        return False


def download(dId, filename, cookies) -> bool:
    try:
        target = {'\\': '、', '/': '-', ':': '：', '*': '·',
                  '?': '？', '"': '\'', '<': '《', '>': '》', '|': '｜'}
        for k, v in target:
            filename = filename.replace(k, v)

        filename += '.pdf'
        r = requests.post(INTRANET_DOWN_CONTENT,
                          data={'dId': dId}, cookies=cookies)
        # TODO: Change save path of the downloaded file
        with open(filename, 'wb') as f:
            f.write(r.content)
            f.close()
            return True

    except Exception as e:
        print("Exception:", e)
        return False


def proc_more_news(s):
    html = etree.HTML(s)
    news = html.xpath("//span[@class='link_b']/a")
    news_list = []
    for e in news:
        title = e.text.strip().replace('\xa0', ' ')
        pos1 = title.find(')')
        pos2 = title.rfind('  20')
        news_list.append({
            'faculty': title[1:pos1],
            'title': title[pos1 + 2:pos2],
            'date': title[pos2 + 2:],
            'link': e.attrib['onclick']
        })
    print(json.dumps(news_list))


def proc_news(s):
    html = etree.HTML(s)

    faculties = html.xpath("//tr/td[1]/text()")
    titles = html.xpath("//tr/td[2]/span/a/text()")
    links = html.xpath("//tr/td[2]/span/a/@onclick")
    dates = html.xpath("//tr/td[3]/text()")

    numbers = len(faculties)
    if numbers != len(titles):
        raise Exception("Spider Error.")
    if numbers != len(links):
        raise Exception("Spider Error.")
    if numbers != len(dates):
        raise Exception("Spider Error.")

    news_list = []
    for i in range(0, len(faculties)):
        news_list.append({
            'faculty': faculties[i],
            'title': titles[i].strip(),
            'link': links[i],
            'date': dates[i],
        })
        # if links[i][0] == 'v':  # if viewContent()
        #     links[i] = links[i][13:-3].replace("'", "")
        #     args = links[i].split(", ")
        #     print(args)
        #     view(args[0], args[1], args[2], args[3], titles[i], c)
        # continue

        # if linkes[i][0] == 'd: # if downContent()
        #     print("Downloading %s ..." % titles[i], end='')
        #     if download(linkes[i][13:-3], "%s_%s" % (faculties[i], titles[i]), c):
        #         print(" Finished.")
        #     else:
        #         print(" Failed.")

    print(json.dumps(news_list))

# c = login()
# s = getMoreNews(c)
# proc_more_news(s)
