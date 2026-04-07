from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion/', include('inventario.urls_admin')), # Administración personalizada
    path('', include('core.urls')),          # páginas públicas
    path('tienda/', include('inventario.urls')), # renamed inventario to tienda in URL
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)