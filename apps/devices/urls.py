from rest_framework.routers import DefaultRouter

from .views import (
    DeviceTypeViewSet,
    BrandViewSet,
    DeviceViewSet
)

router = DefaultRouter()

router.register(r"device-types", DeviceTypeViewSet)
router.register(r"brands", BrandViewSet)
router.register(r"devices", DeviceViewSet)

urlpatterns = router.urls