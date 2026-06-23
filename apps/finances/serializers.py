from rest_framework import serializers
from .models import BillingPeriod,RepairFinance, ExpenseCategory, Expense

class BillingPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingPeriod
        fields = "_all_"

class RepairFinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairFinance
        fields = "_all_"

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = "_all_"

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = "_all_"
