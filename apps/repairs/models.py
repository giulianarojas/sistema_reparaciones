from django.db import models
from apps.devices.models import Device
from apps.users.models import User

#modelo para agrupar problemas similares y alimentar las sugerencias futuras
class ProblemCategory(models.Model):
    #nombre de la categoría (ej: "no da video" "no enciende" etc)
    name=models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Repair(models.Model):
    #los estados posibles de la reparación
    class Status(models.TextChoices):
        RECEIVED = "received", "Recibido"
        DIAGNOSING = "diagnosing", "Diagnosticando"
        WAITING_PARTS = "waiting_parts", "En espera de repuestos"
        IN_PROGRESS = "in_progress", "En reparación"
        COMPLETED = "completed", "Finalizado"
        DELIVERED = "delivered", "Entregado"
        CANCELLED = "cancelled", "Cancelado"

    #relacion con el equipo: un equipo puede tener muchas reparaciones
    device=models.ForeignKey(Device, on_delete=models.CASCADE, related_name="repairs")
     
    #tecnico asignado a la reparacion, protegido para no borrar reparaciones si se borra el usuario
    technician = models.ForeignKey(User, on_delete=models.PROTECT)
 
    #categoria del problema para alimentar la base de conocimiento a futuro
    problem_category = models.ForeignKey(ProblemCategory, on_delete=models.PROTECT, related_name="repairs")

    reported_problem = models.TextField()

    diagnosis = models.TextField(blank=True, null=True)

    proposed_solution = models.TextField(blank=True, null=True)

    performed_procedure = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=Status.choices,default=Status.RECEIVED)

    entry_date= models.DateTimeField(auto_now_add=True)

    delivery_date=models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
            return f"Repair #{self.id}"

class RepairHistory(models.Model):
    repair = models.ForeignKey(Repair, on_delete=models.CASCADE, related_name="history")

    previous_status= models.CharField(max_length=20, choices=Repair.Status.choices)

    new_status = models.CharField(max_length=20, choices=Repair.Status.choices)

    changed_by = models.ForeignKey(User, on_delete=models.PROTECT)

    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.repair} - {self.new_status}"