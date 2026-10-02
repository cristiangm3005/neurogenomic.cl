# Neurogenomic · Página de inicio nativa para Elementor Pro

> **Versión simplificada.** Para el diseño completo, con la historia 3D, los mapas de calor interactivos y todas las animaciones, usa `elementor-json/neurogenomic-inicio.json` (ver `WORDPRESS-ELEMENTOR.md`). Esta versión nativa solo conviene si necesitas editar cada texto con los controles de Elementor.

**Archivo para importar:** `neurogenomic-inicio-elementor-pro.json`. Se regenera con `python3 elementor-nativo/build_nativo.py`.

Es la página de inicio completa hecha solo con widgets nativos (sin widgets HTML). Al importarla, las imágenes se
descargan solas a la Biblioteca de Medios y todo el movimiento usa funciones de Elementor Pro: Motion Effects,
Entrance Animations, Sticky y hover.

## 1 · Probado en

- WordPress 7.1.2.
- Elementor 3.33.
- Elementor Pro 3.33.1, probado con la compilación GPL equivalente de la misma versión.

Se importó con el mismo proceso de importación de plantillas que usa el editor y se revisó en un navegador a 1440 px
y a 390 px:
- **Errores:** ninguno en la consola y ninguna imagen sin cargar.
- **Desborde:** sin scroll horizontal.
- **Imágenes:** 11 imágenes importadas a la Biblioteca de Medios.
- **Fondos:** 6 capas con parallax y zoom que cambian con el scroll.
- **Entradas:** 99 animaciones de entrada que se activan al bajar.
- **Encabezado:** el sticky cambia de fondo después de 80 px.
- **Mapa de calor:** pasa de opacidad 0 a 1 al hacer scroll.

## 2 · Qué se anima y cómo

| Sección | Imagen | Animación (nativa de Elementor Pro) |
|---|---|---|
| Hero | Escena 3D de la neurona | Fondo con parallax, zoom y seguimiento del mouse; titular con entrada, parallax y fundido |
| Capítulos 01 a 05 | Escenas 3D: neurona, señales, servidores, estrategia, consumidor | Mismo fondo con parallax y zoom; titulares con parallax lento; pasos con entrada escalonada |
| 01 · Así mira tu cliente | Bolsa de café y la misma foto con el mapa de calor | El mapa de calor aparece con el scroll (Transparency › Fade In) |
| 02 · Packaging | Botella y la misma botella con el mapa de calor | El mapa de calor aparece con el scroll |
| 09 · Diagnóstico | Teléfono con una tienda ficticia | Parallax vertical |
| Encabezado | — | Sticky; fondo sólido después de 80 px |
| Tarjetas, pasos y botones | — | Entrada escalonada; borde lima y «Float» al pasar el cursor |
| Franja de disciplinas y logotipo del pie | — | Desplazamiento horizontal con el scroll |

**Imágenes de escritorio:** se importan a tu Biblioteca de Medios.

**Imágenes de móvil (fondos 9:16):** Elementor no importa las imágenes de fondo responsivas, así que quedan enlazadas
al repositorio público de GitHub, con una URL fija que no cambia. Si prefieres tenerlas en tu sitio:
1. Sube `img/el/el-*-movil.webp` a Medios.
2. En cada sección, ve a Estilo › Fondo, cambia a la vista móvil y elige la imagen.

## 3 · Cómo importar

1. **Elementor › Ajustes:** deja activada la carga de Google Fonts.
2. **Plantillas › Plantillas guardadas › Importar plantillas:** elige `neurogenomic-inicio-elementor-pro.json` y pulsa
   Importar.
3. **Crear la página:** Páginas › Añadir nueva › Editar con Elementor › ícono de carpeta › Mis plantillas › Insertar.
   Cuando pregunte si quieres aplicar los ajustes de la plantilla, responde **Sí**. Eso trae la plantilla Canvas, el
   fondo negro y el CSS de la página.
4. **Publicar** y revisar la página en una ventana privada.

Si tienes un plugin de caché u optimización (WP Rocket, LiteSpeed, Autoptimize, SiteGround Optimizer…), excluye los
scripts de Elementor de «Retrasar JavaScript» y de «Combinar JS». Si no, las animaciones de entrada y de scroll no
arrancan hasta que el visitante interactúa.

