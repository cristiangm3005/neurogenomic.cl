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
