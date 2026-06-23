from rest_framework import viewsets

from .models import BillingPeriod,RepairFinance, ExpenseCategory, Expense
from .serializers import (
    BillingPeriodSerializer,
    RepairFinanceSerializer,
    ExpenseCategorySerializer,
    ExpenseSerializer
)

class BillingPeriodViewSet(viewsets.ModelViewSet):
    queryset = BillingPeriod.objects.all()
    serializer_class = BillingPeriodSerializer


class RepairFinanceViewSet(viewsets.ModelViewSet):
    queryset = RepairFinance.objects.all()
    serializer_class = RepairFinanceSerializer

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer