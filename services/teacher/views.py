from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from mustplus.decorators import require_get
from services.authentication.decorators import validate
from services.teacher.models import Teacher, TeachCourse
from settings import codes, messages


@require_get
@validate
def api_teacher(request, name_zh):
    try:
        teacher = Teacher.objects.get(name_zh=name_zh)
        teaches = TeachCourse.objects.filter(teacher=teacher).order_by('-intake')
        courses = []
        for teach in teaches:
            courses.append({
                'intake': teach.intake,
                'course_code': teach.course.course_code,
                'name_zh': teach.course.name_zh,
                'credit': teach.course.credit,
                'faculty': teach.course.faculty
            })
        return JsonResponse({
            'code': codes.OK,
            'msg': messages.OK,
            'name_zh': teacher.name_zh,
            'name_en': teacher.name_en,
            'faculty': '' if teacher.faculty is None else teacher.faculty.name_zh,
            'avatar_url': teacher.avatar_url,
            'position': teacher.position,
            'email': teacher.email,
            'office_room': teacher.office_room,
            'office_hour': teacher.office_hour,
            'courses': courses
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'code': codes.TEACHER_ID_NOT_FOUNT,
            'msg': messages.TEACHER_ID_NOT_FOUNT
        })
