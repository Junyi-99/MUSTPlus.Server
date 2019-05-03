# 这个文件主要是与COES连接的部分，现在包括COES的登录
# 个人信息和课程表的获取
import time

import requests
from django.core.exceptions import ObjectDoesNotExist

from MUSTPlus import codes
from MUSTPlus import coes_url
from MUSTPlus.models import ClassRoom
from MUSTPlus.models import Course
from MUSTPlus.models import Faculty
from MUSTPlus.models import Major
from MUSTPlus.models import Student


# Author : Aikov
# Time :2019/4/30
# Status:Finished
def get_token(body):
    token_simple = '49057506de26d2ea640cea1847d7f3d5'
    target = 'org.apache.struts.taglib.html.TOKEN" value="'
    pos = body.find(target) + target.__len__()
    return body[pos:pos + token_simple.__len__()]


# Author : Aikov
# Time :2019/4/30
# Status:Finished
def verify(userid, password, lang):
    r = requests.get(url=coes_url.LOGIN_URL)
    token = get_token(r.text)
    data = {
        'userid': userid,
        'password': password,
        'submit': 'Login' if lang == 'en' else '登入',
        'org.apache.struts.taglib.html.TOKEN': token
    }
    time.sleep(3.0)

    r = requests.post(url=coes_url.LOGIN_URL, data=data)
    if r.text.find('<!--COES VERSION ') == -1:
        return False, 0
    else:
        return True, r.cookies


# Author : Aikov
# Time :2019/4/30
# Status: Need to improve
def get_cookie(userid, password, lang):
    return verify(userid, password, lang)[1]


def coes_logout(cookies):
    requests.post(url=coes_url.LOGOUT_URL, cookies=cookies)


# Author : Aikov
# Time :2019/4/30
# Status: Unfinished
def get_info(userid, password, lang):
    try:
        student = Student.objects.get(student_id=userid)
    except ObjectDoesNotExist:
        student = Student.objects.create(student_id=userid)
    cookies = get_cookie(userid, password, lang)
    if cookies == 0:
        return 0
    # Find info on personal info
    r = requests.get(url=coes_url.STUDENT_INFO_URL, cookies=cookies)
    r2 = requests.get(url=coes_url.STUDY_PLAN_GROUP_URL, cookies=cookies)
    coes_logout(r.cookies)
    # Find Chinese name
    tar = 'Name in Chinese:&nbsp;</td> <td class="blackfont"> ' if lang == 'en' \
        else '中文姓名:&nbsp;</td> <td class="blackfont"> '
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('  </td>', __start=pos1)
    student.name_zh = r.text[pos1:pos2]

    # Find English name
    tar = 'Name in English:&nbsp;</td> <td class="blackfont"> ' if lang == 'en' \
        else '英文姓名:&nbsp;</td> <td class="blackfont"> '
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('  </td>', __start=pos1)
    student.name_en = r.text[pos1:pos2]

    # Find sex
    tar = 'Gender:&nbsp;</td> <td class="blackfont">' if lang == 'en' \
        else '性別:&nbsp;</td> <td class="blackfont">'
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('</td>', __start=pos1)
    sex = r.text[pos1:pos2]
    if sex == 'Male' or sex == '男':
        student.sex = True
    else:
        student.sex = False
    # Find birthday
    tar = 'Date of Birth:&nbsp;</td> <td class="blackfont">' if lang == 'en' \
        else '出生日期:&nbsp;</td> <td class="blackfont">'
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('</td>', __start=pos1)
    date = r.text[pos1:pos2]
    date = date.split('/')
    student.birthday.day = int(date[0])
    student.birthday.mouth = int(date[1])
    student.birthday.year = int(date[2])
    # TODO: TOO MUCH redundant, Hardly read codes.
    # Find info on study plan

    # Find Faculty
    tar = 'Faculty:&nbsp;</td> <td class="blackfont">' \
        if lang == 'en' else '學院:&nbsp;</td> <td class="blackfont">'
    pos1 = r2.text.find(tar) + tar.__len__()
    pos2 = r2.text.find('</td>', __start=pos1)
    name_f = r2.text[pos1:pos2]

    # Find Major
    tar = 'Major:&nbsp;' \
        if lang == 'en' else '課程專業:&nbsp;'
    pos = r.text.find(tar)
    # 不知道为什么两个tar之间在源码里有一个回车，这样规避一下
    tar = '</td> <td class="blackfont">  '
    pos1 = r2.text.find(tar, __start=pos) + tar.__len__()
    pos2 = r2.text.find('  </td>', __start=pos1)
    name_m = r2.text[pos1:pos2]
    try:
        if lang == 'en':
            faculty = Faculty.objects.get(name_en=name_f)
            major = Major.objects.get(name_en=name_m)
        else:
            faculty = Faculty.objects.get(name_zh=name_f)
            major = Major.objects.get(name_en=name_m)
    except ObjectDoesNotExist:
        return codes.OTHER_ARGUMENT_INVALID
    student.faculty_id = faculty.id
    student.major_id = major.id
    # 已经从COES爬完了个人信息
    student.save()