## 5 · Opcional: cambiar las imágenes por videos de Higgsfield

**Cómo se consigue el loop sin corte.** Higgsfield no tiene un interruptor de loop. El loop se logra así:

1. Generar primero un **fotograma clave** (imagen) en 16:9 y otro en 9:16.
2. Generar el video con ese mismo fotograma como **imagen inicial y final** (`--start-image` y `--end-image`).
3. Si aun así queda un salto, aplicar un fundido cruzado de 0,5 s al comprimir (paso 4).

**Por qué los prompts van en inglés.** Los modelos de video siguen mejor las instrucciones en inglés.

**La lista «Evitar».** Higgsfield no tiene campo de prompt negativo, así que lo que hay que evitar va redactado en
positivo dentro del prompt. La lista «Evitar» de cada clip sirve para revisarlo antes de aprobarlo.

**Base común de marca** (ya incluida en cada prompt): fondo casi negro `#0A0B0D`, grafito `#111316`, blanco roto
`#F2F3F0`, gris frío `#A0A5B0` y un único acento lima `#C8FF00` que ocupa menos del 10 % del cuadro. El encuadre deja
mucho espacio negativo para el texto, que nunca va dentro del video.

**Modelos.**

| Clip | Modelo recomendado | Por qué |
|---|---|---|
| V01 Hero | Seedance 2.5 (`seedance_2_5`) | Mejor coherencia de movimiento en partículas finas; admite imagen inicial y final para el loop, hasta 1080p. |
| V02, V03, V06, V07 | Kling 3.0 (`kling3_0`) | Más económico para fondos de un solo plano y movimiento lento; también admite imagen inicial y final. |
| V04 Demo de mirada | Seedance 2.5 | Necesita que la maqueta no cambie mientras el mapa de calor crece; es el modelo más estable en eso. |
| V05 Packaging | Seedance 2.5 (`omni_reference`) | Puede partir del render real de la botella del sitio (`img/ng-bottle-1200.webp`) como imagen inicial y final. |
| V08 Impacto | Seedance 2.5 | Partículas que convergen en una silueta: es un movimiento complejo que Kling resuelve peor. |

Los fotogramas clave se generan con GPT Image 2.5 (`gpt_image_2_5`), el modelo por defecto de Higgsfield para
imagen. Los nombres de modelo vienen del catálogo de las habilidades de Higgsfield instaladas en el repo. Antes de
generar, confirma los parámetros con `higgsfield model get <modelo> --json`, porque requiere haber iniciado sesión.

### Flujo y comandos (iguales para los 8 clips)
```bash
# 1) Fotograma clave (imagen) en cada formato: es también el poster
higgsfield generate create gpt_image_2_5 --prompt "<PROMPT 16:9>" --aspect_ratio 16:9 --wait
higgsfield generate create gpt_image_2_5 --prompt "<PROMPT con la frase 9:16>" --aspect_ratio 9:16 --wait
# 2) Video con el mismo fotograma al inicio y al final (así cierra el loop)
higgsfield generate create seedance_2_5 --mode omni_reference --start-image key_16x9.png --end-image key_16x9.png --duration 8 --resolution 1080p --prompt "<PROMPT 16:9>" --wait
higgsfield generate create kling3_0 --start-image key_16x9.png --end-image key_16x9.png --duration 8 --prompt "<PROMPT 16:9>" --wait
# Antes de generar, confirma los parámetros: higgsfield model get seedance_2_5 --json  /  higgsfield model get kling3_0 --json
```
- **Formato:** sale del fotograma inicial. Para la versión 9:16 repite el paso 2 con `key_9x16.png`.
- **Prompt 9:16:** cambia la frase de encuadre por la que indica cada clip en «Frase 9:16».
- **Audio:** desactívalo si el modelo lo permite. De todos modos se elimina al comprimir (`-an`).

