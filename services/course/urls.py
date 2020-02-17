from django.urls import path

from services.course import views

urlpatterns = [
    path('init', views.init),
    path('<int:course_id>', views.api_course, name='course detail'),
    path('<int:course_id>/comment', views.api_comment, name='get & post & delete'),
    path('<int:course_id>/ftp', views.api_ftp, name='get & post & delete'),
    path('thumbs_up', views.api_thumbs_up, name='post & delete'),
    path('thumbs_down', views.api_thumbs_down, name='post & delete'),
]
