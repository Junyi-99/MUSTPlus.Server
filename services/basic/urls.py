from django.urls import path

from services.basic import views

urlpatterns = [
    path('init/faculties', views.init_faculties),
    path('init/departments', views.init_departments),
    path('week', views.api_week),  # 获取当前日子是学期第几周
    path('semester', views.api_semester),  # 获取当前日子是学期第几周
]
