from django.urls import path

from Services.Course import views

urlpatterns = [
    path('init', views.init),
    path('<int:course_id>', views.api_course, name='course detail'),
    path('<int:course_id>/comment', views.api_comment, name='course comment(get&post&delete)'),

]
