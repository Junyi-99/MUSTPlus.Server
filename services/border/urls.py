from django.urls import path

from services.border import views

urlpatterns = [
    path('<int:port>', views.api_border, name='Border Gate Information'),
]
