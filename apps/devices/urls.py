from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_list, name='device_list'),
    path('<int:device_id>/', views.device_detail, name='device_detail'),
]
