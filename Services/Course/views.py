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
        Course.objects.get(course_code=course_code, course_class=course_class)
        print("Course ", course_code, name_zh, "Exist!~")
    except ObjectDoesNotExist:
        course = Course(
            course_code=course_code,
            course_class=course_class,
            name_zh=name_zh,
            name_en=name_en,
            credit=credit,
            faculty=faculty,
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
            html_source = make_request(token, 1, faculty, cookie)

            for l in process_course_list(html_source):
                save_course(
                    l["course_code"].strip(), 'EMPTY',
                    l['name_zh'].strip(), l['name_en'].strip(),
                    l['credit'].strip(), get_faculty(l['faculty'].strip())
                )

            for page in range(2, get_all_pages(html_source) + 1):
                html_source = make_request(token, page, faculty, cookie)
                for l in process_course_list(html_source):
                    save_course(
                        l["course_code"].strip(), 'EMPTY',
                        l['name_zh'].strip(), l['name_en'].strip(),
                        l['credit'].strip(), get_faculty(l['faculty'].strip())
                    )
                print(page)

    except Exception as e:
        print(e)
        traceback.print_exc(file=sys.stdout)

    return HttpResponse("")
