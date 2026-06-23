from django.db import models
from apps.customers.models import Customer

#este modelo permite que los tipo de equipos sean dinamicos
class DeviceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#modelo para marca de equipo, tambien dinamica 
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
#guarda informacion permanente del equipo, conecto con el id del cliente 

class Device(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="devices")
    
    device_type = models.ForeignKey(DeviceType, on_delete=models.PROTECT)

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

    model = models.CharField(max_length=100, blank=True, null=True)

    serial_number = models.CharField(max_length=100, blank=True, null=True)

    reception_notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add = True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model}"