from django.contrib import admin
from .models import BillingPeriod, RepairFinance, ExpenseCategory, Expense

admin.site.register(BillingPeriod)
admin.site.register(RepairFinance)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)

