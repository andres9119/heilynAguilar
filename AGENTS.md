# AGENTS.md — Tienda Heilyn (Django)

Guía de referencia completa del repositorio. Léela antes de tocar cualquier código.

---

## 1. Resumen del proyecto

Tienda virtual **Heilyn Aguilar Store** — venta de ropa para dama en **Cúcuta, Colombia** (bodys, corsets, tops, faldas, denim). E-commerce tipo catálogo con **carrito por WhatsApp + Nequi** integrado, panel de administración de inventario y blog local para SEO.

- Dominio: `https://byheilynaguilar.com/`
- Keyword objetivo SEO: **"ropa para dama en Cúcuta"**
- Modelo de venta: el usuario arma el carrito en `localStorage` y paga por WhatsApp (Nequi `312 308 0861`). **No hay pasarela de pago**.
- Contacto WhatsApp ventas: `573123080861`.

---

## 2. Stack y dependencias

- **Django 5.2** (`Django>=4.2,<6.0`), Python 3.13.
- Base de datos: **SQLite** (dev) / **PostgreSQL** (prod, via `psycopg2-binary`).
- Servidor web: **Gunicorn** + **Nginx** (systemd) en VPS IONOS.
- `Pillow` (conversión WebP de imágenes), `python-dotenv` (variables de entorno).
- Firebase del frontend: Bootstrap 5.3, Font Awesome 6, Google Fonts (Inter + Playfair Display), CSS propio `mejorada.css`.

---

## 3. Estructura de carpetas

```
salonweb/               # Proyecto Django (settings, urls root, wsgi, asgi)
core/                   # Páginas públicas + blog
  models.py             # Banner, ResenaComunidad, ArticuloBlog
  views.py              # Vistas públicas (inicio, detalle, paginas, blog)
  urls.py               # Rutas públicas
  sitemaps.py           # StaticViewSitemap, ProductSitemap, BlogSitemap
  templates/core/       # Plantillas públicas
  migrations/
inventario/             # Productos, variaciones, stock, ventas, panel admin
  models.py             # Producto, Talla, Color, Variacion, ImagenProducto, MovimientoStock, Venta
  views.py              # CRUD de productos (solo superuser)
  views_admin.py        # Dashboard + inventario + movimientos (staff)
  urls.py               # rutas de inventario (/tienda/)
  urls_admin.py         # rutas del panel (/gestion/)
  forms.py              # ProductoForm
  admin.py              # Registros en Django admin
  templates/inventario/
templates/              # base.html, dashboard_base.html, robots.txt
static/
  css/                  # brand.css, estilos.css, mejorada.css (tema activo), tienda.css
  js/bolsa.js           # lógica del carrito
  img/productos/        # logos
media/                  # imágenes subidas (productos, blog, comunidad, banners)
scripts/                # utilidades de migración de datos
deploy/                 # gunicorn.service, gunicorn.socket, nginx.conf
```

---

## 4. Modelos

### App `core`
| Modelo | Campos | Uso |
|---|---|---|
| `Banner` | imagen, titulo, subtitulo, texto_boton, enlace_boton, orden, activo | Banners del home |
| `ResenaComunidad` | imagen, nombre_cliente, comentario, orden, activo | Testimonios y grid de comunidad |
| `ArticuloBlog` | titulo, slug, resumen, contenido, imagen, fecha_publicacion, activo | Entradas del blog local. Contenido plano; `\|linebreaks` renderiza párrafos |

### App `inventario`
| Modelo | Campos | Relación |
|---|---|---|
| `Talla` | nombre, orden | — |
| `Color` | nombre, codigo_hex | — |
| `Producto` | nombre, descripcion, precio, precio_costo, categoria, imagen, slug, fecha_ingreso, activo | tener `variaciones` (Variacion) |
| `Variacion` | producto, talla, color, stock | FK a Producto/Talla/Color |
| `ImagenProducto` | producto, imagen, orden | FK a Producto (galería) |
| `MovimientoStock` | variacion, tipo(INGRESO/EGRESO), cantidad, precio_costo_unitario, motivo, fecha, usuario | bitácora de stock |
| `Venta` | variacion, cantidad, precio_venta, precio_costo, fecha, usuario | registro de ventas |

Categorías de `Producto.CATEGORIAS`: Bodys, Corset, Top, Shorts, Faldas, Denim.

**Propiedades útiles:** `Producto.stock_total` (suma stock de variaciones), `Venta.total_venta`, `Venta.total_costo`, `Venta.ganancia`.

