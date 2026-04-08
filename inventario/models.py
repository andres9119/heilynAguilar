from django.db import models
from django.core.files.base import ContentFile
from django.utils.text import slugify
import os
from PIL import Image
from io import BytesIO

class Talla(models.Model):
    nombre = models.CharField(max_length=20)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.nombre

class Color(models.Model):
    nombre = models.CharField(max_length=50)
    codigo_hex = models.CharField(max_length=7, blank=True, null=True, help_text="Ej: #FF0000")

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    CATEGORIAS = [
        ('Bodys', 'Bodys'),
        ('Corset', 'Corset'),
        ('Top', 'Top'),
        ('Shorts', 'Shorts'),
        ('Faldas', 'Faldas'),
        ('Denim', 'Denim'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, help_text="Imagen principal")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if self.imagen:
            # Si ya es webp, no volver a procesar para evitar bucles o trabajo extra
            if not self.imagen.name.lower().endswith('.webp'):
                img = Image.open(self.imagen)
                
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                
                # Redimensionar solo si excede el ancho deseado
                if img.width > 800:
                    output_size = (800, int((800 * img.height) / img.width))
                    img.thumbnail(output_size, Image.LANCZOS)
                
                output = BytesIO()
                img.save(output, format='WebP', quality=85)
                output.seek(0)
                
                name = os.path.splitext(self.imagen.name)[0] + ".webp"
                self.imagen.save(name, ContentFile(output.read()), save=False)
            
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            counter = 1
            while Producto.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def stock_total(self):
        return sum(v.stock for v in self.variaciones.all())

class Variacion(models.Model):
    producto = models.ForeignKey(Producto, related_name='variaciones', on_delete=models.CASCADE)
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Variación"
        verbose_name_plural = "Variaciones"

    def __str__(self):
        return f"{self.producto.nombre} - {self.talla} - {self.color}"

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/galeria/')
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']
        verbose_name = "Imagen de Galería"
        verbose_name_plural = "Imágenes de Galería"
    def save(self, *args, **kwargs):
        if self.imagen and not self.imagen.name.lower().endswith('.webp'):
            img = Image.open(self.imagen)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            if img.width > 800:
                output_size = (800, int((800 * img.height) / img.width))
                img.thumbnail(output_size, Image.LANCZOS)
                
            output = BytesIO()
            img.save(output, format='WebP', quality=85)
            output.seek(0)
            
            name = os.path.splitext(self.imagen.name)[0] + ".webp"
            self.imagen.save(name, ContentFile(output.read()), save=False)
            
        super().save(*args, **kwargs)

class MovimientoStock(models.Model):
    TIPO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]
    variacion = models.ForeignKey(Variacion, related_name='movimientos', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=255, help_text="Ej: Compra, Venta, Ajuste de inventario, Daño")
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Movimiento de Stock"
        verbose_name_plural = "Movimientos de Stock"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.variacion} - {self.cantidad}"
