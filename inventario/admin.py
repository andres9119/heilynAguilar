from django.contrib import admin
from .models import Producto, ImagenProducto, Talla, Color, Variacion

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 2

class VariacionInline(admin.TabularInline):
    model = Variacion
    extra = 3

from django.utils.safestring import mark_safe

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('miniatura', 'nombre', 'categoria', 'precio', 'activo', 'stock_total')
    search_fields = ('nombre', 'categoria')
    list_filter = ('activo', 'categoria')
    fields = ('nombre', 'descripcion', 'categoria', 'precio', 'imagen', 'activo')
    readonly_fields = ('miniatura_detalle',)
    inlines = [ImagenProductoInline, VariacionInline]

    def miniatura(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="50" height="auto" style="border-radius: 4px;" />')
        return "Sin imagen"
    miniatura.short_description = "Vista previa"

    def miniatura_detalle(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="200" height="auto" style="border-radius: 8px;" />')
        return "Sin imagen"
    miniatura_detalle.short_description = "Imagen actual"

@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

from django import forms
from django.forms.widgets import TextInput

class ColorWidget(TextInput):
    input_type = 'color'

class ColorAdminForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'codigo_hex': ColorWidget()
        }

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    form = ColorAdminForm
    list_display = ('nombre', 'color_preview', 'codigo_hex')
    
    def color_preview(self, obj):
        return mark_safe(f'<div style="width: 25px; height: 25px; background-color: {obj.codigo_hex}; border-radius: 50%; border: 1px solid #bbb;"></div>')
    color_preview.short_description = 'Muestra'
