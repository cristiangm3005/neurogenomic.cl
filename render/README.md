# Renders fotográficos (Blender · Cycles)

Escenas que generan las imágenes `img/ng-*`. Cada escena guarda también las posiciones proyectadas (0–1 sobre la foto) de cada zona del packaging, para que fijaciones, heatmap y zonas ciegas queden calibrados sobre la imagen.

| Script | Imagen | Datos |
|---|---|---|
| `pouch_tex.py` → `pouch_scene.py` | Bolsa de café kraft «MESTA · HUILA» (2400×1500) | `<salida>.json` → copiar a `src/data/pouch.json` |
| `bottle_scene.py` | Botella de bebida genérica, sin marca ni textos (1200×1520) | `<salida>.json` → copiar a `src/data/bottle.json` (zonas + silueta para recortar el mapa de calor) |
| `box_scene.py` | Tres cajas «BRISA» A/B/C (1200×1520) | `boxes.json` → copiar a `src/data/boxes.json` (sin `_box`) |
| `tracker_scene.py` | Barra de eye tracking bajo un monitor (2520×1080) | — |

## Cómo regenerar

```bash
python3.11 -m venv .venv && .venv/bin/pip install bpy==5.0.1 pillow
npm i @fontsource/anton @fontsource/space-grotesk @fontsource/ibm-plex-mono   # fuentes de la etiqueta
.venv/bin/python pouch_tex.py
.venv/bin/python pouch_scene.py 2400 1500 128 pouch.png
.venv/bin/python box_scene.py 1200 1520 96 .
.venv/bin/python bottle_scene.py 1200 1520 128 bottle.png
.venv/bin/python tracker_scene.py 2520 1080 96 tracker.png
```

Después exporta cada PNG a AVIF y WebP con los anchos que usa `build.py` (`REAL`). Por ejemplo, `ng-pouch-960/1600/2400.avif|webp`.
Las marcas MESTA y BRISA son ficticias.
