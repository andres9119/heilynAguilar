from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from .models import Producto, Variacion, MovimientoStock, Talla, Color
from django.contrib import messages
from django.utils import timezone

@staff_member_required
def dashboard_home(request):
    # KPIs
    total_productos = Producto.objects.count()
    total_variaciones = Variacion.objects.count()
    total_stock = Variacion.objects.aggregate(total=Sum('stock'))['total'] or 0
    
    # Alertas de stock bajo (ej: < 3 unidades)
    stock_bajo = Variacion.objects.filter(stock__lt=3).select_related('producto', 'talla', 'color')
    cantidad_stock_bajo = stock_bajo.count()
    
    # Datos para gráfico: Stock por categoría
    categorias = Producto.CATEGORIAS
    stock_por_categoria = []
    for cat_slug, cat_name in categorias:
        total = Variacion.objects.filter(producto__categoria=cat_slug).aggregate(total=Sum('stock'))['total'] or 0
        stock_por_categoria.append({'nombre': cat_name, 'total': total})

    # Últimos movimientos
    ultimos_movimientos = MovimientoStock.objects.all().select_related('variacion__producto', 'usuario')[:10]

    context = {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'cantidad_stock_bajo': cantidad_stock_bajo,
        'stock_bajo': stock_bajo,
        'stock_por_categoria': stock_por_categoria,
        'ultimos_movimientos': ultimos_movimientos,
        'segment': 'dashboard'
    }
    return render(request, 'inventario/dashboard_home.html', context)

@staff_member_required
def inventory_manager(request):
    query = request.GET.get('q', '')
    categoria = request.GET.get('categoria', '')
    
    variaciones = Variacion.objects.select_related('producto', 'talla', 'color').all()
    
    if query:
        variaciones = variaciones.filter(
            Q(producto__nombre__icontains=query) | 
            Q(producto__descripcion__icontains=query)
        )
    
    if categoria:
        variaciones = variaciones.filter(producto__categoria=categoria)

    context = {
        'variaciones': variaciones,
        'categorias': Producto.CATEGORIAS,
        'query': query,
        'categoria_filtro': categoria,
        'segment': 'inventario'
    }
    return render(request, 'inventario/inventory_manager.html', context)

@staff_member_required
def ajust_stock(request, pk):
    if request.method == 'POST':
        variacion = get_object_or_404(Variacion, pk=pk)
        tipo = request.POST.get('tipo') # INGRESO o EGRESO
        cantidad = int(request.POST.get('cantidad', 0))
        motivo = request.POST.get('motivo', 'Ajuste manual')
        
        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser mayor a cero.")
            return redirect('inventory_manager')

        if tipo == 'INGRESO':
            variacion.stock += cantidad
        elif tipo == 'EGRESO':
            if variacion.stock < cantidad:
                messages.error(request, f"No hay suficiente stock para retirar {cantidad} unidades.")
                return redirect('inventory_manager')
            variacion.stock -= cantidad
        
        variacion.save()
        
        # Registrar movimiento
        MovimientoStock.objects.create(
            variacion=variacion,
            tipo=tipo,
            cantidad=cantidad,
            motivo=motivo,
            usuario=request.user
        )
        
        id_producto = f" #{variacion.producto.id}"
        messages.success(request, f"Stock actualizado con éxito para {variacion.producto.nombre} ({variacion.talla} - {variacion.color}).")
        
    return redirect('inventory_manager')

@staff_member_required
def movements_log(request):
    movimientos = MovimientoStock.objects.all().select_related('variacion__producto', 'variacion__talla', 'variacion__color', 'usuario')
    
    context = {
        'movimientos': movimientos,
        'segment': 'movimientos'
    }
    return render(request, 'inventario/movements_log.html', context)
