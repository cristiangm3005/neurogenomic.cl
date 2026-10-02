# neurogenomic.cl — sitio 2026

Experiencia de scroll inmersiva para **Neurogenomic** (Genomic Industries SpA) · *Neuroscience-Driven Marketing Optimization*.

## Concepto

**Un registro de laboratorio en vivo.** El sitio se lee como una sesión de medición biométrica y abre con un masthead editorial (wordmark gigante, tagline apilado y tres filas enmarcadas de navegación, secciones y disciplinas) que, al hacer scroll, se reduce a una barra fija compacta. Primero se calibra el instrumento (preloader de 5 puntos). El CTA final incluye un micro-formulario (solo correo + consentimiento) que también envía por FormSubmit. Luego se mira: la mirada recorre el propio titular («Todos miran. Nosotros medimos.») y tu cursor pasa a ser el punto de fijación. Después se mide: una demo cuadro a cuadro convierte la mirada en fijaciones, scanpath, heatmap y zonas ciegas; un registro sincronizado contrasta lo que se declara con lo que se mide, y el stack de herramientas (Python, SQL, NeuroKit2, Power BI…) muestra cómo se procesa cada estudio. Al final se decide. La narrativa avanza **Calibrar → Mirar → Medir (demo, packaging, señales y herramientas) → Servicios en resumen → Construir (método) → Probar (caso) → Proteger (ética) → Decidir (CTA)**. El detalle de los seis servicios vive en `servicios.html`. El lenguaje visual sale de las piezas de campaña de Neurogenomic: negro puro, un solo foco, titulares condensados en mayúsculas (Anton) con la palabra clave en lima `#C8FF00`, heatmaps térmicos pixelados y lecturas de datos con línea guía (IBM Plex Mono). El texto corrido va en Space Grotesk. Retículas, crosshairs y timestamps le dan la precisión de un laboratorio.

## Estructura

```
index.html · servicios.html · tecnologia.html · contacto.html   ← sitio listo (generado)
neurogenomic-index.html  ← inicio en un solo archivo (imágenes y 80 cuadros de la demo incrustados): se abre sin la carpeta img/
neurogenomic-sitio.zip   ← las 4 páginas + img/ listas para subir a un hosting
landing.html             ← landing B2B con demo scroll-driven (fuente: landing/src; build: landing/build_landing.py). Ver LANDING.md
neurogenomic-landing.html ← la misma landing en un solo archivo
elementor/00…19-*.html   ← cada sección como bloque autocontenido para el widget HTML de Elementor
img/                     ← fotos (lata, botella) y renders fotográficos (bolsa de café, caja de té, teléfono, 80 cuadros de la demo) en AVIF + WebP
src/data/*.json          ← calibración: posición de cada zona de los renders, para fijaciones y heatmaps
render/                  ← escenas de Blender (Cycles) que generan los renders; ver render/README.md
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
   - `00-global-nav` y `12-footer` van en el Theme Builder (header/footer) o al inicio y al final de cada página.
   - Inicio: `01` a `11`. Servicios: `13` + `14` + `08` + `15` + `11`. Tecnología: `16` + `05` + `06` + `17` + `04` + `09` + `10` + `11`. Contacto: `18` + `19`.
   - La numeración de los encabezados (01, 02…) se calcula según el orden de cada página. Los bloques sueltos llevan la numeración del inicio.
2. Cada bloque trae los tokens y el núcleo `NG`. Si se repiten, no pasa nada: el núcleo se inicializa una sola vez y cada sección usa una guarda `data-init` (arranca en `DOMContentLoaded`, `load` y `elementor/frontend/init`).
3. En el editor de Elementor se desactivan Lenis y los pins para poder editar con comodidad.
4. Sube los archivos de `img/` a la Biblioteca de medios y reemplaza `/img/` por esa URL en los bloques.
5. El formulario (`19-contacto-formulario`) ya envía a tu correo; ver la sección siguiente.
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
