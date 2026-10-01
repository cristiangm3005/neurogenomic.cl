# Imágenes necesarias · Neurogenomic 2026

Todas en AVIF + WebP, nítidas (sin blur ni velos), color grading hacia negros profundos con toques de verde volt `#C8F542`.
Exporta cada imagen en **768 / 1280 / 1920 / 2560 px** de ancho con el patrón `nombre-ANCHO.avif` y `nombre-ANCHO.webp`
(p. ej. `hero-eye-1920.avif`). Las variantes `-portrait` (9:16) solo necesitan 768 y 1280.

Mientras una imagen no exista, el sitio muestra un placeholder técnico con el nombre del archivo (no una imagen rota).

| # | Archivo base | Proporción | Dónde se usa | Prompt de generación |
|---|---|---|---|---|
| 01 | `hero-eye` | 16:9 (desktop) + 9:16 (móvil: hero-eye-portrait) | S1 Hero | Macro photograph of a human eye, extreme close-up, iris in sharp focus, a thin volt-green (#C8F542) laser crosshair reflected on the cornea, dark charcoal background, cinematic low-key lighting, hyper-realistic, 8K, shallow depth of field, editorial tech campaign |
| 02 | `branding-package` | 4:5 | S5 Servicio 01 Branding | Hand holding a premium unbranded product package under a studio spotlight, faint eye-tracking heatmap projected onto the box in green and yellow, black background, hyper-realistic product photography |
| 03 | `bi-dashboard` | 16:9 | S5 Servicio 02 BI | Executive in a dark glass room looking at a holographic dashboard of biometric data lines, reflections on glass, volt-green accent light, cinematic, hyper-realistic |
| 04 | `facial-coding` | 4:5 | S4 panel C·02 Facial coding | Close-up portrait of a person's face with subtle micro-expression, precise thin white facial landmark points overlaid, dark studio, Rembrandt lighting, hyper-realistic skin texture |
| 05 | `gsr-sensor` | 1:1 | S4 panel C·03 GSR | Fingertips resting on minimal biometric sensor electrodes with thin cables, black matte surface, single green rim light, macro photography, hyper-realistic |
| 06 | `lab-session` | 21:9 | S6 Método + cabecera Tecnología | Modern neuromarketing lab, participant seated in front of a monitor with a slim eye tracker bar, operator in soft focus behind, dark interior, green monitor glow, documentary photography, hyper-realistic |
| 07 | `ethics-fingerprint` | 16:9 | S9 Ética | Abstract macro of a fingerprint pattern dissolving into encrypted data particles, black background, volt-green highlights, hyper-realistic |
| 08 | `cta-eye-contracted` | 16:9 (desktop) + 9:16 (móvil: cta-eye-contracted-portrait) | S10 CTA final (cierre narrativo) *(variante del hero, pupila contraída)* | Same framing as the hero: macro photograph of the same human eye, extreme close-up, pupil strongly contracted (miosis), iris in sharp focus, thin volt-green (#C8F542) crosshair reflected on the cornea, dark charcoal background, cinematic low-key lighting, hyper-realistic, 8K, editorial tech campaign |
| 09 | `ecommerce-checkout` | 4:5 | S5 Servicio 03 E-commerce *(añadida: el brief no traía prompt para este servicio)* | Close-up of a hand holding a smartphone showing a minimal checkout screen, tiny volt-green eye-tracking fixation dots over the pay button, dark studio, single green rim light, hyper-realistic, editorial tech campaign |
| 10 | `marketing-pretest` | 4:5 | S5 Servicio 04 Marketing *(añadida: el brief no traía prompt para este servicio)* | Person in a dark room watching an ad on a screen, the ad reflected in their eyes, slim eye tracker bar under the screen, volt-green accent light, cinematic low-key, hyper-realistic, documentary style |
| 11 | `seo-search` | 4:5 | S5 Servicio 05 SEO *(añadida: el brief no traía prompt para este servicio)* | Dark desk, a single monitor showing an abstract search results page with one AI-generated answer card highlighted by a thin volt-green outline, reflections on glossy desk, cinematic low-key, hyper-realistic, no logos |
| 12 | `software-build` | 4:5 | S5 Servicio 06 Software *(añadida: el brief no traía prompt para este servicio)* | Developer's hands on a mechanical keyboard, code reflected on glasses lens in the foreground, dark interior, green monitor glow, shallow depth of field, hyper-realistic, editorial tech campaign |

| OG | `og-neurogenomic.jpg` | 1200×630 | Open Graph / redes | Composición del hero (ojo macro) con el logotipo Neurogenomic, para compartir en redes |

Para la variante móvil del hero y del CTA, genera el mismo prompt en **9:16** y nómbralo `hero-eye-portrait` / `cta-eye-contracted-portrait`.

Ajusta la variable CSS `--ng-pupil` (por defecto `64% 46%`) en `.ng-hero__media img` y `.ng-cta__media img` para que el zoom de scroll apunte exactamente a la pupila de tu foto.
