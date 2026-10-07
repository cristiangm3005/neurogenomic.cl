# MetalGenomic · importar en Elementor Pro

Usar **`metalgenomic-landing-elementor-pro-v2.json`** (reemplaza a la versión anterior).

## Qué cambió en la v2 (por qué la v1 mostraba solo las montañas planas)
La v1 cargaba three.js con un `importmap` y un `<script type="module">`. En WordPress eso falla con facilidad:
- otro `importmap` o módulo cargado antes por WordPress 6.5+ o por un plugin (los navegadores anteriores a 2025 ignoran el segundo mapa);
- optimizadores de JS (LiteSpeed Cache, WP Rocket, Autoptimize, Cloudflare Rocket Loader) que cambian el tipo de los scripts;
- el editor de Elementor vuelve a pintar el widget y se acumulaban contextos WebGL.

La v2:
- usa solo scripts clásicos y un cargador propio que trae three.js y sus complementos desde jsDelivr (con respaldo en unpkg), sin `importmap`;
- deja una sola instancia viva aunque el editor vuelva a pintar el widget;
- si el navegador marca el GPU como de bajo rendimiento, reintenta antes de rendirse;
- trae un modo de diagnóstico.

## Importar
1. WordPress → Plantillas → Plantillas guardadas → **Importar plantillas** → subir el `.json` v2.
2. En la página: «Editar con Elementor» → carpeta → «Mis plantillas» → **Insertar** «MetalGenomic · Landing 3D» (si ya habías insertado la v1, borra ese widget primero).
3. Engranaje de la página → **Diseño de página = Elementor Canvas**.
4. Publicar y revisar **en la página publicada** (en el editor también carga, pero más lento).

## Si todavía no se ve el 3D
1. Abre la página publicada agregando `?mgdebug=1` al final de la URL (ej. `https://tusitio.cl/landing/?mgdebug=1`). Abajo a la izquierda aparece el estado y el motivo exacto («activo», «sin WebGL», «el motor 3D no cargó a tiempo», etc.).
2. Revisa estos puntos:
   - **Optimizadores**: excluye la página (o el script) de «Delay JS», «Defer JS», «Combine/Minify JS» en LiteSpeed Cache / WP Rocket / Autoptimize, y desactiva Rocket Loader de Cloudflare para esta URL.
   - **Rol del usuario**: guarda la página con un Administrador (capacidad `unfiltered_html`); si no, WordPress elimina los `<script>`. Algunos hostings definen `DISALLOW_UNFILTERED_HTML` en `wp-config.php`: en ese caso hay que quitarlo o pedirlo al hosting.
   - **Acceso a CDN**: el sitio debe poder cargar `cdn.jsdelivr.net` (o `unpkg.com`), `cdnjs.cloudflare.com` y Google Fonts; una política CSP estricta debe permitir `blob:` en `script-src`.
   - **Navegador**: aceleración por hardware activada (Chrome → Configuración → Sistema).

## SEO (configurar en el plugin de SEO)
- Título: «MetalGenomic | Biolixiviación, genómica e IA para minería en Chile»
- Meta descripción: «Biolixiviación, exploración geoespacial, mantenimiento predictivo y gemelo digital para la mediana minería. Diagnóstico de tu operación en hasta 4 semanas.»

## Editar textos
Todo está en un único widget **HTML**. Mantener clases, IDs y atributos `data-*`.
