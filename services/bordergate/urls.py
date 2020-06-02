from django.urls import path

from services.bordergate import views

urlpatterns = [
    path('<int:port>', views.api_bordergate, name='Border Gate Information'),
]
