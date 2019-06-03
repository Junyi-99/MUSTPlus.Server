from django.urls import path

from Services.Timetable import views

urlpatterns = [
    path('', views.timetable),

]
