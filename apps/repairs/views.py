from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Repair, ProblemCategory
from apps.devices.models import Device, DeviceType, Brand
from apps.customers.models import Customer
from apps.users.models import User
from apps.finances.models import RepairFinance, BillingPeriod
from django.db.models import Q, Sum, Count


@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Calcular facturación total
    try:
        total_income = RepairFinance.objects.aggregate(
            total=Sum('amount_charged')
        )['total'] or 0
    except:
        total_income = 0
    
    # Contar equipos pendientes (no finalizados ni entregados)
    try:
        pending_repairs = Repair.objects.exclude(
            status__in=[Repair.Status.COMPLETED, Repair.Status.DELIVERED, Repair.Status.CANCELLED]
        ).count()
    except:
        pending_repairs = 0
    
    # Contar equipos finalizados (completados o entregados)
    try:
        completed_repairs = Repair.objects.filter(
            status__in=[Repair.Status.COMPLETED, Repair.Status.DELIVERED]
        ).count()
    except:
        completed_repairs = 0
    
    # Calcular porcentaje del límite de monotributo
    try:
        latest_billing = BillingPeriod.objects.first()
        billing_percentage = 0
        if latest_billing and latest_billing.billing_limit > 0:
            billing_percentage = (total_income / latest_billing.billing_limit) * 100
    except:
        latest_billing = None
        billing_percentage = 0
    
    # Obtener últimas reparaciones
    try:
        recent_repairs = Repair.objects.select_related(
            'device__customer',
            'device__brand',
            'problem_category'
        ).order_by('-created_at')[:5]
    except:
        recent_repairs = []
    
    context = {
        'total_income': total_income,
        'pending_repairs': pending_repairs,
        'completed_repairs': completed_repairs,
        'billing_percentage': billing_percentage,
        'latest_billing': latest_billing,
        'recent_repairs': recent_repairs,
    }
    return render(request, 'dashboard.html', context)


@login_required
def repair_list(request):
    repairs = Repair.objects.select_related('device__customer', 'problem_category').order_by('-created_at')
    
    # Filtro por búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        repairs = repairs.filter(
            Q(device__customer__name__icontains=search_query) |
            Q(device__customer__last_name__icontains=search_query) |
            Q(device__brand__name__icontains=search_query) |
            Q(device__model__icontains=search_query) |
            Q(reported_problem__icontains=search_query)
        )
    
    # Filtro por estado
    status_filter = request.GET.get('status', '')
    if status_filter:
        repairs = repairs.filter(status=status_filter)
    
    context = {
        'repairs': repairs,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Repair.Status.choices,
    }
    return render(request, 'repairs/repairs_list.html', context)


