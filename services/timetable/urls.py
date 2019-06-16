from django.urls import path

from services.timetable import views

urlpatterns = [
    path('', views.timetable),
]
