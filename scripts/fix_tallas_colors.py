import os
import sys
import django

sys.path.append(r"c:\Users\LENOVO\Desktop\Proyectos programacion\salon_unas")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salonweb.settings')
django.setup()

from inventario.models import Color, Talla

# 1. Update Talla ordering
tallas = Talla.objects.all()

orden_map = {
    'xs': 10,
    's': 20,
    'm': 30,
    'l': 40,
    'xl': 50,
    'xxl': 60,
    'unica': 100,
    'única': 100
}

for talla in tallas:
    name_lower = talla.nombre.lower().strip()
    talla.orden = orden_map.get(name_lower, 99)
    talla.save()
    print(f"Set orden {talla.orden} for Talla '{talla.nombre}' (id: {talla.id})")

# 2. Update Cafe Color
try:
    cafe = Color.objects.get(nombre__contains='Caf')
    cafe.codigo_hex = '#6F4E37' # Coffee brown
    cafe.save()
    print("Updated Color 'Café' to #6F4E37")
except Color.DoesNotExist:
    pass
except Color.MultipleObjectsReturned:
    for c in Color.objects.filter(nombre__contains='Caf'):
        c.codigo_hex = '#6F4E37'
        c.save()
    print("Updated multiple 'Café' colors to #6F4E37")
