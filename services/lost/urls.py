from django.urls import path

from services.lost import views
# Lost and Found
urlpatterns = [
    path('', views.api_settings, name=''),
]
