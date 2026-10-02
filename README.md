# neurogenomic.cl — sitio 2026

Experiencia de scroll inmersiva para **Neurogenomic** (Genomic Industries SpA) · *Neuroscience-Driven Marketing Optimization*.

## Concepto

**Un registro de laboratorio en vivo.** El sitio se lee como una sesión de medición biométrica y abre con un masthead editorial (wordmark gigante, tagline apilado y tres filas enmarcadas de navegación, secciones y disciplinas) que, al hacer scroll, se reduce a una barra fija compacta. Primero se calibra el instrumento (preloader de 5 puntos). El CTA final incluye un micro-formulario (solo correo + consentimiento) que también envía por FormSubmit. Luego se mira: la mirada recorre el propio titular («Todos miran. Nosotros medimos.») y tu cursor pasa a ser el punto de fijación. Después se mide: una demo cuadro a cuadro convierte la mirada en fijaciones, scanpath, heatmap y zonas ciegas; un registro sincronizado contrasta lo que se declara con lo que se mide, y el stack de herramientas (Python, SQL, NeuroKit2, Power BI…) muestra cómo se procesa cada estudio. Al final se decide. La narrativa avanza **Calibrar → Mirar → Medir (demo, packaging, señales y herramientas) → Servicios en resumen → Construir (método) → Probar (caso) → Proteger (ética) → Decidir (CTA)**. El detalle de los seis servicios vive en `servicios.html`. El lenguaje visual sale de las piezas de campaña de Neurogenomic: negro puro, un solo foco, titulares condensados en mayúsculas (Anton) con la palabra clave en lima `#C8FF00`, heatmaps térmicos pixelados y lecturas de datos con línea guía (IBM Plex Mono). El texto corrido va en Space Grotesk. Retículas, crosshairs y timestamps le dan la precisión de un laboratorio.

## Historia 3D · «De la neurona al consumidor»

El inicio se recorre como una historia continua sobre una sola escena WebGL (Three.js r128, cargada desde cdnjs cuando el navegador queda libre). Una nube de partículas cambia de forma con el scroll:

1. **Neurona** (detrás del hero y en el capítulo 01): soma, dendritas, axón con impulsos de luz y neurotransmisores que cruzan la sinapsis.
2. **Señales** (capítulo 02): los impulsos se vuelven corrientes de datos, nodos de comportamiento y un mapa de calor de atención.
3. **Datos + IA** (capítulo 03): pasillo de servidores y un núcleo de IA.
4. **Estrategia** (capítulo 04): cinco nodos (datos, emociones, mensajes, productos y segmentos) unidos por rutas.
5. **Consumidor** (capítulo 05): silueta abstracta con productos, mensajes y canales que lo orbitan.

Las secciones existentes quedan entre los capítulos, con fondo translúcido sobre la escena.

Composición y rendimiento:
- **Composición:** la escena se desplaza hacia el lado contrario al texto (offset 2,8–3,3), con cámara a z≈12,5 y FOV 52°. Lleva niebla exponencial y un desenfoque de profundidad que agranda y atenúa las partículas fuera de foco.
- **Cursor:** las partículas cercanas al cursor se apartan y brillan en lima.
- **Textos:** van en paneles con `backdrop-filter: blur(12px)` sobre `rgba(10,10,15,.65)`.
- **Navegación:** a la derecha hay un dock de capítulos ([01 NEURONA] → [05 IMPACTO]) que se navega con teclado y hace scroll suave. Abajo a la izquierda hay un botón para pausar la animación, que el navegador recuerda.
- **Rendimiento:** un IntersectionObserver congela el render cuando la historia no está en pantalla. Mientras se compilan los shaders se muestra un indicador de carga.
- **Cierre:** al terminar el capítulo 05 la escena se funde y entra la sección de contacto.
- **Móvil:** 6 000 partículas (16 000 en escritorio), escena centrada y escalada, y opacidad de 35 % mientras hay texto encima. Con `prefers-reduced-motion` la escena queda quieta y solo cambia con el scroll. En móvil se usan menos partículas y menor resolución. Sin WebGL se muestran `img/story/cap-1…5.webp`, que son capturas de la propia escena. El azul, violeta, cian y dorado se usan solo en la atmósfera 3D: la interfaz mantiene el negro y el lima de la marca.

## Responsive

Breakpoints: ≤575 (teléfono), 576–767 (tablet vertical), 768–991 (tablet horizontal), 992–1199 (laptop) y ≥1200 (escritorio).
- **Navegación:** horizontal desde 992 px. Por debajo hay un menú hamburguesa accesible: `aria-expanded`/`aria-controls`, foco atrapado, cierre con Escape y el foco vuelve al botón que lo abrió. La barra fija mide 64 px en teléfonos y se oculta al bajar.
- **Grillas:** las de 3 o más columnas pasan a 2 en tablet y a 1 en teléfono.
- **Tamaños:** los textos mínimos son de 11 px y todas las áreas táctiles miden al menos 44 × 44 px.
- **Revisión:** se revisa sin scroll horizontal en 320, 360, 390, 414, 768, 820, 1024, 1280, 1440 y 1920 px de ancho, en las 4 páginas y en el archivo único.

## Estructura

```
index.html · servicios.html · tecnologia.html · contacto.html   ← sitio listo (generado)
neurogenomic-index.html  ← inicio en un solo archivo (imágenes y 80 cuadros de la demo incrustados): se abre sin la carpeta img/
neurogenomic-sitio.zip   ← las 4 páginas + img/ listas para subir a un hosting
landing.html             ← landing B2B con demo scroll-driven (fuente: landing/src; build: landing/build_landing.py). Ver LANDING.md
neurogenomic-landing.html ← la misma landing en un solo archivo
elementor/00…25-*.html   ← cada sección como bloque autocontenido para el widget HTML de Elementor
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
   - `00-global-nav` y `18-footer` van en el Theme Builder (header/footer) o al inicio y al final de cada página.
   - Inicio: `01` a `17`, en orden (`02-historia-3d` una sola vez, antes del hero). Servicios: `19` + `20` + `14` + `21` + `17`. Tecnología: `22` + `08` + `10` + `23` + `07` + `15` + `11` + `17`. Contacto: `24` + `25`.
   - La numeración de los encabezados (01, 02…) se calcula según el orden de cada página. Los bloques sueltos llevan la numeración del inicio.
2. Cada bloque trae los tokens y el núcleo `NG`. Si se repiten, no pasa nada: el núcleo se inicializa una sola vez y cada sección usa una guarda `data-init` (arranca en `DOMContentLoaded`, `load` y `elementor/frontend/init`).
3. En el editor de Elementor se desactivan Lenis y los pins para poder editar con comodidad.
4. Sube los archivos de `img/` a la Biblioteca de medios y reemplaza `/img/` por esa URL en los bloques.
5. El formulario (`25-contacto-formulario`) ya envía a tu correo; ver la sección siguiente.
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