# Author:Aikov
# Time:2019/5/2
# Status:Finished
def get_class(userid, password, intake, lang):
    cookies = get_cookie(userid, password, lang)
    if cookies == 0:
        return 0
    r = requests.get(url=coes_url.TIME_TABLE_URL)
    token = get_token(r.text)
    data = {
        'formAction': 'Timetable',
        'intake': intake,
        'org.apache.struts.taglib.html.TOKEN': token,
    }
    r = requests.post(url=coes_url.TIME_TABLE_URL, data=data, cookies=cookies)
    pos = r.text.find('<option value="')
    count = 0
    while r.text.find('<option value=', __start=pos) != -1:
        pos = r.text.find('<option value=', __start=pos)
        count = count + 1
    week = 1
    # TODO: 请解释一下
    # 1、下面的代码的目的     这一段代码是为了逐周获取课表
    # 2、count和week的关系   count是一共有多少个周，week是当前正在获取的周

    while week != count:
        data = {
            'formAction': 'Timetable',
            'intake': 'intake',
            'org.apache.struts.taglib.html.TOKEN': get_token(r.text),
            'week': str(week),
        }
        r = requests.post(url=coes_url.TIME_TABLE_URL, data=data)
        process_timetable(r.text)
        week = week + 1


# Author: Aikov and Junyi
# Time: 2019/5/2
# Status: Unfinished
def process_timetable(body):
    pos1 = body.find('var timetable = new TimeTable();')
    pos2 = body.find(' timetable.drawTimeTable();')
    body = body[pos1 + 32:pos2]
    body = body.replace('timetable.add(', '')
    body = body.replace('\n ', '')
    body = body.replace('\n', '')
    body = body.replace('+\' - \'+', ',')
    body = body.replace('&quot;', '')
    body = body.replace('\'', '')
    body = body[:-3].split(');')  # 防止split出空元素

    for e in body:
        temp = e.split(',')
        try:
            Course.objects.get(course_id=temp[3], course_class=temp[5])
        except ObjectDoesNotExist:
            course = Course.objects.create(course_id=temp[3], course_class=temp[5])
            course.date_start.month, course.date_start.day = date_switch(temp[8])
            course.date_end.month, course.date_end.day = date_switch(temp[9])
            classroom = ClassRoom.objects.get(name_en=temp[6])
            course.classroom_id = classroom.id
            course.time_start.hour, course.time_start.minute = time_switch(temp[1])
            course.time_end.hour, course.time_end.minute = time_switch(temp[2])
            course.save()


# Author: Junyi, Aikov
# Time: 2019/5/3
# Status: finished
def date_switch(body) -> tuple:
    month = body[0:3]
    day = int(body[3:])
    t = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
    for i in range(0, 12):
        if month == t[i]:
            month = i + 1
    return month, day


# Author: Aikov and Junyi
# Time: 2019/5/3
# Status: finished
def time_switch(body) -> tuple:
    _time = body.split(':')
    h = int(_time[0])
    m = int(_time[1])
    return h, m
