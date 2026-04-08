from django.db import models

class Banner(models.Model):
    imagen = models.ImageField(upload_to='banners/', help_text="Imagen recomendada: 1920x800px")
    titulo = models.CharField(max_length=200, blank=True, null=True)
    subtitulo = models.CharField(max_length=300, blank=True, null=True)
    texto_boton = models.CharField(max_length=50, default="VER COLECCIÓN")
    enlace_boton = models.CharField(max_length=500, default="#tienda")
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        verbose_name = "Banner Principal"
        verbose_name_plural = "Banners Principales"

    def __str__(self):
        return self.titulo or f"Banner {self.id}"

class ResenaComunidad(models.Model):
    imagen = models.ImageField(upload_to='comunidad/', help_text="Foto de la clienta (preferiblemente cuadrada)")
    nombre_cliente = models.CharField(max_length=100, help_text="Ej: @maria_perez o María P.")
    comentario = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']
        verbose_name = "Reseña de Comunidad"
        verbose_name_plural = "Reseñas de Comunidad"

    def __str__(self):
        return f"Reseña de {self.nombre_cliente}"
