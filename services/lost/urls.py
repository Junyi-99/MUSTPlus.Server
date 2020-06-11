from django.urls import path

from services.lost import views
# Lost and Found
urlpatterns = [
    path('', views.api_lost, name='获取lost列表，或发布新的lost（GET, POST）'),
    path('<int:lost_record_id>', views.api_lost_specify, name='对指定id的lost进行操作（POST，DELETE）'),
]
