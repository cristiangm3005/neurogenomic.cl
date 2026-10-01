# neurogenomic.cl — sitio 2026

Experiencia de scroll inmersiva para **Neurogenomic** (Genomic Industries SpA) · *Neuroscience-Driven Marketing Optimization*.

## Concepto

**Un registro de laboratorio en vivo.** El sitio se lee como una sesión de medición biométrica. Primero se calibra el instrumento (preloader de 5 puntos). Luego se mira: un ojo macro en el que tu cursor es el punto de fijación. Después se mide: la mirada sobre una pieza real se convierte en fijaciones, scanpath, heatmap y zonas ciegas. Al final se decide. La narrativa avanza **Calibrar → Mirar → Medir (95 %, tres señales) → Construir (6 servicios, método) → Probar (caso) → Proteger (ética) → Decidir (CTA)**. El cierre vuelve al mismo ojo con la pupila contraída. Todo el sistema visual usa negro carbón, volt `#C8F542` y la lima `#C8FF00` reservada para datos en vivo, con Space Grotesk + IBM Plex Mono. Retículas, crosshairs y timestamps le dan la precisión de un laboratorio.

## Estructura

```
index.html · servicios.html · tecnologia.html · contacto.html   ← sitio listo (generado)
elementor/00…16-*.html   ← cada sección como bloque autocontenido para el widget HTML de Elementor
IMAGENES.md              ← lista de imágenes (archivo, proporción, prompt)
src/core/tokens.css      ← sistema de diseño (colores, tipografía, utilidades ng-)
src/core/core.js         ← núcleo NG: carga GSAP/ScrollTrigger/Lenis una vez, guardas data-init, helpers
src/sections/*.html      ← fuente de cada sección (<style> + HTML + <script>)
build.py                 ← genera páginas, bloques Elementor e IMAGENES.md (python3 build.py)
```

Edita siempre `src/` y vuelve a ejecutar `python3 build.py`. Los HTML de la raíz y de `elementor/` son generados.

## Ver en local

Abre `index.html` en el navegador o sirve la carpeta (`python3 -m http.server`). Mientras no subas las imágenes, cada foto muestra un placeholder técnico con su nombre de archivo.

## Elementor / WordPress

1. Crea un widget **HTML** por bloque, a ancho completo y sin padding, y pega el archivo completo de `elementor/`.
   - `00-global-nav` y `12-footer` van en el Theme Builder (header/footer) o al inicio y al final de cada página.
   - Inicio: `01` a `11`. Servicios: `13` + `06` + `07` + `08` + `11`. Tecnología: `14` + `05` + `03` + `04` + `09` + `10` + `11`. Contacto: `15` + `16`.
2. Cada bloque trae los tokens y el núcleo `NG`. Si se repiten, no pasa nada: el núcleo se inicializa una sola vez y cada sección usa una guarda `data-init` (arranca en `DOMContentLoaded`, `load` y `elementor/frontend/init`).
3. En el editor de Elementor se desactivan Lenis y los pins para poder editar con comodidad.
4. Sube las imágenes y reemplaza `/img/` por la URL de la Biblioteca de medios.
5. **Formulario**: en `16-contacto-formulario`, completa `data-endpoint="…"` (Formspree, un webhook, admin-ajax, etc.). Recibe un POST JSON. Si queda vacío, valida y muestra el éxito sin enviar datos.
6. Crea las páginas `/privacidad/` y `/terminos/`, que enlazan el footer y el formulario.

## Stack

HTML semántico + CSS (custom properties, `clamp()`, container queries) + JS vanilla. GSAP 3.12.5 + ScrollTrigger (cdnjs) y Lenis 1.1.13 (jsDelivr) se cargan bajo demanda. Si el CDN falla, todo el contenido sigue visible y estático. Con `prefers-reduced-motion: reduce` no hay Lenis, pins, parallax, cursor ni preloader.