**WebP automático:** `Producto.save()` e `ImagenProducto.save()` convierten la imagen a WebP (máx 800px, calidad 85) si no lo es ya. No añadas otra conversión.

**Slug automático:** `Producto.save()` y `ArticuloBlog.save()` generan slug único desde `slugify(nombre/titulo)` si está vacío.

---

## 5. URLs — Rutas completas

Root `salonweb/urls.py`:
- `/admin/` → Django admin
- `/gestion/` → panel de inventario (`inventario/urls_admin.py`)
- `/` y páginas públicas (`core/urls.py`)
- `/tienda/` → CRUD inventario (`inventario/urls.py`)
- `/robots.txt`, `/sitemap.xml`

### `core/urls.py` (públicas)
| Ruta | Nombre | Vista |
|---|---|---|
| `/` | `inicio` | `views.inicio` |
| `/producto/<slug:slug>/` | `detalle_producto` | `views.detalle_producto` |
| `/contacto/` | `contacto` | estática |
| `/politicas-de-privacidad/` | `politicas` | estática |
| `/terminos-y-condiciones/` | `terminos` | estática |
| `/preguntas-frecuentes/` | `faq` | estática |
| `/politica-de-devoluciones/` | `devoluciones` | estática |
| `/quienes-somos/` | `nosotros` | estática |
| `/beneficios/` | `beneficios` | estática |
| `/guia-de-tallas/` | `tallas` | estática |
| `/blog/` | `blog_lista` | `views.blog_lista` |
| `/blog/<slug:slug>/` | `blog_detalle` | `views.blog_detalle` |

### `inventario/urls_admin.py` (panel `/gestion/`, requiere staff)
| Ruta | Nombre | Vista |
|---|---|---|
| `/gestion/` | `dashboard_home` | KPIs + finanzas |
| `/gestion/inventario/` | `inventory_manager` | tabla de variaciones con stock |
| `/gestion/ajustar-stock/<int:pk>/` | `ajust_stock` | ingreso/egreso de stock + movimiento |
| `/gestion/movimientos/` | `movements_log` | bitácora |
| `/gestion/registrar-venta/` | `registrar_venta` | registrar venta + descuento stock |

### `inventario/urls.py` (CRUD productos, requiere superuser)
| Ruta | Nombre |
|---|---|
| `/tienda/` | `lista_productos` |
| `/tienda/nuevo/` | `crear_producto` |
| `/tienda/editar/<int:pk>/` | `editar_producto` |
| `/tienda/eliminar/<int:pk>/` | `eliminar_producto` |
| `/tienda/actualizar-cantidad/<int:pk>/` | `actualizar_cantidad` (deshabilitado: devuelve error) |

---

## 6. Funcionalidades por vista

### `core/views.py`
- `inicio` → lista de `Producto.activo`, filtros GET (`q`, `talla`, `categoria`, `precio_max`), banners, testimonios. Filtrado vía AJAX (re-render del grid). Usa `prefetch_related('variaciones__talla','variaciones__color')`.
- `detalle_producto` → producto por slug + `prefetch_related` de variaciones e imágenes.
- `blog_lista` / `blog_detalle` → artículos activos.

### `inventario/views.py` (CRUD, guardado por `user_passes_test(is_superuser)`)
- `lista_productos`, `crear_producto`, `editar_producto`, `eliminar_producto` (POST), `actualizar_cantidad` (inactivo).

### `inventario/views_admin.py` (guard por `staff_member_required`)
- `dashboard_home` → KPIs (total productos, stock, stock bajo <3), finanzas del mes (recogido, gastado, perdidas, ganancia neta), gráfico de ventas diarias 15 días, stock por categoría, últimos 10 movimientos.
- `inventory_manager` → búsqueda por `q`/`categoria`, ajusta stock con validaciones y registra `MovimientoStock`.
- `registrar_venta` → crea `Venta`, descuenta stock, registra movimiento EGRESO "Venta registrada #V...".

---

## 7. Frontend y carrito

### Carrito (`static/js/bolsa.js`)
- Almacena el carrito en `localStorage` bajo la clave `heilyn_bag`.
- Botones `.add-to-bag` con `data-id/name/price/image/talla/color`. En tarjetas, `data-require-size="true"` fuerza seleccionar talla (`.ha-size-btn.active`) antes de agregar.
- El detalle de producto selecciona talla (`.talla-badge`) y color (`.color-option`) y los guarda en `data-talla`/`data-color` del botón `#btn-add-detail`.
- `checkoutWhatsApp()` arma el mensaje y abre `wa.me/573123080861` (listo para el pago Nequi + comprobante).

