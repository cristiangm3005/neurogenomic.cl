# Crítica de animación · Inicio actual → propuesta Landing 3D

Revisé la página de Inicio actual (`index.html`) recorriéndola entera en 29 capturas a 1440×900 y leyendo su código de animación: `src/core/core.js`, `src/sections/x-story.html` y cada sección.

## 1. Diagnóstico

**Veredicto:** la escena 3D de partículas es lo mejor que tiene el sitio, pero hoy funciona como papel tapiz: se enciende y se apaga entre secciones. La página habla dos idiomas visuales y usa unos quince efectos de movimiento que no se relacionan entre sí. El problema no es la falta de animación, sino la falta de una sola historia.

| # | Gravedad | Problema | Evidencia | Consecuencia |
|---|---|---|---|---|
| 1 | ALTA | **La historia se corta** | Entre el capítulo 02 y el 03 hay unos 6.000 px de secciones opacas (demo, packaging, «Lo que no se dice»). Entre el 03 y el 04 hay otros 5.000 px (tecnología, ética). | La transformación neurona → señales → servidores ocurre detrás de los paneles. El usuario ve la figura «teletransportarse», justo lo que el 3D debía contar. |
| 2 | ALTA | **Dos paletas** | El 3D usa azul, violeta y cian (`rgba(40,70,220)`, etiquetas `#6FE3FF`). El resto del sitio es negro + lima. | Los capítulos parecen de otra marca y el lima pierde fuerza. |
| 3 | ALTA | **Hero doble** | El masthead NEUROGENOMIC, el menú, dos filas de anclas y 9 chips ocupan unos 430 px antes del H1 «El marketing digital cambió». | Dos titulares compiten y la escena 3D arranca bajo el pliegue. |
| 4 | ALTA | **Texto y 3D no están sincronizados** | El texto entra por IntersectionObserver (margen −18 %). La figura se forma con otra fórmula (`(vh·1.05 − top)/(vh·0.6)`). | El titular llega con la figura a medio armar, o después. No hay un instante compartido. |
| 5 | MEDIA | **Demasiados vocabularios** | Palabras que suben, fade-up de 28 px, chips con rebote `back.out(1.6)`, tarjetas que giran 38°, trazos SVG, máquina de escribir con tachado, contadores, marquesina de 60 s, inclinación con scrub, línea de ECG, ken burns de 22 s, botón con degradado infinito, parpadeos, botones magnéticos e inercia Lenis de 1,15 s. | No hay personalidad de movimiento. El rebote, además, choca con una marca que vende evidencia científica. |
| 6 | MEDIA | **Tarjetas de vidrio y huecos** | `backdrop-filter: blur(12px)` sobre un WebGL a pantalla completa. Capítulos de 150vh con tarjeta sticky. | Costo de GPU en cada cuadro, una caja que tapa la figura y pantallas casi vacías (capturas 04, 13 y 19). |
| 7 | MEDIA | **Morph sin dirección** | La transición suma ruido aleatorio (`sin(aD.x·40)·0.6`). | Las partículas se agitan en vez de viajar. No se lee como «una cosa que se convierte en otra». |
| 8 | MEDIA | **Inercia sobre inercia** | Lenis (1,15 s) más un suavizado propio de la escena más 10–38 ScrollTriggers con scrub. | El scroll se siente flotante y la figura llega tarde respecto del dedo. |
| 9 | BAJA | **Etiquetas en bloque** | Todas las etiquetas 3D se encienden a la vez (0,4 s). | Pierden jerarquía. |
| 10 | BAJA | **Bucles decorativos permanentes** | Botón con degradado infinito, parpadeos, ken burns. | Compiten por la atención con la figura. |

**Lo que funciona y se conserva:** la calidad de las partículas y su nitidez en celular, la tipografía (Big Shoulders, Schibsted Grotesk y Martian Mono), el negro + lima, el respeto a `prefers-reduced-motion`, el botón para pausar y el respaldo sin WebGL.

## 2. Propuesta: Landing 3D «De la mirada a la decisión»

Archivo: `landing-3d/neurogenomic-landing-3d.html`, con su plantilla `neurogenomic-landing-3d-elementor.json`. Tiene el mismo estilo y diseño que el sitio, **no lleva menú** y abre solo con **NEUROGENOMIC en grande**.

### Concepto
Un solo cuerpo de partículas que nunca desaparece cambia de forma siete veces. Cada forma es un capítulo:

`NEUROGENOMIC` → **neurona** → **señales** (atención, emoción, activación → mapa de atención) → **IA** (esfera de datos) → **seis servicios** (seis nodos con su nombre) → **persona** → **fijación** (la retícula de eye tracking donde se toma la decisión, detrás del formulario).