@login_required
def repair_create(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Obtener datos del formulario
                customer_id = request.POST.get('customer_id')
                customer_name = request.POST.get('customer_name', '').strip()
                
                device_type_name = request.POST.get('device_type', '').strip()
                brand_name = request.POST.get('brand', '').strip()
                device_model = request.POST.get('device_model', '').strip()
                device_serial = request.POST.get('device_serial', '').strip()
                reception_notes = request.POST.get('reception_notes', '').strip()
                
                problem_category_name = request.POST.get('problem_category', '').strip()
                reported_problem = request.POST.get('reported_problem', '').strip()
                status = request.POST.get('status', Repair.Status.RECEIVED)
                
                # Validaciones
                if not customer_name:
                    raise ValueError('Debe ingresar un cliente')
                
                if not device_type_name or not brand_name:
                    raise ValueError('Debe especificar el tipo de equipo y la marca')
                
                if not problem_category_name:
                    raise ValueError('Debe especificar la categoría del problema')
                
                if not reported_problem:
                    raise ValueError('Debe describir el problema reportado')
                
                # Obtener o crear el cliente
                if customer_id:
                    customer = Customer.objects.get(id=customer_id)
                else:
                    # Buscar cliente por nombre completo
                    parts = customer_name.split()
                    if len(parts) >= 2:
                        name = ' '.join(parts[:-1])
                        last_name = parts[-1]
                    else:
                        name = customer_name
                        last_name = ''
                    
                    # Buscar si existe cliente con ese nombre
                    customer = Customer.objects.filter(
                        name__icontains=name,
                        last_name__icontains=last_name
                    ).first()
                    
                    if not customer:
                        raise ValueError('Cliente no encontrado. Debe seleccionar un cliente existente o crear uno nuevo usando el botón "Nuevo Cliente"')
                
                # Crear o obtener DeviceType (se puede reutilizar)
                device_type, _ = DeviceType.objects.get_or_create(
                    name=device_type_name
                )
                
                # Crear o obtener Brand (se puede reutilizar)
                brand, _ = Brand.objects.get_or_create(
                    name=brand_name
                )
                
                # SIEMPRE crear un Device nuevo para este cliente (no reutilizar)
                device = Device.objects.create(
                    customer=customer,
                    device_type=device_type,
                    brand=brand,
                    model=device_model or None,
                    serial_number=device_serial or None,
                    reception_notes=reception_notes or None
                )
                
                # Crear o obtener ProblemCategory (se puede reutilizar)
                problem_category, _ = ProblemCategory.objects.get_or_create(
                    name=problem_category_name
                )
                
                # Crear la reparación
                repair = Repair.objects.create(
                    device=device,
                    technician=request.user,
                    problem_category=problem_category,
                    reported_problem=reported_problem,
                    status=status
                )
                
                return redirect('repair_list')
                
        except ValueError as e:
            error = str(e)
        except Customer.DoesNotExist:
            error = 'Cliente no encontrado. Debe seleccionar un cliente existente o crear uno nuevo usando el botón "Nuevo Cliente"'
        except Exception as e:
            error = f'Error al crear la reparación: {str(e)}'
        
        # Si hay error, volver a mostrar el formulario con el mensaje de error
        customers = Customer.objects.all()
        problem_categories = ProblemCategory.objects.all()
        device_types = DeviceType.objects.all()
        brands = Brand.objects.all()
        
        context = {
            'customers': customers,
            'problem_categories': problem_categories,
            'device_types': device_types,
            'brands': brands,
            'status_choices': Repair.Status.choices,
            'error': error
        }
        return render(request, 'repairs/repair_create.html', context)
    
    # GET request
    customers = Customer.objects.all()
    problem_categories = ProblemCategory.objects.all()
    device_types = DeviceType.objects.all()
    brands = Brand.objects.all()
    
    context = {
        'customers': customers,
        'problem_categories': problem_categories,
        'device_types': device_types,
        'brands': brands,
        'status_choices': Repair.Status.choices,
    }
    return render(request, 'repairs/repair_create.html', context)


@login_required
def repair_detail(request, repair_id):
    repair = get_object_or_404(Repair, id=repair_id)
    repair_finance = getattr(repair, 'finance', None)
    
    # Buscar reparaciones similares para sugerencias
    similar_repairs = Repair.objects.filter(
        problem_category=repair.problem_category,
        status=Repair.Status.COMPLETED
    ).exclude(id=repair.id)[:5]
    
    context = {
        'repair': repair,
        'repair_finance': repair_finance,
        'similar_repairs': similar_repairs,
        'status_choices': Repair.Status.choices,
    }
    return render(request, 'repairs/repair_detail.html', context)


@login_required
def repair_update(request, repair_id):
    repair = get_object_or_404(Repair, id=repair_id)
    
    if request.method == 'POST':
        repair.diagnosis = request.POST.get('diagnosis', '')
        repair.proposed_solution = request.POST.get('proposed_solution', '')
        repair.performed_procedure = request.POST.get('performed_procedure', '')
        repair.save()
        
        return redirect('repair_detail', repair_id=repair.id)
    
    context = {
        'repair': repair,
    }
    return render(request, 'repairs/repair_update.html', context)


@login_required
def repair_update_status(request, repair_id):
    repair = get_object_or_404(Repair, id=repair_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        repair.status = new_status
        
        # Si se marca como entregado, establecer fecha de entrega
        if new_status == Repair.Status.DELIVERED:
            from django.utils import timezone
            repair.delivery_date = timezone.now()
        
        repair.save()
        
        # Crear registro en historial
        from .models import RepairHistory
        RepairHistory.objects.create(
            repair=repair,
            previous_status=request.POST.get('previous_status'),
            new_status=new_status,
            changed_by=request.user
        )
        
        return redirect('repair_detail', repair_id=repair.id)
    
    context = {
        'repair': repair,
        'status_choices': Repair.Status.choices,
    }
    return render(request, 'repairs/repair_update_status.html', context)


@login_required
def get_suggestions(request):
    """API para obtener sugerencias de problemas similares"""
    query = request.GET.get('q', '')
    device_type = request.GET.get('device_type', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'same_device_type': [], 'other_device_types': []})
    
    # Base query para buscar reparaciones
    base_query = Repair.objects.filter(
        Q(problem_category__name__icontains=query) |
        Q(reported_problem__icontains=query) |
        Q(diagnosis__icontains=query)
    ).select_related(
        'device__customer',
        'device__device_type',
        'device__brand',
        'problem_category'
    ).exclude(
        status=Repair.Status.CANCELLED
    ).order_by('-created_at')
    
    same_device_type_repairs = []
    other_device_types_repairs = []
    
    # Si se especificó un tipo de equipo, buscar primero coincidencias del mismo tipo
    if device_type:
        same_type = base_query.filter(
            device__device_type__name__icontains=device_type
        )[:5]
        
        for repair in same_type:
            same_device_type_repairs.append({
                'repair_id': repair.id,
                'problem_category': repair.problem_category.name if repair.problem_category else repair.reported_problem[:50],
                'reported_problem': repair.reported_problem[:100] if repair.reported_problem else '',
                'device_type': repair.device.device_type.name if repair.device.device_type else 'N/A',
                'brand': repair.device.brand.name if repair.device.brand else '',
                'model': repair.device.model if repair.device.model else '',
                'customer': f"{repair.device.customer.name} {repair.device.customer.last_name}" if repair.device.customer else '',
                'status': repair.get_status_display(),
                'diagnosis': repair.diagnosis[:100] if repair.diagnosis else '',
                'performed_procedure': repair.performed_procedure[:100] if repair.performed_procedure else '',
                'created_at': repair.created_at.strftime('%d/%m/%Y') if repair.created_at else '',
            })
        
        # Si hay menos de 5 del mismo tipo, buscar otros tipos
        if len(same_device_type_repairs) < 5:
            other_types = base_query.exclude(
                device__device_type__name__icontains=device_type
            )[:5]
            
            for repair in other_types:
                other_device_types_repairs.append({
                    'repair_id': repair.id,
                    'problem_category': repair.problem_category.name if repair.problem_category else repair.reported_problem[:50],
                    'reported_problem': repair.reported_problem[:100] if repair.reported_problem else '',
                    'device_type': repair.device.device_type.name if repair.device.device_type else 'N/A',
                    'brand': repair.device.brand.name if repair.device.brand else '',
                    'model': repair.device.model if repair.device.model else '',
                    'customer': f"{repair.device.customer.name} {repair.device.customer.last_name}" if repair.device.customer else '',
                    'status': repair.get_status_display(),
                    'diagnosis': repair.diagnosis[:100] if repair.diagnosis else '',
                    'performed_procedure': repair.performed_procedure[:100] if repair.performed_procedure else '',
                    'created_at': repair.created_at.strftime('%d/%m/%Y') if repair.created_at else '',
                })
    else:
        # Si no se especificó tipo de equipo, mostrar todas las reparaciones
        all_repairs = base_query[:10]
        
        for repair in all_repairs:
            same_device_type_repairs.append({
                'repair_id': repair.id,
                'problem_category': repair.problem_category.name if repair.problem_category else repair.reported_problem[:50],
                'reported_problem': repair.reported_problem[:100] if repair.reported_problem else '',
                'device_type': repair.device.device_type.name if repair.device.device_type else 'N/A',
                'brand': repair.device.brand.name if repair.device.brand else '',
                'model': repair.device.model if repair.device.model else '',
                'customer': f"{repair.device.customer.name} {repair.device.customer.last_name}" if repair.device.customer else '',
                'status': repair.get_status_display(),
                'diagnosis': repair.diagnosis[:100] if repair.diagnosis else '',
                'performed_procedure': repair.performed_procedure[:100] if repair.performed_procedure else '',
                'created_at': repair.created_at.strftime('%d/%m/%Y') if repair.created_at else '',
            })
    
    return JsonResponse({
        'same_device_type': same_device_type_repairs,
        'other_device_types': other_device_types_repairs,
        'device_type_filter': device_type
    })


@login_required
def profile(request):
    context = {
        'user': request.user,
    }
    return render(request, 'profile.html', context)


@login_required
def get_customer_devices(request):
    """API para obtener equipos de un cliente específico"""
    customer_id = request.GET.get('customer_id')
    if not customer_id:
        return JsonResponse({'devices': []})
    
    try:
        devices = Device.objects.filter(customer_id=customer_id).select_related(
            'device_type', 'brand'
        )
        devices_data = [
            {
                'id': device.id,
                'name': f"{device.device_type.name} - {device.brand.name} {device.model}"
            }
            for device in devices
        ]
        return JsonResponse({'devices': devices_data})
    except Exception as e:
        return JsonResponse({'devices': []})


@login_required
def repair_payment(request, repair_id):
    repair = get_object_or_404(Repair, id=repair_id)
    
    if request.method == 'POST':
        amount_charged = request.POST.get('amount_charged')
        payment_date = request.POST.get('payment_date')
        is_paid = request.POST.get('is_paid') == 'on'
        
        # Crear o actualizar RepairFinance
        repair_finance, created = RepairFinance.objects.update_or_create(
            repair=repair,
            defaults={
                'amount_charged': amount_charged,
                'payment_date': payment_date if payment_date else None,
                'is_paid': is_paid
            }
        )
        
        return redirect('repair_detail', repair_id=repair.id)
    
    repair_finance = getattr(repair, 'finance', None)
    
    context = {
        'repair': repair,
        'repair_finance': repair_finance,
    }
    return render(request, 'repairs/repair_payment.html', context)
