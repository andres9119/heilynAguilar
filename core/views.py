from django.shortcuts import render, get_object_or_404
from inventario.models import Producto, Talla, Color
from .models import Banner, ResenaComunidad

def inicio(request):
    productos = Producto.objects.filter(activo=True).distinct()
    
    # Filtros
    q = request.GET.get('q')
    talla_id = request.GET.get('talla')
    categoria = request.GET.get('categoria')
    precio_max = request.GET.get('precio_max')
    
    if q:
        productos = productos.filter(nombre__icontains=q)
    if talla_id:
        productos = productos.filter(variaciones__talla__id=talla_id)
    if categoria:
        productos = productos.filter(categoria=categoria)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
        
    # Obtener valores para los filtros del UI
    categorias = Producto.objects.filter(activo=True).values_list('categoria', flat=True).distinct()
    tallas_list = Talla.objects.all()
    
    # Banners y Testimonios
    banners = Banner.objects.filter(activo=True)
    testimonios = ResenaComunidad.objects.filter(activo=True)
    
    return render(request, 'core/inicio.html', {
        'productos': productos,
        'categorias': categorias,
        'tallas_list': tallas_list,
        'banners': banners,
        'testimonios': testimonios
    })

def detalle_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug, activo=True)
    return render(request, 'core/detalle_producto.html', {'producto': producto})

def contacto(request):
    return render(request, 'core/contacto.html')

def politicas(request):
    return render(request, 'core/politicas.html')

def terminos(request):
    return render(request, 'core/terminos.html')

def faq(request):
    return render(request, 'core/faq.html')

def devoluciones(request):
    return render(request, 'core/devoluciones.html')

def nosotros(request):
    return render(request, 'core/nosotros.html')

def beneficios(request):
    return render(request, 'core/beneficios.html')

def tallas(request):
    return render(request, 'core/tallas.html')
