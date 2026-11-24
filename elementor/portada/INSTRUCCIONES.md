# Portada · textos nuevos (widget HTML de Elementor)

- `widget-html-nuevo.html`: código completo para pegar en el widget **HTML** de la portada.
- `widget-html-original-respaldo.html`: el código que hay hoy en la web (copia de respaldo).

## Cómo aplicarlo
1. WordPress → Páginas → Portada → **Editar con Elementor**.
2. Haz clic en el único widget **HTML** de la página (contiene toda la animación 3D).
3. Selecciona todo el contenido del campo *Código HTML* (Ctrl+A) y bórralo.
4. Pega el contenido completo de `widget-html-nuevo.html`.
5. **Actualizar**. Si usas caché (LiteSpeed, WP Rocket, Cloudflare…), púrgala.

Para volver atrás, pega `widget-html-original-respaldo.html` de la misma forma.

## Qué cambia
- Hero: nuevo titular y subtítulo, 3 frases que rotan (packaging / campaña / web) y CTA «Agenda tu diagnóstico».
- Capítulos 01–05 y el bloque de contacto: títulos y textos nuevos. Se eliminaron las listas abstractas y las etiquetas que se repetían.
- Animación 3D: se quitaron los paneles «Qué muestra» y las etiquetas de biología (Soma, Sinapsis…). Las etiquetas ahora dicen Mirada / Rostro / Piel y Packaging / Campaña / Web / Marca.
- Formulario: el botón dice «Enviar» y el asunto del correo, «Solicitud de diagnóstico».
- La animación, los colores, el formulario y el botón «Pausar animación» siguen funcionando igual. Las frases que rotan también se detienen con la pausa.

## Ajustes responsive (versión 2)
Probado en 320×568, 360×640, 360×740, 390×844, 414×896, 768×1024, 1024×768, 1280×720, 1440×900, 1920×1080 y celular en horizontal (667×375, 844×390). Ningún elemento queda encima de otro.
- Celular en horizontal: texto a la izquierda y figura a la derecha, solo con lo esencial. Antes el texto quedaba encima de la figura.
- Etiquetas de las figuras 3D: ya no se pisan entre ellas, no salen de la pantalla y no entran en la columna de texto.
- Figura 3D en celular: más pequeña, para que no toque el texto.
- Bolsa (demo eye tracking):
  - La tarjeta toma su tamaño de la altura de la pantalla. En celular es más grande y el título va en una sola línea.
  - Las etiquetas (Marca 21%, Zona ciega…) siempre quedan dentro de la imagen y sin chocar entre sí.
  - En escritorio ya no toca el botón «Pausar animación».
- Notebooks de poca altura (720–900 px): textos y listas más compactos, sin tocar el indicador de capítulo ni el botón de pausa.

## Lista de servicios (versión 3)
- La sección 04 muestra los 6 servicios con nombre y descripción en todos los dispositivos. Antes, en celular solo aparecían como etiquetas y en pantallas bajas no aparecían.
- Descripciones (basadas en la página /servicios/):
  - Branding: Marca probada con personas antes de lanzarla
  - Business Intelligence: Estudios y datos de venta en un solo tablero
  - E-commerce: Menos fricción en el camino a la compra
  - Marketing digital: Piezas probadas antes de invertir en medios
  - SEO: Visible en buscadores y en respuestas de IA
  - Desarrollo web: Sitios y aplicaciones con IA integrada
- Celular y tablet: lista en 2 columnas. Escritorio: lista en filas con código S·01–S·06.

## Capítulo 02 «Qué medimos»: lentes de eye tracking (versión 4)
- La animación de corrientes de señales se reemplazó por unos lentes de eye tracking en vista explosionada, hechos con las mismas partículas que el resto de la escena (no usa imágenes).
- Marco y patillas en verde lima para que se distingan sobre el fondo oscuro.
- Piezas separadas: lente, placa de circuito, batería (ámbar) y tapa de la carcasa.
- Cable flexible naranja por el que viajan pulsos de señal en lima.
- Etiquetas: «Cámara ocular · mirada», «Cámara de escena» y «Sensor de piel». En celular son más cortas: «Mirada», «Escena» y «Piel».
- Los lentes giran levemente y se detienen con «Pausar animación».

## Neurona más grande y lentes que se explican solos (versión 5)
- Capítulo 01: la neurona ocupa más espacio (hasta 80 % del alto) sin invadir la columna de texto. En pantallas de poca altura mantiene el tamaño anterior.
- Capítulo 02: una persona con los lentes, y cada medición se ve en acción:
  - Mirada: los ojos detrás de los cristales se mueven; un rayo lima sale de ellos hasta un punto de fijación que se desplaza.
  - Rostro: una cámara facial frente a la cara, con su campo de visión; una línea de escaneo recorre el rostro y enciende los puntos faciales (cejas, nariz, pómulos, boca, mentón).
  - Piel: junto al sensor de la patilla corre una curva de respuesta electrodérmica.
- Etiquetas: «Mirada · eye tracking», «Rostro · cámara facial» y «Piel · sensor EDA». En celular: «Mirada», «Rostro» y «Piel».
