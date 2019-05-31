from django.urls import path
from Services.Timetable import views
urlpatterns = [
    path('timetable', views.get_timetable),

]
