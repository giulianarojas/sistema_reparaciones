from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=30)
    email = models.EmailField(max_length=150, unique=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["last_name", "name"]

    def __str__(self):
        return f"{self.name} {self.last_name}"