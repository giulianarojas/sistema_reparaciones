from rest_framework import viewsets

from .models import DeviceType, Brand, Device
from .serializers import (
    DeviceTypeSerializer,
    BrandSerializer,
    DeviceSerializer
)

class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer