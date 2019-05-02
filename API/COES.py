# 这个文件主要是与COES连接的部分，现在包括COES的登录
# 个人信息和课程表的获取，现在课程表的获取还没有完成
import time

import requests
from django.core.exceptions import ObjectDoesNotExist

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
def verify(userid, password) -> bool:
    url = 'https://coes-stud.must.edu.mo/coes/login.do'

    r = requests.get(url=url)
    token = get_token(r.text)
    data = {
        'userid': userid,
        'password': password,
        'submit': 'Login',
        'org.apache.struts.taglib.html.TOKEN': token
    }
    time.sleep(3.0)

    r = requests.post(url=url, data=data)
    url = 'https://coes-stud.must.edu.mo/coes/logout.do'
    requests.post(url=url, cookies=r.cookies)
    if r.text.find('<!--COES VERSION ') == -1:
        return False
    else:
        return True


# Author : Aikov
# Time :2019/4/30
# Status:Finished
def get_cookie(userid, password):
    if verify(userid, password):
        url = 'https://coes-stud.must.edu.mo/coes/login.do'
        r = requests.get(url=url)
        token = get_token(r.text)
        data = {
            'userid': userid,
            'password': password,
            'submit': 'Login',
            'org.apache.struts.taglib.html.TOKEN': token
        }
        time.sleep(3.0)
        r = requests.post(url=url, data=data)
        return r.cookies
    else:
        return 0


# Author : Aikov
# Time :2019/4/30
# Status:Finished
def get_info(userid, password):
    try:
        student = Student.objects.get(student_id=userid)
    except ObjectDoesNotExist:
        student = Student.objects.create(student_id=userid)
    cookies = get_cookie(userid, password)
    if cookies == 0:
        return 0
    # Find info on personal info
    url = 'https://coes-stud.must.edu.mo/coes/StudentInfo.do'
    r = requests.get(url=url, cookies=cookies)
    # Find Chinese name
    tar = 'Name in Chinese:&nbsp;</td> <td class="blackfont"> '
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('  </td>', __start=pos1)
    student.name_zh = r.text[pos1:pos2]
    # Find English name
    tar = 'Name in English:&nbsp;</td> <td class="blackfont"> '
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('  </td>', __start=pos1)
    student.name_en = r.text[pos1:pos2]
    # Find sex
    tar = 'Gender:&nbsp;</td> <td class="blackfont">'
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('</td>', __start=pos1)
    student.sex = r.text[pos1:pos2]
    # Find birthday
    tar = 'Date of Birth:&nbsp;</td> <td class="blackfont">'
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('</td>', __start=pos1)
    date = r.text[pos1:pos2]
    date = date.split('/')
    student.birthday.day = int(date[0])
    student.birthday.mouth = int(date[1])
    student.birthday.year = int(date[2])
    # Find info on study plan
    url = 'https://coes-stud.must.edu.mo/coes/StudyPlanGroup.do'
    r = requests.get(url=url, cookies=cookies)
    # Find Faculty
    tar = 'Faculty:&nbsp;</td> <td class="blackfont">'
    pos1 = r.text.find(tar) + tar.__len__()
    pos2 = r.text.find('</td>', __start=pos1)
    name = r.text[pos1:pos2]
    try:
        faculty = Faculty.objects.get(name_en=name)
    except ObjectDoesNotExist:
        faculty = Faculty.objects.get(name_zh=name)
    student.faculty_id = faculty.id
    # Find Major
    tar = 'Major:&nbsp;'
    pos = r.text.find(tar)
    # 不知道为什么两个tar之间在源码里有一个回车，这样规避一下
    tar = '</td> <td class="blackfont">  '
    pos1 = r.text.find(tar, __start=pos) + tar.__len__()
    pos2 = r.text.find('  </td>', __start=pos1)
    name = r.text[pos1:pos2]
    try:
        major = Major.objects.get(name_en=name)
    except ObjectDoesNotExist:
        major = Major.objects.get(name_zh=name)
    student.major_id = major.id
    # 已经从COES爬完了个人信息
    student.save()
    url = 'https://coes-stud.must.edu.mo/coes/logout.do'
    requests.post(url=url, cookies=r.cookies)


# Author:Aikov
# Time:2019/5/2
# Status:Finished
def get_class(userid, password, intake):
    cookies = get_cookie(userid, password)
    if cookies == 0:
        return 0
    url = 'https://coes-stud.must.edu.mo/coes/AcademicRecordsForm.do'
    r = requests.get(url=url)
    token = get_token(r.text)
    data = {
        'formAction': 'Timetable',
        'intake': intake,
        'org.apache.struts.taglib.html.TOKEN': token
    }
    r = requests.post(url=url, data=data, cookies=cookies)
    pos = r.text.find('<option value="')
    count = 0
    while r.text.find('<option value=', __start=pos) != -1:
        pos = r.text.find('<option value=', __start=pos)
        count = count + 1
    week = 1
    while week != count:
        data = {
            'formAction': 'Timetable',
            'intake': 'intake',
            'org.apache.struts.taglib.html.TOKEN': get_token(r.text),
            'week': str(week)
        }
        r = requests.post(url=url, data=data)
        process_timetable(r.text)
        week = week + 1


# Author:Aikov
# Time:2019/5/2
# Status:Unfinished
def process_timetable(body):
    pos1 = body.find('var timetable = new TimeTable();') + 'var timetable = new TimeTable();'.__len__()
    pos2 = body.find(' timetable.drawTimeTable();')
    body = body[pos1:pos2]
    body = body.replace('\n', '')
    body = body.replace('+\' - \'+', ',')
    body = body.replace('&quot;', '')
    body = body.replace('timetable.add(', '')
    body = body.replace('\'', '')
    body = body.split(');')
    for count in range(0, body.__len__()):
        temp = body[count].split(',')
        try:
            course = Course.objects.get(course_id=temp[3], course_class=temp[5])
        except ObjectDoesNotExist:
            course = Course.objects.create(course_id=temp[3], course_class=temp[5])
            course.date_start.month = date_switch(temp[8])[0]
            course.date_start.day = date_switch(temp[8])[1]
            course.date_end.month = date_switch(temp[9])[0]
            course.date_end.day = date_switch(temp[9])[1]
            classroom = ClassRoom.objects.get(name_en=temp[6])
            course.classroom_id = classroom.id
            course.time_start.hour = time_switch(temp[1])[0]
            course.time_start.minute = time_switch(temp[1])[1]
            course.time_end.hour = time_switch(temp[2])[0]
            course.time_end.minute = time_switch(temp[2])[1]
            course.save()


def date_switch(body) -> list:
    month = body[0:2]
    day = body[3:]
    day = int(day)
    if month == 'Jan':
        month = 1
    elif month == 'Feb':
        month = 2
    elif month == 'Mar':
        month = 3
    elif month == 'Apr':
        month = 4
    elif month == 'May':
        month = 5
    elif month == 'Jun':
        month = 6
    elif month == 'Jul':
        month = 7
    elif month == 'Aug':
        month = 8
    elif month == 'Sep':
        month = 9
    elif month == 'Oct':
        month = 10
    elif month == 'Nov':
        month = 11
    elif month == 'Dec':
        month = 12
    a = [month, day]
    return a


def time_switch(body) -> list:
    _time = body.split(':')
    h = int(_time[0])
    m = int(_time[1])
    a = [h, m]
    return a




