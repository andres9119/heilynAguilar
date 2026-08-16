from django.contrib import admin
from .models import Banner, ResenaComunidad, ArticuloBlog

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

@admin.register(ArticuloBlog)
class ArticuloBlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'slug', 'fecha_publicacion', 'activo')
    list_editable = ('activo',)
    list_filter = ('activo', 'fecha_publicacion')
    prepopulated_fields = {'slug': ('titulo',)}
    search_fields = ('titulo', 'resumen')
