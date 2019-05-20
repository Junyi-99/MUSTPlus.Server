from django.urls import path

from Services.Basic import views

urlpatterns = [
    path('init/faculties', views.init_faculties),
    path('init/departments', views.init_departments),
]