#### V01 · Hero en loop · `VIDEO_HERO_URL`
```text
MODELO: Seedance 2.5 (seedance_2_5) · 8 s · 1080p · 16:9 escritorio + 9:16 móvil · sin audio
ESCENA: vacío negro infinito con polvo desenfocado que da profundidad
SUJETO: una neurona de miles de partículas luminosas; dendritas ramificadas y axón largo con pulsos sinápticos
CÁMARA: órbita muy lenta de 10° con leve acercamiento; vuelve exactamente al encuadre inicial
ESTILO: visualización científica premium, partículas fotorrealistas, poca profundidad de campo, grano fino
PALETA: fondo #0A0B0D · partículas #F2F3F0 y #A0A5B0 · pulsos #C8FF00 (menos del 10 % del cuadro)
ILUMINACIÓN: clave baja, contraluz frío suave; el único color es el lima de los pulsos
DURACIÓN / FORMATO: 8 s · 16:9 y 9:16
LOOP: fotograma inicial = final; una sola toma continua, sin cortes
EVITAR: texto, letras, números, logos, marcas de agua, HUD o interfaces, cerebros rosados, rostros, destellos de lente, glitch, parpadeos o flashes, cortes rápidos, cámara temblorosa

PROMPT 16:9:
A single neuron made of tens of thousands of fine glowing particles floating in an infinite near-black void (#0A0B0D). Branching dendrites and a long axon in soft off-white (#F2F3F0) and cool grey (#A0A5B0); slow lime-green (#C8FF00) synaptic pulses travel along the axon every few seconds. The neuron sits in the right third of the frame and the left two thirds stay dark and empty. Very slow 10-degree orbit with a gentle push-in that returns exactly to the opening framing. Premium scientific visualization, photoreal particles, shallow depth of field, out-of-focus dust motes, fine film grain, low-key lighting with a soft cool rim light. Calm continuous motion in one single take, seamless loop. Clean frame without any text, logos or interface elements; steady, smooth camera.

Frase 9:16: The neuron sits in the upper third of the vertical frame and the lower half stays dark and empty.
```

#### V02 · Capítulo 01 «Origen neuronal» · `VIDEO_CAP1_URL`
```text
MODELO: Kling 3.0 (kling3_0) · 8 s · 720p · 16:9 + 9:16 · sin audio
ESCENA: macro de una sinapsis en un espacio oscuro y húmedo
SUJETO: dos terminales nerviosas casi tocándose; partículas de neurotransmisor cruzan lentamente la hendidura
CÁMARA: macro fija con una «respiración» de foco muy suave (rack focus de ida y vuelta)
ESTILO: microscopía cinematográfica, texturas orgánicas translúcidas, bokeh suave
PALETA: fondo #0A0B0D · membranas #111316 y #A0A5B0 · partículas lima #C8FF00 en pequeños destellos
ILUMINACIÓN: contraluz difuso frío; las partículas tienen un brillo propio suave
DURACIÓN / FORMATO: 8 s · 16:9 y 9:16
LOOP: inicio = final; las partículas fluyen de forma continua
EVITAR: texto, números, logos, sangre o tonos rojos, estética médica de quirófano, rostros, flashes, cortes

PROMPT 16:9:
Extreme macro of a synapse in a dark, moist space: two translucent nerve terminals almost touching, with tiny lime-green (#C8FF00) neurotransmitter particles drifting slowly across the gap. Membranes in graphite (#111316) and cool grey (#A0A5B0) against a near-black background (#0A0B0D). The synapse sits in the right half of the frame and the left half is soft dark bokeh. Locked-off macro camera with a very slow, subtle focus breathing that returns to the starting focus. Cinematic microscopy, organic translucent textures, soft diffuse cool backlight, gentle glow on the particles. Continuous calm motion in one take, seamless loop, clean frame without text or logos.

Frase 9:16: The synapse sits in the upper half of the vertical frame and the lower half is soft dark bokeh.
```

