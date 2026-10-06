# MetalGenomic · assets pendientes y datos a validar

## Cómo reemplazar las ilustraciones por renders reales

1. Copia el archivo en `assets/img/render/` con el nombre indicado.
2. En `assets/js/main.js`, completa la ruta en `RENDERS` (arriba del archivo):
   ```js
   var RENDERS = {
     truckSide: 'assets/img/render/truck-side.webp',
     truckTop:  'assets/img/render/truck-top.webp'
   };
   ```
   La ilustración SVG se oculta sola cuando el render carga. Las animaciones (avance, rebote, giro en la carretera) siguen funcionando sobre el render.
3. Para las fotos de las escalas, reemplaza el `<picture>` de la capa correspondiente en `index.html` (mismos tamaños: 800 px y 1600 px, en AVIF y WebP).

Estilo común para todos los prompts (pegar al inicio, siempre igual):
> Photorealistic, warm late-afternoon Atacama desert light, fine dust in the air, rock textures, copper / oxide / teal color grade, cinematic, 8K, no logos, no text, no brand marks.

| # | Archivo | Uso en la página | Prompt |
|---|---|---|---|
| 1 | `assets/img/render/truck-side.webp` (1600×900, fondo transparente) | Hero y Soluciones: camión que carga y avanza | Photorealistic 3D render of a large mining haul truck (ultra-class, 300-ton type), side view facing right, loaded with copper ore, isolated on transparent background, soft contact shadow, warm desert light, no logos |
| 2 | `assets/img/render/truck-top.webp` (1200×660, transparente) | Método: camión en vista cenital sobre la carretera | Same mining haul truck, exact top-down orthographic view facing right, dump body full of copper ore, isolated on transparent background, soft drop shadow, no logos |
| 3 | `assets/img/render/shovel-side.webp` (1600×1150, transparente) | Hero: pala hidráulica (hoy SVG) | Photorealistic hydraulic front shovel loading ore, side view facing right, bucket raised and dumping, isolated, transparent background, dust particles, no logos |
| 4 | `assets/img/scale-plant-{800,1600}.{avif,webp}` | Escalas · Planta 2 km (hoy usa la foto del rajo) | Aerial drone photo of copper heap leaching pads with drip irrigation and turquoise PLS ponds, Atacama desert, top-down |
| 5 | `assets/img/scale-equipment-…` (opcional, ya existe una foto) | Escalas · Equipo 10 m | Industrial SAG mill inside a concentrator plant, cinematic lighting, sensors highlighted, dark moody atmosphere |
| 6 | `assets/img/scale-microbe-{800,1600}.{avif,webp}` | Escalas · Microbio 1 µm (hoy foto de mineral + bacterias en canvas) | Colorized scanning electron microscopy of Acidithiobacillus ferrooxidans bacteria on a chalcopyrite crystal surface, copper and teal tones, extreme macro |
| 7 | `assets/img/dna-poster.webp` (opcional) | Genómica: imagen fija para móviles muy lentos | Glowing 3D DNA double helix made of copper and teal particles, black background |
| 8 | Ya existe (`cathode-*`) | Cátodo | Photorealistic stacked copper cathode sheets, specular highlights, dark background, cinematic |
| 9 | `assets/img/seq/truck-000…089.webp` (opcional) | Secuencia de 90 cuadros del camión (ruedas y avance) | Mismo render del punto 1 exportado como turntable/avance de 90 cuadros |
| 10 | `assets/img/og-1200x630.jpg` | Vista previa al compartir (Open Graph) | Composición del hero con el camión cargado y el titular |

Además: fotos reales del equipo, del laboratorio y de pilotos (el plan del sitio las pone por sobre cualquier imagen generada), y el logo final en SVG.

## Textos y datos marcados para validar

Hoy aparecen en la página con la etiqueta amarilla **Dato a validar**. Hay que confirmarlos o reemplazarlos antes de publicar:

- **3** consorcios candidatos evaluados por mineral.
- **21 días** de la muestra al reporte genómico.
- **100 %** microorganismos nativos, sin cepas importadas.

Otros datos que hay que confirmar con MetalGenomic:

- Correo de contacto `contacto@metalgenomic.cl` (formulario, pie y schema.org).
- Dominio `https://metalgenomic.cl/` (canonical y Open Graph).
- Ciudad en el pie y en schema.org: Copiapó, Atacama.
- Que la integración con SCADA, PI System, SAP PM y GIS está disponible hoy.
- Que el monitoreo genómico ajusta riego, pH y aireación (bloque 03 de Genómica).
- Plazos: diagnóstico de hasta 4 semanas y piloto de 1 a 3 meses.
