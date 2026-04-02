from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from inventario.models import Producto

class StaticViewSitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return ['inicio', 'contacto']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            'inicio': 1.0,
            'contacto': 0.5,
        }
        return priorities.get(item, 0.6)

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Producto.objects.filter(activo=True)

    def lastmod(self, obj):
        return obj.fecha_ingreso

    def location(self, obj):
        return reverse('detalle_producto', args=[obj.pk])
