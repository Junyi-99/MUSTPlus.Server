from django.urls import path

from services.student import views

urlpatterns = [
    path('me', views.student_me, name='个人资料（GET）'),
    path('<str:student_id>', views.student_get, name="其他学生资料(GET)"),
]
