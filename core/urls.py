from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('contacto/', views.contacto, name='contacto'),
    path('politicas-de-privacidad/', views.politicas, name='politicas'),
    path('terminos-y-condiciones/', views.terminos, name='terminos'),
    path('preguntas-frecuentes/', views.faq, name='faq'),
    path('politica-de-devoluciones/', views.devoluciones, name='devoluciones'),
    path('quienes-somos/', views.nosotros, name='nosotros'),
    path('beneficios/', views.beneficios, name='beneficios'),
    path('guia-de-tallas/', views.tallas, name='tallas'),
]
