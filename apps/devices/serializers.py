from rest_framework import serializers
from .models import DeviceType, Brand, Device


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = "_all_"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "_all_"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "_all_"