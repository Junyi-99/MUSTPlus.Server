from django.urls import path

from Services.Teacher import views

urlpatterns = [
    path('<str:name_zh>', views.api_teacher, name='(get) Get Teacher Details'),
]
