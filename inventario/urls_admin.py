from django.urls import path
from . import views_admin

urlpatterns = [
    path('', views_admin.dashboard_home, name='dashboard_home'),
    path('inventario/', views_admin.inventory_manager, name='inventory_manager'),
    path('ajustar-stock/<int:pk>/', views_admin.ajust_stock, name='ajust_stock'),
    path('movimientos/', views_admin.movements_log, name='movements_log'),
]
