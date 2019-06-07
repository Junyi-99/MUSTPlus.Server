from django.urls import path

from Services.Course import views

urlpatterns = [
    path('init', views.init),
    path('<int:course_id>', views.api_course, name='course detail'),
    path('<int:course_id>/comment', views.api_comment, name='(get&post&delete)course comment'),
    path('<int:course_id>/comment/thumbs_up', views.api_comment, name='(post&delete)thumbs up a course comment'),
    path('<int:course_id>/comment/thumbs_down', views.api_comment, name='(post&delete)thumbs up a course comment'),
]
