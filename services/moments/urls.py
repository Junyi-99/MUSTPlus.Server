from django.urls import path

from services.moments import views

urlpatterns = [
    path('<int:moment_id>', views.api_moment, name='(get) Get moment details'),
]
