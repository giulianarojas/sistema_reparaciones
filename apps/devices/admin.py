from django.contrib import admin
from .models import DeviceType, Brand, Device

admin.site.register(DeviceType)
admin.site.register(Brand)
admin.site.register(Device)
