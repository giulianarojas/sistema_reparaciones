from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
import csv
from .models import RepairFinance, Expense, BillingPeriod, ExpenseCategory
from apps.repairs.models import Repair


@login_required
def finance_dashboard(request):
    # Calcular ingresos totales
    total_income = RepairFinance.objects.aggregate(
        total=Sum('amount_charged')
    )['total'] or 0
    
    # Calcular gastos totales
    total_expenses = Expense.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Calcular ganancia
    profit = total_income - total_expenses
    
    # Calcular pendiente de cobro
    pending_payment = RepairFinance.objects.filter(
        is_paid=False
    ).aggregate(total=Sum('amount_charged'))['total'] or 0
    
    # Obtener el último billing period
    latest_billing = BillingPeriod.objects.first()
    
    # Calcular porcentaje del límite de facturación
    billing_percentage = 0
    if latest_billing:
        billing_percentage = (total_income / latest_billing.billing_limit) * 100 if latest_billing.billing_limit > 0 else 0
    
    # Obtener últimas reparaciones con finanzas
    recent_repairs = RepairFinance.objects.select_related(
        'repair__device__customer',
        'repair__problem_category'
    ).order_by('-created_at')[:10]
    
    # Obtener gastos recientes
    recent_expenses = Expense.objects.select_related('category').order_by('-created_at')[:10]
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'profit': profit,
        'pending_payment': pending_payment,
        'billing_percentage': billing_percentage,
        'latest_billing': latest_billing,
        'recent_repairs': recent_repairs,
        'recent_expenses': recent_expenses,
    }
    return render(request, 'finances/finance_dashboard.html', context)


@login_required
def expense_list(request):
    expenses = Expense.objects.select_related('category').order_by('-created_at')
    
    # Filtro por fecha
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        expenses = expenses.filter(expense_date__gte=start_date)
    if end_date:
        expenses = expenses.filter(expense_date__lte=end_date)
    
    # Filtro por categoría
    category_filter = request.GET.get('category')
    if category_filter:
        expenses = expenses.filter(category_id=category_filter)
    
    categories = ExpenseCategory.objects.all()
    
    context = {
        'expenses': expenses,
        'categories': categories,
        'start_date': start_date,
        'end_date': end_date,
        'category_filter': category_filter,
    }
    return render(request, 'finances/expense_list.html', context)


@login_required
def expense_create(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        # Crear o obtener la categoría
        category, created = ExpenseCategory.objects.get_or_create(
            name=category_name
        )
        
        Expense.objects.create(
            category=category,
            amount=request.POST.get('amount'),
            description=request.POST.get('description', ''),
            expense_date=request.POST.get('expense_date')
        )
        return redirect('expense_list')
    
    categories = ExpenseCategory.objects.all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'finances/expense_create.html', context)


@login_required
def billing_period_create(request):
    if request.method == 'POST':
        BillingPeriod.objects.create(
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            billing_limit=request.POST.get('billing_limit'),
            notes=request.POST.get('notes', '')
        )
        return redirect('finance_dashboard')
    
    return render(request, 'finances/billing_period_create.html')


@login_required
def export_finances_csv(request):
    # Crear respuesta HTTP con tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_finanzas.csv"'
    
    # Crear writer CSV
    writer = csv.writer(response)
    
    # Escribir encabezados
    writer.writerow([
        'ID Reparación',
        'Fecha Cobro',
        'Monto Cobrado',
        'Estado Pago',
        'Tipo Equipo',
        'Marca',
        'Modelo',
        'Cliente',
        'Cliente Teléfono',
        'Categoría Problema',
        'Estado Reparación',
        'Fecha Creación',
        'Técnico'
    ])
    
    # Obtener todos los datos financieros con relaciones
    finances = RepairFinance.objects.select_related(
        'repair__device__customer',
        'repair__device__device_type',
        'repair__device__brand',
        'repair__problem_category',
        'repair__technician'
    ).order_by('-created_at')
    
    # Escribir filas de datos
    for finance in finances:
        repair = finance.repair
        device = repair.device
        customer = device.customer
        
        writer.writerow([
            repair.id,
            finance.payment_date.strftime('%Y-%m-%d') if finance.payment_date else '',
            finance.amount_charged,
            'Pagado' if finance.is_paid else 'Pendiente',
            device.device_type.name if device.device_type else '',
            device.brand.name if device.brand else '',
            device.model,
            f"{customer.name} {customer.last_name}",
            customer.phone_number,
            repair.problem_category.name if repair.problem_category else '',
            repair.get_status_display(),
            repair.created_at.strftime('%Y-%m-%d'),
            repair.technician.username if repair.technician else ''
        ])
    
    return response
