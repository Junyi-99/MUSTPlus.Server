import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from services.authentication.decorators import validate
from services.basic.models import Department, Faculty
from services.news.models import Announcement, Document, Attachment
from settings import codes, messages


@validate
def student_me(request):
   pass

@validate
def student_get(request, student_id):
    pass