La marca se deshace en la neurona y la historia termina en un punto de fijación. Empieza en la marca y termina en la decisión del cliente.

### Sistema de movimiento (4 reglas para todo el sitio)
1. **Una curva.** Todas las entradas usan `cubic-bezier(.16,1,.3,1)` (`--lx-out`) durante 0,9–1 s con un escalonado de 70–80 ms. Las salidas usan la misma curva en 0,4 s. Sin rebotes.
2. **Un gesto de llegada.** Cuando la figura termina de formarse, en el mismo cuadro:
   - una onda lima la recorre;
   - se dibuja la línea de medición bajo el antetítulo;
   - el titular sube línea por línea;
   - las etiquetas aparecen escalonadas.

   El texto está atado al estado de la figura, no a un observador aparte.
3. **Un morph con dirección.** La nueva forma se arma de izquierda a derecha, como un escáner, mientras las partículas trazan un arco hacia la cámara. Lo conduce el scroll y es reversible: al subir, se deshace.
4. **La escena siempre visible.** No hay paneles opacos. El texto va sobre un degradado lateral y la figura se ubica sola, calculado en píxeles, en el espacio libre (al costado en computador, arriba en celular y tablet vertical) y escalada para que quepa entera.

### Hero
- Sin menú. Durante 1,9 s las partículas llegan desde el fondo y escriben NEUROGENOMIC de izquierda a derecha. Es el único momento de «deleite» y ocurre una vez.
- El texto HTML queda como contorno nítido y las partículas rellenan las letras. En pantallas sin WebGL, la marca se ve sólida.
- Al bajar, las letras se aflojan y se convierten en la neurona.
- En celular la marca va en dos líneas (NEURO / GENOMIC) para ocupar el ancho.

### Lo que se quitó y por qué
- **GSAP, ScrollTrigger y Lenis:** se reemplazan por scroll nativo, un solo bucle rAF y transiciones CSS reversibles. La escena responde al dedo sin retraso.
- **Preloader, tarjetas de vidrio, botones magnéticos, botón con degradado infinito, rebotes, marquesina y tilt:** eran ruido frente a la figura.
- **Capítulos de 150vh con huecos:** cada capítulo mide 210vh con su cuadro fijo, así siempre hay figura y texto en pantalla.

### Rendimiento y accesibilidad
- Un solo `requestAnimationFrame`, que se detiene con la pestaña oculta o con la animación pausada.
- Partículas: 10.000 en celular, 14.000 en tablet y 19.000 en escritorio. Densidad de píxeles limitada a 2× en pantallas táctiles y 1,75× en escritorio.
- Botón «Pausar animación», que recuerda la preferencia.
- `prefers-reduced-motion`: sin intro, sin onda, sin giro y sin desplazamientos; el texto solo aparece con fundido.
- Sin WebGL: marca sólida y atmósfera en CSS. Todo el texto es HTML real: un H1 y un H2 por capítulo.
- Formulario por FormSubmit (correo + consentimiento + honeypot), igual que el sitio.

### Contenido
Usa solo textos que ya existían en el sitio: capítulos, servicios, método, ética y CTA. No hay cifras, clientes ni testimonios nuevos.

La demo, el packaging, el caso y el centro de confianza completo siguen en las páginas internas. La landing enlaza a `/contacto/` y `/privacidad/`.

## 3. Pruebas realizadas
- Chromium a 1440×900, 1024×768 (iPad horizontal), 768×1024 (iPad vertical) y 390×844 (celular): 0 errores, sin scroll horizontal y la figura completa en cada capítulo.
- Sin WebGL y con movimiento reducido: texto completo y legible.
- Importada en WordPress 7.1.2 + Elementor 3.33 (tema Hello Elementor) con *Elementor Canvas*: se ve igual que el HTML suelto.

## 4. Cómo subirla a Elementor
1. Crea una página nueva (por ejemplo *Landing*) y pulsa **Editar con Elementor**.
2. Haz clic en el ícono de carpeta, luego en **Mis plantillas**, luego en el ícono de subir, y elige `neurogenomic-landing-3d-elementor.json`.
3. Pulsa **Insertar** y acepta los ajustes de página (aplica *Elementor Canvas* y el fondo negro).
4. Pulsa **Publicar**. No hace falta subir imágenes ni fuentes: todo va dentro del archivo.

Para cambiar el código, edita `landing-3d/src/landing.html` y ejecuta `python3 landing-3d/build.py`.
