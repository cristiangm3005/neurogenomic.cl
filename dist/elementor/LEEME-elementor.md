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

## v4 (usar esta)
`metalgenomic-landing-elementor-pro-v4.json` parte de la v3 y corrige:
- **Títulos en negro dentro de Elementor:** el kit global del sitio (Sitio › Tipografía/Colores) pintaba los `h1–h6`, `p`, enlaces y botones. Ahora la landing tiene prioridad sobre el kit, así que se ve igual en cualquier tema.
- **Halos borrosos bajo el texto:** se quitaron todas las sombras difusas del texto y el efecto «lupa» de las letras al pasar el cursor. El contraste lo da el velo oscuro del fondo, más firme donde la planta se ve blanca.
- **Paneles cortados en el editor móvil:** el alto de cada escena se mide con la ventana real, no con unidades `svh`.
- **Portada en dos líneas** («Del dato / al cátodo.») para que en escritorio se vean la bajada y el botón sin hacer scroll.
- **Electroobtención en móvil:** el texto ya no queda bajo las barras negras.
- Ajustes de redacción en varias frases.

Importa la v4 igual que las anteriores y reemplaza el widget de la versión previa.

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

## Si en otro navegador dice «Página no encontrada» (404)
No es el código del 3D: en el editor estás conectado como administrador y ves cosas que un visitante no ve. Revisa en este orden:
1. **Estás abriendo la plantilla, no una página.** Las URL tipo `/?elementor_library=...` o `/elementor_library/...` (Plantillas → Plantillas guardadas → «Vista previa») son privadas y dan 404 a cualquier visitante. Crea una página real: **Páginas → Añadir nueva → Editar con Elementor → Insertar** la plantilla.
2. **La página no está publicada.** Botón **Publicar** (no «Guardar borrador» ni «Vista previa»; las URL con `preview=true` o `?p=123&preview` solo funcionan con sesión iniciada). En Páginas → Todas, el estado debe decir «Publicada», no «Borrador», «Pendiente» ni «Programada».
3. **Visibilidad = Pública** (no «Privada» ni «Protegida con contraseña»).
4. **Usa la URL correcta:** en Páginas → Todas, pasa el mouse sobre la página → **Ver**. Copia esa dirección y pruébala en una ventana de incógnito.
5. **Refresca los enlaces permanentes:** Ajustes → Enlaces permanentes → **Guardar cambios** (sin cambiar nada). Arregla la mayoría de los 404 de páginas nuevas.
6. **Limpia la caché** (LiteSpeed, WP Rocket, Cloudflare, caché del hosting): pueden seguir sirviendo el 404 antiguo.
7. **Modo mantenimiento / «Próximamente»** de Elementor (Elementor → Herramientas → Modo mantenimiento) o plugins de seguridad/membresía que restrinjan la página a usuarios conectados: desactívalos o excluye la página.
8. **Dominio:** confirma que abres el mismo dominio que WordPress tiene en Ajustes → Generales (con o sin `www`, `https`). Si el dominio es nuevo, la DNS puede tardar en propagarse en otras redes.

Cuando la página se vea en incógnito, comprueba el 3D con `?mgdebug=1`.

## SEO (configurar en el plugin de SEO)
- Título: «MetalGenomic | Biolixiviación, genómica e IA para minería en Chile»
- Meta descripción: «Biolixiviación, exploración geoespacial, mantenimiento predictivo y gemelo digital para la mediana minería. Diagnóstico de tu operación en hasta 4 semanas.»

## Editar textos
Todo está en un único widget **HTML**. Mantener clases, IDs y atributos `data-*`.
