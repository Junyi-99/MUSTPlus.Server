from django.urls import path

from Services.Authentication import views

urlpatterns = [
    path('login', views.login, name='Login MUST+'),
    path('logout', views.logout, name='Logout MUST+'),
    path('hash', views.hash, name='Get Login Hash'),
]