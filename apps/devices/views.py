from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Device
from django.db.models import Q


@login_required
def device_list(request):
    devices = Device.objects.select_related('customer', 'device_type', 'brand').all()
    
    # Filtro por búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        devices = devices.filter(
            Q(customer__name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(brand__name__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(serial_number__icontains=search_query)
        )
    
    context = {
        'devices': devices,
        'search_query': search_query,
    }
    return render(request, 'devices/device_list.html', context)


@login_required
def device_detail(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    repairs = device.repairs.select_related('problem_category').order_by('-created_at')
    
    context = {
        'device': device,
        'repairs': repairs,
    }
    return render(request, 'devices/device_detail.html', context)
