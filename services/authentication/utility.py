from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest

from services.student.models import Student


# 通过 GET 请求参数中的 token 参数，获得对应的 student 对象
# 注意：本函数给定 token 即获取对象，无 token 有效期验证功能
# 注意：本函数给定 token 即获取对象，无 token 有效期验证功能
# 注意：本函数给定 token 即获取对象，无 token 有效期验证功能
def get_student_object(request: WSGIRequest) -> Optional[Student]:
    token = str(request.GET.get('token', ""))
    if token == "":
        return None
    try:
        stu = Student.objects.get(token=token)
    except ObjectDoesNotExist:
        return None
    return stu
