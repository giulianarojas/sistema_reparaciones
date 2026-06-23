from rest_framework.routers import DefaultRouter

from .views import (
    ProblemCategoryViewSet,
    RepairViewSet,
    RepairHistoryViewSet
)

router = DefaultRouter()

router.register(r"problem-category", ProblemCategoryViewSet)
router.register(r"repair", RepairViewSet)
router.register(r"repair-history", RepairHistoryViewSet)

urlpatterns = router.urls