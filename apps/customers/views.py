from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Customer
from django.db.models import Q


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    
    # Filtro por búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(dni__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    context = {
        'customers': customers,
        'search_query': search_query,
    }
    return render(request, 'customers/customer_list.html', context)


@login_required
def customer_create(request):
    if request.method == 'POST':
        try:
            Customer.objects.create(
                name=request.POST.get('name'),
                last_name=request.POST.get('last_name'),
                dni=request.POST.get('dni'),
                phone_number=request.POST.get('phone_number'),
                email=request.POST.get('email'),
                notes=request.POST.get('notes', '')
            )
            return redirect('customer_list')
        except Exception as e:
            from django.db import IntegrityError
            if isinstance(e, IntegrityError):
                context = {
                    'error': f'Ya existe un cliente con ese dato único: {str(e)}'
                }
                return render(request, 'customers/customer_create.html', context)
            raise
    
    return render(request, 'customers/customer_create.html')


@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    devices = customer.devices.prefetch_related('repairs').all()
    
    # Obtener todas las reparaciones de este cliente (a través de sus dispositivos)
    from apps.repairs.models import Repair
    repairs = Repair.objects.filter(
        device__customer=customer
    ).select_related('device', 'problem_category').order_by('-created_at')
    
    context = {
        'customer': customer,
        'devices': devices,
        'repairs': repairs,
    }
    return render(request, 'customers/customer_detail.html', context)


@login_required
def create_customer_ajax(request):
    """Vista AJAX para crear un cliente desde el formulario de reparación"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    
    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    dni = request.POST.get('dni')
    phone_number = request.POST.get('phone_number', '')
    email = request.POST.get('email', '')
    
    if not name or not last_name or not dni:
        return JsonResponse({'success': False, 'error': 'Nombre, apellido y DNI son obligatorios'})
    
    try:
        customer = Customer.objects.create(
            name=name,
            last_name=last_name,
            dni=dni,
            phone_number=phone_number,
            email=email
        )
        return JsonResponse({
            'success': True,
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'last_name': customer.last_name
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