#### V03 · Capítulo 02 «Señales y comportamiento» · `VIDEO_CAP2_URL`
```text
MODELO: Kling 3.0 (kling3_0) · 8 s · 720p · 16:9 + 9:16 · sin audio
ESCENA: espacio oscuro con profundidad donde flotan trazos de señal
SUJETO: líneas finas de señal en capas a distintas profundidades: un trazo de mirada (puntos unidos por una línea), una onda suave de conductancia de la piel y una nube de puntos abstracta; todo fluye de izquierda a derecha
CÁMARA: travelling lateral lento de derecha a izquierda, con parallax entre capas
ESTILO: visualización de datos minimalista con aspecto físico (luz real, desenfoque de profundidad), nada de interfaz
PALETA: fondo #0A0B0D · trazos #A0A5B0 y #F2F3F0 · un solo trazo activo en lima #C8FF00
ILUMINACIÓN: los trazos emiten luz tenue; sin focos externos
DURACIÓN / FORMATO: 8 s · 16:9 y 9:16
LOOP: inicio = final; flujo continuo
EVITAR: texto, ejes con números, cuadrículas de gráfico, rostros, HUD de ciencia ficción azul, flashes, cortes

PROMPT 16:9:
Fine luminous signal traces float in layers at different depths in a near-black space (#0A0B0D): a gaze path of small dots joined by a thin line, a smooth skin-conductance wave and an abstract cloud of points, all flowing gently from left to right. Most traces are cool grey (#A0A5B0) and off-white (#F2F3F0); a single active trace glows lime green (#C8FF00). The traces sit mostly in the lower and right part of the frame, keeping the upper left area dark and calm. Slow lateral camera truck with soft parallax between layers. Minimal, physical-looking data visualization with real light falloff and depth-of-field blur, no interface. One continuous take, seamless loop, clean frame without any text, numbers or chart axes.

Frase 9:16: The traces sit mostly in the upper half of the vertical frame and the lower half stays dark and calm.
```

#### V04 · Destacado «Así mira tu cliente» · `VIDEO_DEMO_MIRADA_URL`
```text
MODELO: Seedance 2.5 (seedance_2_5) · 10 s · 1080p · 16:9 + 9:16 · sin audio
ESCENA: vista cenital de una maqueta minimalista de página web hecha solo de bloques grises (imagen principal, titular como barras, botón), sin ningún texto
SUJETO: aparecen fijaciones de mirada como puntos con anillo lima unidos por una línea fina; un mapa de calor florece sobre la imagen principal y el botón, y luego se desvanece hasta dejar la maqueta limpia
CÁMARA: fija, totalmente quieta
ESTILO: demo de producto limpia y elegante; mapa de calor suave y translúcido
PALETA: maqueta #111316 y #16191D sobre #0A0B0D · fijaciones #C8FF00 · calor de gris frío a lima a blanco cálido
ILUMINACIÓN: plana y suave, sin reflejos
DURACIÓN / FORMATO: 10 s · 16:9 y 9:16
LOOP: inicio y final = maqueta limpia sin mapa de calor
EVITAR: texto legible, letras falsas, logos, cursor del mouse, rojo o arcoíris clásico en el mapa de calor, rostros, movimiento de cámara, flashes
NOTA: en la página va acompañado de «Demostración visual. No corresponde a datos de un estudio real.» (texto fuera del video)

PROMPT 16:9:
Top-down, locked-off view of a minimalist web page wireframe made only of grey blocks (#111316 and #16191D on a #0A0B0D background): a large hero image block, headline shown as solid bars and a rounded button block, with no letters at all. Small lime-green (#C8FF00) ringed dots appear one by one as gaze fixations, linked by a thin line in viewing order; a soft translucent heat map blooms over the hero image and the button, going from cool grey through lime to warm white, then gently fades away until the wireframe is clean again. Elegant, calm product demo, flat soft lighting, no reflections, perfectly still camera. Seamless loop that starts and ends on the clean wireframe, without any readable text, logos or mouse cursor.

Frase 9:16: The wireframe is a vertical mobile page layout that fills the frame.
```

