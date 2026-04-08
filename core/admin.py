from django.contrib import admin
from .models import Banner, ResenaComunidad

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'orden', 'activo')
    list_editable = ('orden', 'activo')
    list_filter = ('activo',)

@admin.register(ResenaComunidad)
class ResenaComunidadAdmin(admin.ModelAdmin):
    list_display = ('nombre_cliente', 'orden', 'activo')
    list_editable = ('orden', 'activo')
    list_filter = ('activo',)
