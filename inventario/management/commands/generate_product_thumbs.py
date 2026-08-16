import os
from io import BytesIO

from django.core.management.base import BaseCommand
from PIL import Image

from inventario.models import Producto


class Command(BaseCommand):
    help = "Genera miniaturas responsivas (_360.webp) para los productos existentes que no la tienen."

    def handle(self, *args, **options):
        procesados = 0
        for p in Producto.objects.all():
            if not p.imagen:
                continue
            p.save()
            if p.imagen_thumb:
                procesados += 1
                self.stdout.write(self.style.SUCCESS(f"  OK {p.slug or p.nombre} -> {os.path.basename(p.imagen_thumb.name)}"))
            else:
                self.stdout.write(self.style.WARNING(f"  Sin thumb: {p.slug or p.nombre}"))
        self.stdout.write(self.style.SUCCESS(f"\n{procesados} productos con miniatura generada."))