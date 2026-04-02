# Guía de Imágenes Estáticas para Servicios

## Estructura de Carpetas

```
static/images/servicios/
├── manicure/           # Servicios de manicure
├── pedicure/           # Servicios de pedicure  
└── tratamientos/       # Tratamientos especiales
```

## Convenciones de Nombres

### Para Servicios de Manicure:
- `manicure-clasica.jpg`
- `manicure-francesa.jpg`
- `manicure-gel.jpg`
- `nail-art.jpg`

### Para Servicios de Pedicure:
- `pedicure-spa.jpg`
- `pedicure-clasica.jpg`
- `pedicure-gel.jpg`

### Para Tratamientos:
- `tratamiento-parafina.jpg`
- `masaje-manos.jpg`
- `cuidado-cuticulas.jpg`

## Uso en Templates

```html
{% load static %}

<!-- Imagen de servicio -->
<img src="{% static 'images/servicios/manicure/manicure-gel.jpg' %}" 
     alt="Manicure en Gel" 
     class="img-fluid">

<!-- Con Bootstrap card -->
<div class="card">
    <img src="{% static 'images/servicios/pedicure/pedicure-spa.jpg' %}" 
         class="card-img-top" 
         alt="Pedicure Spa">
    <div class="card-body">
        <h5 class="card-title">Pedicure Spa</h5>
        <p class="card-text">Relajante tratamiento completo...</p>
    </div>
</div>
```

## Formatos Recomendados
- **JPG**: Para fotografías de servicios
- **PNG**: Para logos o imágenes con transparencia
- **WebP**: Para mejor compresión (navegadores modernos)

## Tamaños Recomendados
- **Cards de servicios**: 400x300px
- **Hero images**: 1200x600px  
- **Thumbnails**: 150x150px
