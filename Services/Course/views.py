import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from Services.Authentication.decorators import validate
from Services.Authentication.utility import get_student_object
from Services.Basic.COES.CourseList import faculties, make_request, process_course_list, get_all_pages
from Services.Basic.models import Faculty
from Services.Basic.query import get_faculty
from Services.Course.models import Course


def save_course(course_code: str, course_class: str, name_zh: str, name_en: str, credit: str, faculty: Faculty):
    try:
        Course.objects.get(course_code, course_class)
    except ObjectDoesNotExist:
        course = Course(
            course_code,
            course_class,
            name_zh,
            name_en,
            credit,
            faculty,
        )
        course.save()


@validate
def init(request):
    try:
        student = get_student_object(request)
        token = student.coes_token
        cookie = student.coes_cookie

        for faculty in faculties:
            print("Now faculty: ", faculty)
            html = make_request(token, 1, faculty, cookie)
            pages = get_all_pages(html)

            for page in range(1, pages + 1):  # 这里为什么要多循环一次（从1开始不从2开始）呢，因为少循环一次会让代码变丑很多
                print("Page", page)
                html_source = make_request(token, page, faculty, cookie)
                course_list = process_course_list(html_source)
                for course in course_list:
                    save_course(
                        course["course_code"].strip(),
                        'EMPTY',
                        course['name_zh'].strip(),
                        course['name_en'].strip(),
                        course['credit'].strip(),
                        get_faculty(course['faculty'].strip())
                    )


    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)
    return HttpResponse()
