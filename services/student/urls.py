from django.urls import path

from services.student import views

urlpatterns = [
    path('me', views.student_me, name='my profile'),
    path('<str:student_id>', views.student_get, name="other student's profile"),
]