#### V05 · Destacado «Packaging» · `VIDEO_PACKAGING_URL`
```text
MODELO: Seedance 2.5 (seedance_2_5, modo omni_reference) · 8 s · 1080p · 16:9 + 9:16 · sin audio
FOTOGRAMA INICIAL Y FINAL: el render del sitio img/ng-bottle-1200.webp (exportado a PNG) para que la botella sea la misma
ESCENA: estudio oscuro, suelo de pizarra mate
SUJETO: botella de vidrio sin marca con líquido ámbar, tapa metálica y etiqueta negra lisa con un filete lima; un mapa de calor translúcido florece sobre la etiqueta (más intenso), la tapa, el hombro (suave) y la base (tenue), y se desvanece
CÁMARA: giro muy lento de la botella, 12° hacia un lado y vuelta al punto inicial (ida y vuelta)
ESTILO: fotografía de producto premium, vidrio realista con refracción
PALETA: fondo #0A0B0D · líquido ámbar · acento #C8FF00 · calor de gris frío a lima a blanco cálido
ILUMINACIÓN: luz principal cálida lateral, contraluz lima fino, filo frío; sin brillo en el suelo
DURACIÓN / FORMATO: 8 s · 16:9 y 9:16
LOOP: inicio = final (misma imagen de referencia)
EVITAR: nombres, textos o logos en la botella, marcas reales, manos, salpicaduras, cambios de forma de la botella, reflejos en el suelo, flashes
NOTA: en la página va acompañado de «Demostración visual» (texto fuera del video)

PROMPT 16:9:
The same unbranded glass bottle from the reference image: amber liquid, metal crown cap and a plain black label with a thin lime stripe, standing on a matte dark slate floor in a near-black studio (#0A0B0D). A soft translucent eye-tracking heat map blooms on the bottle: strongest on the label, clear on the cap, softer on the shoulder and faint at the base, glowing from cool grey through lime (#C8FF00) to warm white, then fades away. The bottle turns very slowly about 12 degrees to one side and back to its starting angle. The bottle stays centred with generous dark space on both sides. Premium product photography, realistic glass refraction, warm side key light, thin lime rim light, cool edge light, no floor glare. Bottle shape and label stay identical; plain label without any words or logos. Seamless loop that ends exactly on the reference frame.

Frase 9:16: The bottle fills the middle of the vertical frame with dark space above and below.
```

#### V06 · Capítulo 03 «Centro de datos e IA» · `VIDEO_CAP3_URL`
```text
MODELO: Kling 3.0 (kling3_0) · 8 s · 720p · 16:9 + 9:16 · sin audio
ESCENA: centro de datos oscuro, pasillo de racks negros mate que se pierden en perspectiva
SUJETO: luces de estado diminutas en los racks; flujos de datos como líneas de luz finas que recorren el suelo y convergen en un núcleo luminoso al fondo
CÁMARA: dolly hacia adelante casi imperceptible; los flujos se mueven y la cámara apenas avanza
ESTILO: arquitectura cinematográfica minimalista, niebla volumétrica tenue
PALETA: racks #111316 · fondo #0A0B0D · luces de estado #A0A5B0 · flujos y núcleo #C8FF00
ILUMINACIÓN: clave baja, niebla atravesada por la luz del núcleo
DURACIÓN / FORMATO: 8 s · 16:9 y 9:16
LOOP: inicio = final; flujo de datos continuo
EVITAR: pantallas con texto o código, logos de marcas de servidores, personas, luces azules saturadas, flashes, cortes

PROMPT 16:9:
A dark data centre corridor of matte black server racks (#111316) receding in perspective against a near-black background (#0A0B0D). Tiny cool grey (#A0A5B0) status lights blink softly and slowly on the racks. Thin lines of lime-green light (#C8FF00) flow along the floor and converge into a soft glowing core at the far end. The vanishing point sits in the right third of the frame and the left side stays in deep shadow. Almost imperceptible forward dolly while the light flows keep moving. Minimal cinematic architecture, faint volumetric haze lit by the core, low-key lighting. One continuous take, seamless loop, clean frame without screens, text, code or logos.

Frase 9:16: The vanishing point sits in the upper centre of the vertical frame and the lower half stays in deep shadow.
```

