# MetalGenomic · importar en Elementor Pro

Archivo: `metalgenomic-landing-elementor-pro.json` (plantilla de página, ~228 KB).

## Importar
1. WordPress → Plantillas → Plantillas guardadas → **Importar plantillas** → subir el `.json`.
2. Páginas → Añadir nueva → «Editar con Elementor» → ícono de carpeta → pestaña «Mis plantillas» → **Insertar** «MetalGenomic · Landing 3D».
3. En la configuración de la página (engranaje): **Diseño de página = Elementor Canvas** (ya viene en la plantilla; verificar).
4. Publicar y revisar en la página publicada (la vista previa del editor carga la escena 3D completa y puede ir lenta).

## Requisitos
- El usuario que guarda la página debe ser **Administrador** (capacidad `unfiltered_html`); si no, WordPress elimina los `<script>` y la escena 3D no carga.
- El sitio debe poder cargar recursos de `cdn.jsdelivr.net` (three.js), `cdnjs.cloudflare.com` (GSAP) y Google Fonts.
- No activar en esta página optimizadores que difieran o combinen JavaScript (WP Rocket, Autoptimize, LiteSpeed «Delay JS»): excluirla, porque rompen el `importmap` y el módulo 3D.

## SEO (configurar en el plugin de SEO, no viene en el JSON)
- Título: «MetalGenomic | Biolixiviación, genómica e IA para minería en Chile»
- Meta descripción: «Biolixiviación, exploración geoespacial, mantenimiento predictivo y gemelo digital para la mediana minería. Diagnóstico de tu operación en hasta 4 semanas.»
- Los datos estructurados (schema.org) sí van dentro de la plantilla.

## Editar textos
Todo está en un único widget **HTML**: los textos se editan ahí, buscando la frase. Mantener las clases, IDs y atributos `data-*`, porque la animación depende de ellos.
