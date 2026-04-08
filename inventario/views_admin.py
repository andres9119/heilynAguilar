from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q
from .models import Producto, Variacion, MovimientoStock, Talla, Color, Venta
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate, TruncMonth

@staff_member_required
def dashboard_home(request):
    # KPIs Básicos
    total_productos = Producto.objects.count()
    total_stock = Variacion.objects.aggregate(total=Sum('stock'))['total'] or 0
    stock_bajo = Variacion.objects.filter(stock__lt=3).select_related('producto', 'talla', 'color')
    cantidad_stock_bajo = stock_bajo.count()
    
    # --- Cálculos Financieros ---
    # Rango de tiempo (Default: Mes actual)
    ahora = timezone.now()
    primer_dia_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # 1. Recogido (Ventas totales)
    ventas_mes = Venta.objects.filter(fecha__gte=primer_dia_mes)
    total_recogido = 0
    total_costo_vendido = 0
    for v in ventas_mes:
        total_recogido += v.total_venta
        total_costo_vendido += v.total_costo
    
    # 2. Gastado / Inversión (Ingresos de stock)
    ingresos_mes = MovimientoStock.objects.filter(tipo='INGRESO', fecha__gte=primer_dia_mes)
    total_gastado = sum(mov.cantidad * mov.precio_costo_unitario for mov in ingresos_mes)
    
    # 3. Pérdidas (Egresos manuales - no ventas)
    egresos_manuales = MovimientoStock.objects.filter(tipo='EGRESO', fecha__gte=primer_dia_mes).exclude(motivo__icontains='Venta')
    total_perdidas = sum(mov.cantidad * mov.precio_costo_unitario for mov in egresos_manuales)
    
    # 4. Ganancia Neta Estimada (Sobre lo vendido)
    ganancia_neta = total_recogido - total_costo_vendido - total_perdidas

    # Datos para gráfico: Ganancias por día (últimos 15 días)
    hace_15_dias = ahora - timedelta(days=15)
    ventas_diarias = Venta.objects.filter(fecha__gte=hace_15_dias)\
        .annotate(dia=TruncDate('fecha'))\
        .values('dia')\
        .annotate(total=Sum(models.F('cantidad') * models.F('precio_venta')))\
        .order_by('dia')

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
        'total_recogido': total_recogido,
        'total_gastado': total_gastado,
        'total_perdidas': total_perdidas,
        'ganancia_neta': ganancia_neta,
        'stock_por_categoria': stock_por_categoria,
        'ultimos_movimientos': ultimos_movimientos,
        'ventas_diarias': ventas_diarias,
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
        precio_costo = request.POST.get('precio_costo')
        
        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser mayor a cero.")
            return redirect('inventory_manager')

        # Si no se provee costo, usar el predeterminado del producto
        if not precio_costo:
            precio_costo = variacion.producto.precio_costo
        else:
            precio_costo = float(precio_costo)

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
            precio_costo_unitario=precio_costo,
            motivo=motivo,
            usuario=request.user
        )
        
        messages.success(request, f"Stock actualizado con éxito para {variacion.producto.nombre}.")
        
    return redirect('inventory_manager')

@staff_member_required
def movements_log(request):
    movimientos = MovimientoStock.objects.all().select_related('variacion__producto', 'variacion__talla', 'variacion__color', 'usuario')
    
    context = {
        'movimientos': movimientos,
        'segment': 'movimientos'
    }
    return render(request, 'inventario/movements_log.html', context)

@staff_member_required
def registrar_venta(request):
    if request.method == 'POST':
        pk = request.POST.get('variacion_id')
        cantidad = int(request.POST.get('cantidad', 1))
        precio_venta = request.POST.get('precio_venta')
        
        variacion = get_object_or_404(Variacion, pk=pk)
        
        if variacion.stock < cantidad:
            messages.error(request, f"No hay suficiente stock. Disponible: {variacion.stock}")
            return redirect('inventory_manager')
        
        # Si no se pasó precio personalizado, usar el del producto
        if not precio_venta:
            precio_venta = variacion.producto.precio
        
        # 1. Crear registro de Venta
        Venta.objects.create(
            variacion=variacion,
            cantidad=cantidad,
            precio_venta=precio_venta,
            precio_costo=variacion.producto.precio_costo,
            usuario=request.user
        )
        
        # 2. Descontar Stock
        variacion.stock -= cantidad
        variacion.save()
        
        # 3. Registrar Movimiento de Salida
        MovimientoStock.objects.create(
            variacion=variacion,
            tipo='EGRESO',
            cantidad=cantidad,
            precio_costo_unitario=variacion.producto.precio_costo,
            motivo=f"Venta registrada #V{timezone.now().strftime('%Y%m%d%H%M')}",
            usuario=request.user
        )
        
        messages.success(request, f"Venta de {variacion.producto.nombre} registrada correctamente.")
        
    return redirect('inventory_manager')
