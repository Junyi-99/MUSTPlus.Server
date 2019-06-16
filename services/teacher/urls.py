from django.urls import path

from services.teacher import views

urlpatterns = [
    path('<str:name_zh>', views.api_teacher, name='(get) Get teacher Details'),
]