### Plantillas públicas
Extienden `base.html` (header sticky, menú móvil, footer, modal de guía de tallas, carrito sidebar, WhatsApp flotante). Páginas en `core/templates/core/`.

### Temas CSS
- `mejorada.css` = **tema activo** (clase `ha-theme` en `<body>`).
- `brand.css`, `estilos.css`, `tienda.css` = legados en su mayoría.

---

## 8. Admin de Django (`/admin/`)

- `ProductoAdmin`: inlines `ImagenProductoInline` (galería) y `VariacionInline` (tallas/colores/stock), previsualización de imagen.
- `TallaAdmin`, `ColorAdmin` (widget selector de color hex).
- `BannerAdmin`, `ResenaComunidadAdmin` (orden + activo editables en lista).
- `ArticuloBlogAdmin`: `prepopulated_fields` de slug, búsqueda por título/resumen, filtros.

---

## 9. SEO — Convenciones de `base.html`

Toda página extiende `base.html` y usa estos **bloques**:

```html
{% block title %}{% endblock %}
{% block meta_description %}{% endblock %}
{% block og_title %}{% endblock %}
{% block og_description %}{% endblock %}
{% block og_image %}{% endblock %}
{% block canonical %}{% endblock %}
{% block meta_extra %}{% endblock %}
```

- Keyword objetivo **"ropa para dama en Cúcuta"** + variantes (ropa para mujer en Cúcuta, moda femenina en Cúcuta, outfits en Cúcuta). Úsalas naturales en `title`, `h1`, `meta_description`, `alt`.
- Un solo `<h1>` por página. El home ya lo tiene ("ROPA PARA DAMA EN CÚCUTA").
- `alt` de imágenes de producto: `{{ producto.nombre }} - Ropa para dama en Cúcuta`.
- Schema JSON-LD: `ClothingStore` (en base), `Product` + `Offer` + `AggregateRating` (en detalle de producto).
- `base.html` ya incluye: GA4 (`G-TCS3JX9RV7`), Open Graph, Twitter Cards, canonical, favicons, meta geo (CO-NSA/Cúcuta).

### ⚠️ REGLA CRÍTICA — `{% if %}` y `{% block %}`

**NUNCA envuelvas un `{% block og_image %}` dentro de un `{% if objeto.imagen %}`.**

```html
<!-- MAL: 500 si el objeto no tiene imagen -->
{% if producto.imagen %}{% block og_image %}{{ ... }}{{ producto.imagen.url }}{% endblock %}{% endif %}

<!-- BIEN: el if va DENTRO del bloque -->
{% block og_image %}{% if producto.imagen %}{{ request.scheme }}://{{ request.get_host }}{{ producto.imagen.url }}{% else %}{% static 'img/productos/logo-lg.webp' %}{% endif %}{% endblock %}
```

Motivo: Django extrae los `{% block %}` al compilar aun dentro de un `{% if %}` falso e intenta resolver `objeto.imagen.url` → `ValueError: The 'imagen' attribute has no file associated` → **error 500**. Siempre pon el condicional **dentro** del bloque. (Bug real corregido en `blog_detalle.html` y `detalle_producto.html`.)

### Consultas
- Evita N+1: home y detalle ya usan `prefetch_related('variaciones__talla','variaciones__color','imagenes')`. Mantén el patrón.

---

## 10. Settings / Entorno / Base de datos

- `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` desde `.env` (via `python-dotenv`). Por defecto `DEBUG=True` si no está en `.env`.
- `DB_ENGINE` en `.env` → usa PostgreSQL; si no → SQLite.
- `LANGUAGE_CODE='es-co'`, `TIME_ZONE='America/Bogota'`, `USE_THOUSAND_SEPARATOR=True`.
- `CSRF_TRUSTED_ORIGINS` = `https://byheilynaguilar.com` y `www`.
- Login: `/usuarios/login/`, redirect `/`.
- Estáticos: `STATICFILES_DIRS=['static']`, `STATIC_ROOT=staticfiles`. Media: `media/`.
- `INSTALLED_APPS` incluye `django.contrib.sitemaps` y `django.contrib.humanize`.

