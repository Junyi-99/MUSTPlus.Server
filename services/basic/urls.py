from django.urls import path

from services.basic import views

urlpatterns = [
    path('init/faculties', views.init_faculties),
    path('init/departments', views.init_departments),
]
