from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('nuevo/', views.customer_create, name='customer_create'),
    path('<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('crear-ajax/', views.create_customer_ajax, name='create_customer_ajax'),
]
