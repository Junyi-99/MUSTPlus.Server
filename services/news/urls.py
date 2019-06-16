from django.urls import path

from services.news import views

urlpatterns = [
    path('faculty/<str:faculty_name_zh>', views.news_faculty, name='faculty news'),
    path('department/<str:department_name_zh>', views.news_department, name='department news'),
    path('banners', views.news_banners, name='news banners'),
    path('all', views.news_all, name='all news'),
]
