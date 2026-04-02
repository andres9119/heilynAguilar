from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required, user_passes_test
import json

def is_superuser(user):
    return user.is_superuser

# Listar productos
@user_passes_test(is_superuser)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, "inventario/lista_productos.html", {"productos": productos})

# Crear producto
@user_passes_test(is_superuser)
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm()
    return render(request, "inventario/form_producto.html", {"form": form, "accion": "Crear"})

# Editar producto
@user_passes_test(is_superuser)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm(instance=producto)
    return render(request, "inventario/form_producto.html", {"form": form, "accion": "Editar"})

# Eliminar producto
@user_passes_test(is_superuser)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        producto.delete()
        return redirect("lista_productos")
    return render(request, "inventario/eliminar_producto.html", {"producto": producto})

# Actualizar cantidad (AJAX) - DESHABILITADO TEMPORALMENTE por cambio a Variaciones
@user_passes_test(is_superuser)
@require_POST
@csrf_exempt
def actualizar_cantidad(request, pk):
    return JsonResponse({'success': False, 'error': 'Funcionalidad en reestructuración por cambio a variaciones.'})
