from django.db import models
from apps.repairs.models import Repair

# guardar el historial de topes de facturacion de ARCA
class BillingPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    
    # max_digits=15 permite guardar montos en pesos muy grandes (hasta miles de millones)
    billing_limit = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Period: {self.start_date} to {self.end_date} - Limit: ${self.billing_limit}"

# ingresos (Relacionado 1 a 1 con las Reparaciones)
class RepairFinance(models.Model):

    class PaymentMethod(models.TextChoices):
        CASH= "cash", "Efectivo"
        TRANSFER= "transfer", "transferencia"
        MERCADO_PAGO = "mercado_pago", "Mercado Pago"

    # OneToOneField asegura que una reparacion tenga un solo cobro final asociado
    repair = models.OneToOneField(Repair, on_delete=models.CASCADE, related_name="finance")
    amount_charged = models.DecimalField(max_digits=15, decimal_places=2)
    
    # puede ser nulo porque quiza se entrega el equipo y el cliente paga unos dias despues
    payment_date = models.DateField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Finance for Repair #{self.repair.id} - ${self.amount_charged}"

#categorias de gastos (electricidad, insumos, cuota monotributo, etc)
class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

#los egresos (los gastos del dia a dia)
class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name="expenses")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    expense_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.category.name} - ${self.amount} on {self.expense_date}"