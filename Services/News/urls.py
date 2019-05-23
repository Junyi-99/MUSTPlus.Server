from django.urls import path

from Services.News import views

urlpatterns = [
    path('faculty/<int:faculty_id>', views.news_faculty, name='faculty news'),
    path('department/<int:department_id>', views.news_department, name='department news'),
    path('banners', views.news_banners, name='news banners'),
    path('all', views.news_all, name='all news'),

]