from django.urls import path

from services.authentication import views

urlpatterns = [
    path('login', views.login, name='Login MUST+'),
    path('logout', views.logout, name='Logout MUST+'),
    path('hash', views.get_hash, name='Get Login Hash'),
]