Variables de `.env` (producción, ver `.env.example`):
`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

---

## 11. Despliegue a producción

VPS Linux (IONOS): Nginx + Gunicorn (systemd), código en `/var/www/tienda_heilyn`. Gestión vía GitHub → git pull.

```bash
cd /var/www/tienda_heilyn
git pull origin main
# si hubo cambios de modelo:
source venv/bin/activate && python manage.py migrate
python manage.py collectstatic --noinput   # si cambió static/css
# cambios de template NO requieren reiniciar (Django no cachea templates);
# tras modelo/código python nuevo, reinicia:
systemctl restart gunicorn-tienda
```

- Sitemap: `https://byheilynaguilar.com/sitemap.xml`. Registrar páginas nuevas en Google Search Console y pedir indexación.
- Google Analytics 4: `G-TCS3JX9RV7` (no duplicar).
- ⚠️ Tras agregar/quitar **estáticos** (favicons, fuentes, css) siempre correr `collectstatic`; el cambio no se ve en producción si no. En dúd de que los navegadores tengan cache vieja de estáticos "immutable 1 mes", recordar hard reload o `?v=`. El HTML no se cachea.

`deploy/gunicorn.service` / `deploy/gunicorn.socket` / `deploy/nginx.conf` son las plantillas de despliegue (405→HTTPS, static/media alias).

---

## 12. Pendientes SEO/Performance

### ✅ Hecho (ago 2026)
- **Miniaturas responsivas**: `Producto.imagen_thumb` (`_360.webp`) y `Producto.imagen_thumb_media` (`_627.webp`) generadas en `save()` + comando `generate_product_thumbs`. Las tarjetas usan 288x360; el hero (LCP) usa `_627` con `srcset="[mid] 627w, [main] 1080w"`, `fetchpriority="high"` y `width/height` explícitos (menos CLS/bandwidth).
- **Accesibilidad**: pestañas filtrantes con `role="group"` + `aria-pressed` (ya no `role="tablist"` huérfano); contraste subido en textos grises (0.5→0.72/0.75) y labels dorados (`#7A5226`); títulos "Tu carrito"/"Guía de Tallas" de `h5`→`h2`; número Nequi de `h5`→`div`.
- **Fuentes autoalojadas**: `static/fonts/fonts.css` (`@font-face` con `display:swap`) sirve Inter y Playfair Display (latin+latin-ext, una sola woff2 variable por familia). Font Awesome en `static/fontawesome/` (**Estructura oficial**: `css/all.min.css` + `webfonts/` hermanas). ⚠️ No mover `all.min.css` fuera de `css/`: el CSS usa `url(../webfonts/…)`, que solo resuelve bien desde `static/fontawesome/css/` → `/static/fontawesome/webfonts/`. Un error histórico (CSS en `fontawesome/` sin `css/`) hacía que pidiera `/static/webfonts/` → 404 y los iconos salían como cuadritos. Tras cambios en `static`, correr `collectstatic`.**Ya NO** se carga Google Fonts ni Font Awesome CDN en `base.html`.
- **Rendimiento móvil**: `bootstrap.min.css` se carga **asíncrono** (`media="print" onload="this.media='all'"` + `<noscript>`) con un **CSS crítico inline** replicando las utilidades del primer render (`.d-flex`, `.align-items-center`, `.gap-*`, `.m*`, `.btn`, `.visually-hidden`). JS con `defer` (`bootstrap.bundle.min.js`, `bolsa.js`). Reduce render-blocking y LCP en 4G lento. No añadir nuevas utilidades de Bootstrap críticas sin replicarlas en ese bloque inline.

### ✅ Estrategia de imágenes RESUELTA (ago 2026)
El LCP (hero) ya se sirve con variante `_627.webp` + `srcset`, eliminando el warning de imágenes del hero. Queda **opcional** para máxima escalabilidad:
- **Cloudinary** (plan free, vía `CloudinaryField` o `?tr=` en URL) — requiere cuenta + keys a `.env`.
- **Cloudflare Images** si el dominio ya pasa por Cloudflare.
(No necesario para el score actual; solo si se quiere variantes on-the-fly para blog/galerías.)

### ✅ Infraestructura Cloudflare (ago 2026)
- Zona activa en **Cloudflare** (plan free) con NS `keenan.ns.cloudflare.com` + `lily.ns.cloudflare.com` (IONOS). **DNSSEC OFF** (sin Domain Guard; si se activa, rompe la zona).
- **SSL Full** (edge). **Always Use HTTPS ON**. **Browser Cache TTL = 1 mes** (2678400, `immutable` en estáticos) → tras cambiar un estático, los navegadores con cache vieja pueden seguir 404; usar URL nueva (`?v=`) o pedir "Clear site data"/hard reload al usuario.
- **HTTP/3 + 0-RTT APAGADOS** (daba `ERR_QUIC_PROTOCOL_ERROR` en Chrome del usuario; con HTTP/3 off baja a HTTP/2 estable). Si se reactiva, vigilar errores QUIC en Chrome.
- HTML **no** se cachea en edge (opción A, sin Cache Rule): carrito va en `localStorage`, TTFB ~0.5s es aceptable.
- `Always Online` + `Crawler Hints` ON.

