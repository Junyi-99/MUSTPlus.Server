import sys
import traceback
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from services.authentication import utility
from services.authentication.decorators import validate

from services.basic.models import ClassRoom
from services.course.models import Course, Schedule
from services.student.models import TakeCourse
from services.teacher.models import TeachCourse, Teacher
from services.timetable.controller import __timetable_cache, __timetable_update
from settings import codes, messages

# Default timetable intake
from settings.server import SEMESTER


@csrf_exempt
# @validate
def api_timetable(request):
    stu = utility.get_student_object(request)
    intake = int(request.GET.get('intake', SEMESTER))
    week = int(request.GET.get('week', -1))
    if week == -1 or week < 0:
        week = 0
    return __timetable_update(stu, intake, week)