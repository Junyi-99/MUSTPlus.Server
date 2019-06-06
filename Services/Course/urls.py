from django.urls import path

from Services.Course import views

urlpatterns = [
    path('init', views.init),

]
