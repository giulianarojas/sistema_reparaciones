from django.urls import path
from . import views

urlpatterns = [
    path('', views.repair_list, name='repair_list'),
    path('nueva/', views.repair_create, name='repair_create'),
    path('<int:repair_id>/', views.repair_detail, name='repair_detail'),
    path('<int:repair_id>/editar/', views.repair_update, name='repair_update'),
    path('<int:repair_id>/estado/', views.repair_update_status, name='repair_update_status'),
    path('<int:repair_id>/pago/', views.repair_payment, name='repair_payment'),
    path('suggestions/', views.get_suggestions, name='repair_suggestions'),
    path('get-customer-devices/', views.get_customer_devices, name='get_customer_devices'),
]