### ✅ Correcciones (ago 2026)
- **Favicons**: `static/img/favicon-16x16.png`, `favicon-32x32.png`, `favicon-48x48.png`, `apple-touch-icon.png` (180). Referenciados en `base.html`. ⚠️ Google no usa como icono de sitio un PNG >48px ni el logo 581×584 (por eso salía el globo). La cache de favicons de Google es **independiente y lenta** (puede tardar semanas en refrescarse; no es bug del sitio). Google prefiere `/favicon.ico` en la raíz (no servido aún por Django; opcional: nginx alias).
- **Página `/contacto/`**: reescrita sin mojibake, datos consistente con Cúcuta (ubicación, teléfono/WhatsApp **312 308 0861** — se eliminó el falso `573001234567` y la dirección "Bogotá"). Añadido `meta_description` con keyword.
- **H1 del hero** (`inicio.html`): quitado el `<em class="ha-italic">EN CÚCUTA</em>` → título uniforme (el italic solo estaba a peso 400 y se veía desigual contra el 500 del título).
- **Contacto/NAP**: número de ventas WhatsApp = `573123080861`; Nequi `312 308 0861`. Usar siempre estos (no inventar teléfonos en plantillas).

### ✅ Rediseño visual del blog (ago 2026)
- **Lista (`blog_lista.html`)**: contenedor amplio `max-width:1140px`. La primera entrada queda **destacada** a ancho completo (imagen vertical izquierda + texto grande, clase `.ha-blog-featured`); el resto en grid de 3 columnas (`.ha-blog-card`). Imágenes en **ratio vertical 3/4** con `object-fit:cover` y zoom on-hover (pensado para imágenes cargadas verticalmente). Meta: fecha + minutos de lectura.
- **Detalle (`blog_detalle.html`)**: contenedor `max-width:1120px`, texto `.ha-blog-content` a **980px** (antes 760, se veía estrecho). Hero en **ratio vertical 4/5 centrado y acotado a 780px** para no recortar imágenes verticales ni verse gigante. Drop cap dorado en el primer párrafo + caja CTA `.ha-blog-cta` con fondo crema.
- **Modelo**: propiedad `tiempo_lectura` en `ArticuloBlog` (len/contenido.split()/200, min 1). Sin migración (es property).
- **CSS**: nuevas clases `.ha-blog-*` al final de `mejorada.css`.
- **Versiones de static**: el `?v=` en el link de `mejorada.css` en `base.html` se incrementa manualmente (ej. `20260817c`) cada vez que cambia el CSS, para saltar la cache `immutable` de Cloudflare. ⚠️ Mantener este hábito.

### 🟡 Google Business Profile (ago 2026)
- **Creado y publicado** como "byheilynaguilar" (dashboard "Tu negocio en Google"). Ya enlaza web, Instagram (10.8k) y blog.
- Tareas pendientes de mayor impacto: **subir fotos**, **conseguir las primeras reseñas** (formulario por WhatsApp), **configurar seguimiento de conversiones**.
- ⚠️ Como es **tienda virtual**, usar **Área de servicio + ocultar dirección** en "Editar perfil → Información → Ubicación" (no mostrar una dirección física inventada).
- El SEO local ya da resultados: `ropa para dama en Cúcuta` → posición #1; `corset para mujer Cúcuta` → #2. Backlinks siguen siendo el gap principal (sin pagar).

---

## 13. Scripts auxiliares (`scripts/`)

- `convert_static_to_webp.py` → convierte estáticos a WebP.
- `logo_converter.py` → convierte logos a WebP.
- `fix_tallas_colors.py` → reparación de tallas/colores.
- `upload_colors.py` → carga de colores.

---

## 14. Comandos útiles

```bash
python manage.py check                    # config + templates
python manage.py makemigrations <app>
python manage.py migrate <app>
python manage.py collectstatic --noinput
python manage.py shell -c "..."           # depurar
```

Verificar una URL con el test client:
```python
python manage.py shell -c "from django.test import Client; c=Client(); print(c.get('/blog/').status_code)"
```