#### V07 · Capítulo 04 «Del insight a la estrategia» · `VIDEO_CAP4_URL`
```text
MODELO: Kling 3.0 (kling3_0) · 8 s · 720p · 16:9 + 9:16 · sin audio
ESCENA: plano oscuro infinito visto en ángulo de 60°
SUJETO: constelación de nodos unidos por rutas finas; algunas rutas se encienden en lima una tras otra y convergen en un nodo; el resto se atenúa; después todo vuelve al estado inicial
CÁMARA: órbita lenta de 8° y vuelta al encuadre inicial
ESTILO: mapa de decisiones abstracto y elegante, líneas muy finas, profundidad de campo suave
PALETA: fondo #0A0B0D · nodos y rutas #A0A5B0 · rutas activas y nodo final #C8FF00
ILUMINACIÓN: solo la luz propia de las rutas
DURACIÓN / FORMATO: 8 s · 16:9 y 9:16
LOOP: inicio = final (todas las rutas en reposo)
EVITAR: mapas geográficos reales, texto, etiquetas, números, flechas de interfaz, flashes, cortes

PROMPT 16:9:
An abstract decision map on an infinite near-black plane (#0A0B0D), seen at a 60-degree angle: a constellation of small nodes linked by very thin routes in cool grey (#A0A5B0). Routes light up in lime green (#C8FF00) one after another and converge on a single node while the others dim, then everything eases back to the resting state. The map spreads across the right two thirds of the frame and the left third stays dark. Slow 8-degree orbit that returns to the opening framing. Elegant, minimal, very fine lines, soft depth of field, lit only by the glow of the routes. One continuous take, seamless loop, clean frame without text, labels, numbers or real geography.

Frase 9:16: The map spreads across the upper two thirds of the vertical frame and the bottom third stays dark.
```

#### V08 · Capítulo 05 «Consumidor y experiencia» · `VIDEO_CAP5_URL`
```text
MODELO: Seedance 2.5 (seedance_2_5) · 8 s · 720p · 16:9 + 9:16 · sin audio
ESCENA: vacío oscuro con partículas en suspensión
SUJETO: las partículas convergen hasta formar una silueta humana anónima a contraluz (cabeza y hombros, sin rasgos faciales) con un brillo lima cálido a la altura del pecho; luego se disuelven otra vez en partículas
CÁMARA: acercamiento muy lento y vuelta al encuadre inicial
ESTILO: cinematográfico, cálido y humano, sin aspecto de ciencia ficción
PALETA: fondo #0A0B0D · partículas #F2F3F0 y #A0A5B0 · brillo #C8FF00
ILUMINACIÓN: contraluz suave; el rostro queda siempre en sombra
DURACIÓN / FORMATO: 8 s · 16:9 y 9:16
LOOP: inicio = final (partículas dispersas)
EVITAR: rostros reconocibles, ojos, personas reales, texto, logos, estética robótica o de vigilancia, flashes, cortes

PROMPT 16:9:
Drifting particles in a near-black void (#0A0B0D) slowly gather into an anonymous back-lit human silhouette of head and shoulders, with no facial features and the face always in shadow. A warm lime-green glow (#C8FF00) pulses gently at chest height while off-white (#F2F3F0) and cool grey (#A0A5B0) particles outline the figure, then the silhouette dissolves back into drifting particles. The figure sits in the right third of the frame and the left two thirds stay dark. Very slow push-in that returns to the opening framing. Cinematic, warm and human rather than robotic, soft back light. One continuous take, seamless loop starting and ending on scattered particles, clean frame without text or logos.

Frase 9:16: The figure sits in the upper half of the vertical frame and the lower half stays dark.
```

Para usar un clip:
1. En la sección, ve a Estilo › Fondo › Tipo: Video y pega la URL del MP4.
2. Desactiva el Motion Effect del fondo, porque Elementor no lo combina con video.

## 6 · Lo que no es nativo y cómo se resolvió

| Elemento del sitio original | Resolución en esta versión |
|---|---|
| Escena 3D de partículas (Three.js) | Capturas de la propia escena como fondos con parallax y zoom de scroll |
| Demo «Así mira tu cliente» guiada por el scroll | Foto y mapa de calor alineados; el mapa de calor aparece con el scroll |
| Comparador de la botella que se arrastra | Mismo efecto: el mapa de calor aparece con el scroll |
| Monitores de señal «en vivo» | Tarjetas estáticas con el mismo texto |
| Gráfico «Declarado», preloader | Se omiten |
| Formulario con FormSubmit | Formulario de Elementor Pro (acción Email a cristiangm3005@gmail.com); se recomienda un plugin SMTP |
| Menú con panel animado | Widget Toggle nativo en tablet y móvil |
| prefers-reduced-motion | Custom CSS de la página: sin entradas ni parallax, el mapa de calor queda visible |

Si quieres conservar la escena 3D y las demos interactivas tal cual, sigue disponible la versión con widgets HTML:
`elementor-json/neurogenomic-inicio.json`.
