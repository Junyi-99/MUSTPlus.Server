from django.urls import path

from services.news import views

urlpatterns = [
    path('faculty/<str:faculty_name_zh>', views.api_news_faculty, name='faculty news'),
    path('department/<str:department_name_zh>', views.api_news_department, name='department news'),
    path('announcements', views.api_news_announcements, name='news announcements'),
    path('documents', views.api_news_documents, name='news documents'),
    path('banners', views.api_news_banners, name='news banners'),
    path('all', views.api_news_all, name='all news'),
]
