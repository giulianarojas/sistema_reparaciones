from django.urls import path
from . import views

urlpatterns = [
    path('', views.finance_dashboard, name='finance_dashboard'),
    path('gastos/', views.expense_list, name='expense_list'),
    path('gastos/nuevo/', views.expense_create, name='expense_create'),
    path('billing-period/', views.billing_period_create, name='billing_period_create'),
    path('exportar-csv/', views.export_finances_csv, name='export_finances_csv'),
]
