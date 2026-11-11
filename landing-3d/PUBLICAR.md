# Publicar neurogenomic.cl: portada, Contacto y Privacidad

Hoy la portada enlaza a `/contacto/` y `/privacidad/`, pero ambas páginas devuelven 404. Esta guía las publica y deja un canal de contacto que funciona.

## Archivos

| Página | URL | Plantilla de Elementor | Para pegar en un widget HTML |
|---|---|---|---|
| Portada | `/` | `neurogenomic-landing-3d-elementor.json` | `neurogenomic-landing-3d-widget.html` |
| Contacto | `/contacto/` | `paginas/neurogenomic-contacto-elementor.json` | `paginas/neurogenomic-contacto-widget.html` |
| Privacidad | `/privacidad/` | `paginas/neurogenomic-privacidad-elementor.json` | `paginas/neurogenomic-privacidad-widget.html` |
| Método | `/metodo/` | `paginas/neurogenomic-metodo-elementor.json` | `paginas/neurogenomic-metodo-widget.html` |
| Servicios (índice) | `/servicios/` | `paginas/neurogenomic-servicios-elementor.json` | `paginas/neurogenomic-servicios-widget.html` |
| Cada servicio (6) | `/servicios/<slug>/` | `paginas/servicios/neurogenomic-<slug>-elementor.json` | `paginas/servicios/neurogenomic-<slug>-widget.html` |

Slugs de los servicios: `branding`, `business-intelligence`, `ecommerce`, `marketing-digital`, `seo`, `desarrollo-web`. Crea cada página con **Página superior: Servicios** (panel derecho, «Atributos de página») para que su URL quede como `/servicios/<slug>/`. Los plazos y precios se editan en `servicios.json`; vacíos se publican como «Se define en el diagnóstico» y «A cotizar».

Antes de publicar, completa `datos-legales.json` (RUT, domicilio, fecha de actualización) y confirma los plazos propuestos. Luego ejecuta `python3 landing-3d/build.py`. Un campo vacío no se publica.

## 1. Crear las páginas (arregla el 404)

1. **Páginas › Añadir nueva.** Título «Contacto».
2. En el panel derecho, en **Enlace permanente / Slug**, escribe exactamente `contacto`. Si WordPress propone `contacto-2`, ya existe otra página con ese slug: búscala en Páginas (también en **Borradores** y en la **Papelera**), elimínala definitivamente y vuelve a poner `contacto`.
3. Pulsa **Editar con Elementor**. Abre la carpeta de plantillas, luego **Mis plantillas**, luego **Importar**, y elige el JSON de la tabla. Pulsa **Insertar** y acepta los ajustes de página (Elementor Canvas).
4. Pulsa **Publicar**. Un borrador o una página privada también da 404 a los visitantes.
5. Repite con «Privacidad» (slug `privacidad`), «Método» (`metodo`) y «Servicios» (`servicios`), y luego con los seis servicios como páginas hijas de «Servicios».

## 2. Enlaces permanentes y `.htaccess`

1. Ve a **Ajustes › Enlaces permanentes**, elige **Nombre de la entrada** y pulsa **Guardar cambios** aunque ya esté marcado. Esto regenera las reglas de reescritura.
2. Si sigue el 404 y el hosting usa **Apache**, revisa que el `.htaccess` de la raíz del sitio contenga este bloque y que no esté duplicado ni lo pise otra regla:

```apache
# BEGIN WordPress
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>
# END WordPress
```

3. Si el hosting usa **Nginx**, el bloque `location /` debe incluir `try_files $uri $uri/ /index.php?$args;`. Esto lo cambia el hosting.
4. Vacía la caché del plugin de caché, de la CDN (por ejemplo, Cloudflare) y del hosting.
5. Comprueba en una ventana de incógnito que `https://neurogenomic.cl/contacto/` y `https://neurogenomic.cl/privacidad/` respondan.

## 3. Formularios: prueba real

Los formularios (portada y contacto) envían por **POST** a FormSubmit. Con JavaScript se envían sin salir de la página. Sin JavaScript, por ejemplo si un plugin de optimización lo retrasa, el navegador valida los campos y envía igual por POST. Ya no hay envío por GET a la portada.

1. **Activación de FormSubmit:** el primer envío a un correo nuevo dispara un mensaje de FormSubmit pidiendo confirmar el formulario. Hasta que se pulse ese enlace, los mensajes no llegan. Revisa también la carpeta de spam.
2. Envía una prueba desde `/contacto/` y otra desde el micro-formulario de la portada, con un correo propio.
3. Confirma que llegan con asunto «Contacto · neurogenomic.cl» o «Solicitud de demo (portada) · neurogenomic.cl», y que responder al mensaje va al correo del interesado.
4. Si usas un plugin de optimización (WP Rocket, LiteSpeed, Autoptimize u otro), excluye estas páginas de «retrasar JavaScript».

## 4. Correo visible

`contacto@neurogenomic.cl` aparece en la portada, junto al formulario y en el pie, en Contacto y en Privacidad. **Verifica que esa casilla exista y reciba correo** antes de publicar: envía un correo de prueba desde otra cuenta.
