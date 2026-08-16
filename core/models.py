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

class ArticuloBlog(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True, null=True)
    resumen = models.CharField(max_length=300, help_text="Aparece en la lista y en la meta descripción")
    contenido = models.TextField(help_text="Contenido del artículo. Los saltos de línea generan párrafos.")
    imagen = models.ImageField(upload_to='blog/', blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, help_text="Desmarcar para ocultar el artículo")

    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = "Artículo de Blog"
        verbose_name_plural = "Artículos de Blog"

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.titulo)
            slug = base_slug
            counter = 1
            while ArticuloBlog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
