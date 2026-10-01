# neurogenomic.cl — sitio 2026

Experiencia de scroll inmersiva para **Neurogenomic** (Genomic Industries SpA) · *Neuroscience-Driven Marketing Optimization*.

## Concepto

**Un registro de laboratorio en vivo.** El sitio se lee como una sesión de medición biométrica. Primero se calibra el instrumento (preloader de 5 puntos). Luego se mira: el ojo del perro («Todos miran. Nosotros medimos.»), donde tu cursor es el punto de fijación. Después se mide: la mirada sobre una pieza real se convierte en fijaciones, scanpath, heatmap y zonas ciegas. Al final se decide. La narrativa avanza **Calibrar → Mirar → Medir (95 %, tres señales) → Construir (6 servicios, método) → Probar (caso) → Proteger (ética) → Decidir (CTA)**. El cierre vuelve a ese mismo ojo en primer plano, con un anillo que se contrae sobre la pupila. El lenguaje visual sale de las piezas de campaña de Neurogenomic: negro puro, un solo foco, titulares condensados en mayúsculas (Anton) con la palabra clave en lima `#C8FF00`, heatmaps térmicos pixelados y lecturas de datos con línea guía (IBM Plex Mono). El texto corrido va en Space Grotesk. Retículas, crosshairs y timestamps le dan la precisión de un laboratorio.

## Estructura

```
index.html · servicios.html · tecnologia.html · contacto.html   ← sitio listo (generado)
elementor/00…18-*.html   ← cada sección como bloque autocontenido para el widget HTML de Elementor
img/                     ← fotos incluidas (perro, lata, botella) en AVIF + WebP
IMAGENES.md              ← imágenes incluidas y prompts opcionales
src/core/tokens.css      ← sistema de diseño (colores, tipografía, utilidades ng-)
src/core/core.js         ← núcleo NG: carga GSAP/ScrollTrigger/Lenis una vez, guardas data-init, helpers
src/sections/*.html      ← fuente de cada sección (<style> + HTML + <script>)
build.py                 ← genera páginas, bloques Elementor e IMAGENES.md (python3 build.py)
```

Edita siempre `src/` y vuelve a ejecutar `python3 build.py`. Los HTML de la raíz y de `elementor/` son generados.

## Ver en local

Abre `index.html` en el navegador o sirve la carpeta (`python3 -m http.server`). Las fotos ya vienen incluidas en `img/`.

## Elementor / WordPress

1. Crea un widget **HTML** por bloque, a ancho completo y sin padding, y pega el archivo completo de `elementor/`.
   - `00-global-nav` y `14-footer` van en el Theme Builder (header/footer) o al inicio y al final de cada página.
   - Inicio: `01` a `13`. Servicios: `15` + `08` + `09` + `10` + `13`. Tecnología: `16` + `06` + `07` + `03` + `04` + `05` + `11` + `12` + `13`. Contacto: `17` + `18`.
2. Cada bloque trae los tokens y el núcleo `NG`. Si se repiten, no pasa nada: el núcleo se inicializa una sola vez y cada sección usa una guarda `data-init` (arranca en `DOMContentLoaded`, `load` y `elementor/frontend/init`).
3. En el editor de Elementor se desactivan Lenis y los pins para poder editar con comodidad.
4. Sube los archivos de `img/` a la Biblioteca de medios y reemplaza `/img/` por esa URL en los bloques.
5. El formulario (`18-contacto-formulario`) ya envía a tu correo; ver la sección siguiente.
6. Crea las páginas `/privacidad/` y `/terminos/`, que enlazan el footer y el formulario.

## Stack

HTML semántico + CSS (custom properties, `clamp()`, container queries) + JS vanilla. GSAP 3.12.5 + ScrollTrigger (cdnjs) y Lenis 1.1.13 (jsDelivr) se cargan bajo demanda. Si el CDN falla, todo el contenido sigue visible y estático. Con `prefers-reduced-motion: reduce` no hay Lenis, pins, parallax, cursor ni preloader.

## Formulario de contacto → correo

Cada solicitud se envía con [FormSubmit](https://formsubmit.co) a **cristiangm3005@gmail.com**. El correo se configura en `FORM_EMAIL`, dentro de `build.py`.

- **Activación (una sola vez):** el primer envío desde el sitio publicado hace que FormSubmit mande a esa casilla un correo «Activate Form». Ábrelo y pulsa el botón. Desde ese momento todas las solicitudes llegan directo, en formato tabla, con asunto «Nueva solicitud de diagnóstico · Nombre (Empresa)». Si respondes, la respuesta va al correo de quien escribió.
- **Pruébalo desde el sitio publicado** (GitHub Pages o tu dominio). Abriendo el archivo con doble clic (`file://`), FormSubmit puede rechazar el envío.
- **Validación en línea:** servicio (al menos uno), empresa, cargo, mensaje (mínimo 20 caracteres), plazo, nombre, correo con formato válido y consentimiento. El teléfono y el sitio web son opcionales, pero se revisan si se completan. Incluye un campo trampa contra bots.
- Después de enviar se muestra la confirmación animada «Solicitud recibida». Si el envío falla, aparece un aviso para reintentar.
- **Ocultar el correo del código:** después de activar, FormSubmit te da un alias aleatorio. Ponlo en `FORM_ENDPOINT` y ejecuta `python3 build.py` de nuevo.
