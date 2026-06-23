from rest_framework.routers import DefaultRouter

from .views import (
    BillingPeriodViewSet,
    RepairFinanceViewSet,
    ExpenseCategoryViewSet,
    ExpenseViewSet
)

router = DefaultRouter()

router.register(r"billing-period", BillingPeriodViewSet)
router.register(r"repair-finance", RepairFinanceViewSet)
router.register(r"expense-category", ExpenseCategoryViewSet)
router.register(r"expense", ExpenseViewSet)

urlpatterns = router.urls