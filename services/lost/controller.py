import sys
import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from services.authentication import utility
from services.authentication.decorators import validate
from services.lost.controller import __update_lost_status
from services.lost.models import LostRecord
from settings import codes, messages


def __update_lost_status(student, lost_id, target):
    try:
        record = LostRecord.objects.get(id=lost_id)
        if record.student.student_id != student.student_id:
            return JsonResponse({
                'code': codes.LOST_AND_FOUND_PERMISSION_DENIED,
                'msg': codes.LOST_AND_FOUND_PERMISSION_DENIED
            })
        else:
            record.status = target
            record.save()
            return JsonResponse({
                'code': codes.OK,
                'msg': messages.OK
            })
    except ObjectDoesNotExist:
        return JsonResponse(
            {'code': codes.LOST_AND_FOUND_NO_SUCH_RECORD, 'msg': messages.LOST_AND_FOUND_NO_SUCH_RECORD})

def __lost_delete(student, lost_id):
    try:
        record = LostRecord.objects.get(id=lost_id, visible=True)
        if record.student.student_id != student.student_id:
            return JsonResponse({
                'code': codes.LOST_AND_FOUND_PERMISSION_DENIED,
                'msg': codes.LOST_AND_FOUND_PERMISSION_DENIED
            })
        else:
            record.visible = False
            record.save()
            return JsonResponse({
                'code': codes.OK,
                'msg': messages.OK
            })
    except ObjectDoesNotExist:
        return JsonResponse(
            {'code': codes.LOST_AND_FOUND_NO_SUCH_RECORD, 'msg': messages.LOST_AND_FOUND_NO_SUCH_RECORD})