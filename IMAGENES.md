# Imágenes · Neurogenomic 2026

## Incluidas (ya en `img/`)

Recortes de las piezas de campaña de Neurogenomic, sin el texto incrustado. Se sirven en AVIF con respaldo WebP.

| Archivo | Tamaño | Dónde se usa |
|---|---|---|
| `ref-can-570.avif / .webp` | 570×1590 | Sección «Tu packaging tiene una mirada para ganar» y Servicio 01 · Branding |
| `ref-bottle-520.avif / .webp` | 520×1350 | Servicio 04 · Marketing Digital (página Servicios) |
| `ng-pouch-960/1600/2400` | 2400×1500 | «Así mira tu cliente» (bolsa de café kraft, render fotográfico) y monitor C·01 de Tecnología |
| `ng-box-a/b/c-600/1200` | 1200×1520 | Caso: tres versiones de packaging (render fotográfico) |
| `ng-phone-600/920` | 920×1070 | CTA final: tienda ficticia en un teléfono (render fotográfico) |
| `seq/f_000…079.webp` | 80 cuadros | «Así mira tu cliente»: demo scroll-driven |

Los renders `ng-*` se generan con Blender/Cycles a partir de `render/`. Las capas de eye tracking se ubican con las coordenadas proyectadas que guarda `src/data/*.json`: si cambias un render, vuelve a copiar su JSON.

Business Intelligence, E-commerce, SEO y Software usan ilustraciones dibujadas en SVG con mapa de calor térmico pixelado (no necesitan archivo).

## Opcionales (para subir la resolución o reemplazar ilustraciones)

Los originales miden entre 1080 y 1500 px. Para pantallas grandes conviene regenerarlos a ≥ 2000 px de alto con el mismo estilo:
negro puro, un solo foco, objeto hiperrealista y heatmap térmico pixelado (lima → amarillo → naranja → rojo). Prompts sugeridos:

| Uso | Prompt |
|---|---|
| ecommerce-checkout (4:5) | Close-up of a hand holding a smartphone showing a minimal checkout screen, tiny volt-green eye-tracking fixation dots over the pay button, dark studio, single green rim light, hyper-realistic, editorial tech campaign |
| bi-dashboard (16:9) | Executive in a dark glass room looking at a holographic dashboard of biometric data lines, reflections on glass, volt-green accent light, cinematic, hyper-realistic |
| seo-search (4:5) | Dark desk, a single monitor showing an abstract search results page with one AI-generated answer card highlighted by a thin volt-green outline, reflections on glossy desk, cinematic low-key, hyper-realistic, no logos |
| software-build (4:5) | Developer's hands on a mechanical keyboard, code reflected on glasses lens in the foreground, dark interior, green monitor glow, shallow depth of field, hyper-realistic, editorial tech campaign |
| hero-eye (16:9 (desktop) + 9:16 (móvil: hero-eye-portrait)) | Macro photograph of a human eye, extreme close-up, iris in sharp focus, a thin volt-green (#C8F542) laser crosshair reflected on the cornea, dark charcoal background, cinematic low-key lighting, hyper-realistic, 8K, shallow depth of field, editorial tech campaign |

| OG | `og-neurogenomic.jpg` 1200×630 · Composición del hero (ojo macro) con el logotipo Neurogenomic, para compartir en redes |
