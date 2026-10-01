# Neurogenomic · Sitio web con scroll narrativo

Carpeta lista para publicar. Abre `index.html` con doble clic o súbela tal cual a cualquier hosting estático.

```
neurogenomic-web/
├── index.html            ← página principal (HTML final)
├── privacidad.html       ← borrador con marcadores, requiere revisión legal
├── cookies.html          ← borrador con marcadores
├── terminos.html         ← borrador con marcadores
├── css/styles.css        ← CSS final (tokens, componentes, secciones, movimiento)
├── css/fonts.css         ← fuentes incrustadas (funcionan sin servidor)
├── js/main.js            ← JavaScript final (sin librerías)
├── js/demo-data.js       ← coordenadas de la demostración (datos simulados)
├── fonts/                ← archivos .woff2 originales + licencias
├── img/                  ← fotos, renders y 80 cuadros de la demostración
└── DOCUMENTACION.md      ← este documento
```

Peso total aproximado: 2 MB. En la primera carga sin scroll: unos 380 KB (HTML, CSS, fuentes, JS e imagen del hero). Los 80 cuadros de la demo (1,1 MB) se cargan progresivamente solo cuando el visitante se acerca a esa sección.

---

## 1. Diagnóstico de la versión anterior

| # | Problema | Impacto | Qué se hizo |
|---|---|---|---|
| 1 | El titular («Valida antes de lanzar») era correcto, pero no decía **qué** se valida ni el beneficio económico. | Menos claridad en los primeros 5 segundos. | Nuevo H1 orientado a la decisión y a la inversión: «Valida tus decisiones de marketing antes de invertir en producción.» |
| 2 | Los servicios mezclaban técnicas (eye tracking) con áreas (e-commerce) sin explicar qué se mide ni qué se entrega. | El visitante no sabía qué iba a recibir. | 8 servicios con la misma estructura: qué mide, para qué sirve, qué decisión permite y qué entregable recibes. |
| 3 | El CTA aparecía solo en el hero y al final. | Se perdían visitantes «listos» a mitad de página. | CTA repetido después de Servicios y de Método, más un CTA fijo en móvil que se oculta al llegar al formulario. |
| 4 | La demo no mostraba la respuesta galvánica y su etiqueta era breve. | Se veía una sola de las tres técnicas. | Se agrega una curva de respuesta galvánica que se dibuja con el scroll. La etiqueta es la pedida: «Demostración visual. No corresponde a datos de un estudio real.» |
| 5 | El salto entre cuadros dependía directamente del scroll. | Con ruedas de mouse «a pasos» la animación saltaba. | Suavizado con `requestAnimationFrame` (interpolación); se dibuja solo cuando cambia el cuadro. |
| 6 | El caso ilustrativo no separaba hallazgo y decisión. | Se confundía dato con recomendación. | Estructura Desafío → Método → Hallazgo → Decisión, sin cifras. |
| 7 | La sección de ética mencionaba normas sin el aviso pedido. | Riesgo de leerse como cumplimiento automático. | Ocho principios + el aviso legal responsable; la Ley 21.719 se menciona como referencia, no como certificación. |
| 8 | Las fuentes se cargaban desde Google Fonts. | Petición a un tercero y bloqueo potencial del renderizado. | Fuentes servidas localmente, sin peticiones externas. |
| 9 | El formulario no pedía tipo de proyecto ni presupuesto, y no avisaba que usa un servicio externo. | Leads menos calificados y poca transparencia. | Formulario de 7 campos (presupuesto opcional) y aviso explícito sobre FormSubmit. |
| 10 | Faltaban políticas de cookies, de privacidad y términos. | Enlaces legales inexistentes. | Tres páginas en borrador con marcadores `[AGREGAR …]` y `noindex`, para que no haya enlaces rotos. |
| 11 | Schema con `Service` sueltos. | Datos estructurados poco claros. | `Organization` + `ProfessionalService` con catálogo de servicios, sin dirección, teléfono ni reseñas. |

**Lo que se conservó:** la estética oscura con acento lima, la foto del perro con el anillo de fijación, el render fotográfico de la bolsa y su secuencia de 80 cuadros, las cajas del caso, la tabla «qué mide y qué no», las referencias metodológicas y la integración del formulario con el correo.

## 2. Propuesta de valor

> **Neurogenomic mide cómo miran y reaccionan personas reales frente a tu marca, campaña, packaging o sitio web, para que decidas qué mantener, ajustar o descartar antes de invertir en producción.**

- **Para quién:** equipos de marketing, marca, e-commerce, producto y agencias.
- **Problema:** decisiones tomadas por intuición o por comité, con opiniones declaradas que no siempre reflejan el comportamiento.
- **Cómo:** eye tracking, facial coding y respuesta galvánica, más análisis con IA revisado por personas.
- **Resultado:** recomendaciones accionables, separando lo medido de lo interpretado.

Alternativas de titular evaluadas (se implementó la 1):
1. **Valida tus decisiones de marketing antes de invertir en producción.** ← implementada
2. Decide con evidencia antes de producir, imprimir o pautar.
3. Mide cómo miran y reaccionan tus clientes antes de lanzar.
4. Menos supuestos, mejores decisiones de marca y campaña.
5. Valida antes de lanzar.

## 3. Arquitectura de información

| # | Sección (ancla) | Idea principal | Animación |
|---|---|---|---|
| 1 | Hero `#inicio` | Qué hacemos y qué decisión validas | Gradiente que deriva lento, dos líneas de señal que se dibujan, anillo de fijación, parallax sutil de la foto, indicador «Desliza» |
| 2 | Problema `#problema` | Opinión ≠ comportamiento; corregir después cuesta más | Bloques e íconos que entran en cascada |
| 3 | Servicios `#servicios` | 8 servicios: qué mide / para qué / decisión / entregable | Tarjetas con fade-in + slide-up escalonado · CTA |
| 4 | Cómo funciona `#metodo` | 4 etapas | Línea que se llena con el scroll y enciende cada etapa · CTA |
| 5 | Demostración `#demo` | De la opinión a la evidencia medida | **Secuencia de 80 cuadros sincronizada con el scroll**: fijaciones una por una, recorrido, mapa de calor, zonas ciegas y curva de respuesta galvánica |
| 6 | Aplicaciones `#aplicaciones` | 8 aplicaciones: problema + decisión | Grilla que se revela |
| 7 | Caso ilustrativo `#caso` | Packaging A/B/C | Línea de escaneo que recorre cada caja y revela su mapa de calor (antes/después) |
| 8 | Evidencia `#evidencia` | Qué mide cada técnica y qué no | Entrada suave |
| 9 | Ética `#etica` | 8 principios + aviso legal | Entrada suave (intencionalmente sobria) |
| 10 | Contacto `#contacto` | Formulario de diagnóstico | Campos que aparecen en secuencia |

Navegación (6 elementos): Servicios · Método · Aplicaciones · Evidencia · Ética · Contacto, con indicador de sección activa.

**Técnica de la demo:** el contenedor mide 520 vh (420 vh en móvil) y tiene un bloque *sticky* de 100 svh. El progreso del scroll (0 a 1) elige el cuadro entre 80 renders reales. Las capas se dibujan en canvas con la posición del packaging **en ese cuadro**, así que siguen a la bolsa mientras la cámara se mueve. Un solo `requestAnimationFrame` interpola el valor y deja de ejecutarse cuando llega al destino.

## 4. Copy completo

**Hero**
- Etiqueta: Neuromarketing e inteligencia biométrica · Chile
- H1: Valida tus decisiones de marketing antes de invertir en producción.
- Bajada: Medimos cómo miran y reaccionan personas reales frente a tu marca, campaña, packaging o sitio web, para que decidas qué mantener, ajustar o descartar.
- CTA: **Agendar diagnóstico →** · Ver cómo funciona ↓
- Chips: Eye tracking · Facial coding · Respuesta galvánica · Análisis con IA
- Imagen: «Todos miran. Nosotros medimos.»

**01 · El problema** — Lo que la gente dice no siempre muestra lo que hace.
Encuestas y focus groups recogen opiniones. Son útiles, pero las personas no siempre saben —o no logran explicar— qué captó su atención o qué les generó rechazo.
- *Decisiones con incertidumbre:* qué packaging imprimir, qué campaña pautar o qué diseño publicar se decide muchas veces por intuición o por comité.
- *Opinión no es comportamiento:* lo que alguien declara después no siempre coincide con lo que miró o sintió en el momento.
- *Corregir después cuesta más:* si el problema aparece tras el lanzamiento, ya se pagó la producción, la impresión o los medios.

**02 · Servicios** — Ocho formas de medir antes de decidir. Cada servicio responde a una pregunta concreta de tu negocio. Los combinamos según lo que necesites validar.

| Servicio | Qué mide | Para qué sirve | Decisión | Entregable |
|---|---|---|---|---|
| Eye tracking (seguimiento ocular) | Dónde se detiene la mirada, en qué orden y por cuánto tiempo | Saber qué capta atención y qué pasa desapercibido | Qué destacar, mover o quitar | Mapas de calor, recorridos de mirada y métricas por zona |
| Facial coding (codificación de movimientos faciales) | Cambios en la expresión facial, segundo a segundo | Ubicar momentos de reacción expresiva para revisarlos | Qué momento ajustar | Línea de tiempo de expresiones, interpretada junto a otras señales |
| Respuesta galvánica (GSR, conductancia de la piel) | Variaciones en la activación fisiológica | Ver en qué momentos hay más intensidad de reacción | Dónde están los picos de interés o tensión | Curvas de activación sincronizadas con el estímulo |
| Packaging y punto de venta | Visibilidad frente a la competencia y lectura de cada elemento | Comparar versiones antes de imprimir | Qué versión producir y qué ajustar | Comparación entre versiones con recomendaciones |
| Sitios web y e-commerce | Recorrido de lectura, dudas y fricción | Entender por qué se abandona | Qué cambiar primero | Diagnóstico de fricción priorizado |
| Campañas y piezas creativas | Atención a marca y mensaje, reacción y activación | Hacer un pre-test antes de invertir en medios | Qué versión pautar y qué editar | Informe comparativo de piezas |
| Modelamiento con IA | Patrones en datos de sesión, biométricos y declarativos | Procesar volumen y cruzar con tus métricas | Qué hallazgos priorizar | Tableros y modelos documentados, revisados por el equipo |
| Consultoría de marca, producto y experiencia | Parte de los hallazgos y tus objetivos | Traducir evidencia en cambios | Cómo y en qué orden implementar | Plan de acción y acompañamiento |

CTA: ¿Tienes una decisión pendiente? Cuéntanos qué quieres evaluar y te proponemos el método adecuado. **Agendar diagnóstico**

**03 · Cómo funciona** — Cuatro etapas, una decisión informada.
1. *Diagnosticar:* definimos contigo la decisión a validar, los estímulos y el perfil de participantes.
2. *Medir:* registramos mirada, expresión y activación de personas reales mientras ven tus piezas.
3. *Analizar:* cruzamos las señales con lo que declaran los participantes y separamos dato de interpretación.
4. *Recomendar y verificar:* entregamos recomendaciones accionables y, si lo necesitas, medimos de nuevo la versión ajustada.

CTA: Empieza por el diagnóstico. Una conversación para entender tu desafío. Sin compromiso. **Agendar diagnóstico**

**04 · Demostración visual** — De la opinión a la evidencia medida.
- *Qué se mide:* dónde se detiene la mirada, en qué orden y cómo varía la activación.
- *Qué revela:* qué elementos captan atención, cuáles se ignoran y dónde sube la activación.
- *Qué decisión permite:* priorizar, ajustar o descartar elementos antes de producir.
- Fases: Estímulo → Fijaciones → Recorrido → Mapa de calor → Zonas ciegas.
- Etiqueta: **Demostración visual. No corresponde a datos de un estudio real.** La curva lleva el rótulo «simulada».

**05 · Aplicaciones** — Dónde aplicamos la medición.

| Aplicación | Qué problema resolvemos | Qué decisión ayuda a validar |
|---|---|---|
| Packaging | El envase no destaca o no comunica su beneficio | Qué versión imprimir |
| Branding | La identidad no se diferencia de la categoría | Qué propuesta de marca desarrollar |
| Landing pages | La propuesta de valor no se entiende o el botón principal no se ve | Qué estructura y jerarquía publicar |
| E-commerce | Abandono en la ficha de producto o en el checkout | Qué fricción resolver primero |
| Publicidad digital | Anuncios que no muestran la marca a tiempo | Qué creatividad pautar |
| Videos y audiovisual | Momentos de la pieza que pierden atención | Dónde editar o acortar |
| Software y UX | Tareas que confunden a los usuarios | Qué flujo rediseñar |
| Punto de venta | La marca se pierde en la góndola o el exhibidor | Qué exhibición o material usar |

**06 · Caso ilustrativo** — Tres versiones de packaging, una pregunta. *Caso ilustrativo basado en una situación habitual de validación de packaging.*
- *Desafío:* el equipo de marca debe elegir entre tres diseños y no hay acuerdo interno.
- *Método:* participantes del público objetivo ven las versiones en una góndola simulada mientras se registran mirada y expresión.
- *Hallazgo:* en este ejemplo, la versión B concentra la mirada en la marca; en A y C la atención se dispersa o no llega a la marca.
- *Decisión:* avanzar con B y ajustar la jerarquía del nombre del producto antes de imprimir.

**07 · Evidencia y credibilidad** — Qué mide cada técnica y qué no.
Ninguna señal biométrica, por sí sola, explica una decisión de compra. Por eso combinamos técnicas y diferenciamos dato, interpretación, recomendación y resultado.
- Muchas decisiones de consumo ocurren de forma rápida y parcialmente automática.
- La atención es limitada y compite con múltiples estímulos.
- Las señales biométricas pueden complementar los métodos declarativos cuando se interpretan dentro de un diseño de investigación adecuado.
- Tabla de alcance y límites + 6 referencias metodológicas (ver punto 5).
- Cómo entregamos resultados: dato medido → interpretación → recomendación. El resultado de negocio se verifica después, con tus propias métricas; no lo garantizamos de antemano.

**08 · Ética, privacidad y datos** — Medimos reacciones con reglas claras.
Consentimiento informado · Uso limitado · Protección y seguridad · Derecho a retirarse · No vendemos datos · Sin perfilamiento injustificado · Datos biométricos como sensibles · Evaluación legal por proyecto.
Aviso: «Las obligaciones legales dependen del tipo de estudio, los datos tratados, la ubicación de los participantes y la jurisdicción aplicable. Recomendamos revisar cada proyecto con asesoría legal especializada. En Chile, consideramos la normativa de protección de datos personales vigente y la Ley 21.719; mencionarla no constituye una certificación de cumplimiento.»

**09 · Diagnóstico** — Valida tu próxima decisión antes de invertir en producción.
Cuéntanos qué quieres evaluar: una marca, una campaña, un packaging, un sitio web o una experiencia digital. Revisaremos el desafío y te indicaremos qué metodología puede ser adecuada.
Qué pasa después: 01 Revisamos tu desafío · 02 Conversamos para entender el contexto · 03 Te proponemos método, alcance y plazos.

**Microcopy**

| Elemento | Texto |
|---|---|
| Botón principal | Agendar diagnóstico → |
| Botón secundario | Ver cómo funciona ↓ |
| Botón del formulario | Solicitar diagnóstico → / «Enviando…» |
| Indicador de scroll | Desliza |
| Placeholder correo | nombre@empresa.cl |
| Placeholder necesidad | Ej.: elegir entre dos diseños de packaging antes de imprimir. |
| Ayuda necesidad | Describe la decisión, no hace falta adjuntar archivos. |
| Ayuda presupuesto | Nos ayuda a proponerte un alcance realista. |
| Errores | Escribe tu nombre. · Escribe el nombre de tu empresa. · Revisa el formato del correo (ej.: nombre@empresa.cl). · Elige el tipo de proyecto. · Agrega un poco más de detalle (mínimo 20 caracteres). · Necesitamos tu autorización para contactarte. |
| Error de envío | No pudimos enviar la solicitud. Inténtalo de nuevo en unos minutos. |
| Confirmación | Solicitud recibida. Gracias. Revisaremos tu desafío y te escribiremos al correo que indicaste. |
| Aviso de privacidad | El formulario se envía por FormSubmit, un servicio externo, a nuestro correo. No pedimos datos biométricos. |
| HUD de la demo | Cuadro 001 / 080 · Fijaciones 0 |

## 5. Afirmaciones que requieren fuente o revisión legal

| Afirmación | Estado | Acción |
|---|---|---|
| «95 % de las decisiones de compra son no conscientes» (atribuido a Zaltman / Harvard Business School) | **Eliminada** | Sin fuente primaria verificable con ese alcance. |
| «80 % de las decisiones…», «3 segundos de atención», «95 % de las acciones…» | **Eliminadas** | Cifras populares sin respaldo metodológico claro. |
| «Cero opiniones», «Medimos cerebros», «respuesta real» | **Eliminadas** | Exageradas o imprecisas. |
| «Cifrado de extremo a extremo AES-256» | **Eliminada** | No verificada. Se reemplazó por «acceso restringido y separación entre identidad y señales». **[CONFIRMAR MEDIDAS TÉCNICAS REALES]** |
| «Cumplimiento verificable Ley 21.719 + NMSBA» | **Reformulada** | Se menciona como referencia, sin declarar cumplimiento. **Revisión legal recomendada.** |
| Los 8 principios de ética | **[CONFIRMAR CON NEUROGENOMIC]** | Deben reflejar prácticas reales (plazos de conservación, protocolo con menores, etc.). |
| «Muchas decisiones de consumo ocurren de forma rápida y parcialmente automática» | Formulación prudente | Coherente con Plassmann et al. (2015); no lleva cifra. |
| Referencias [1]–[6] | Obras publicadas y ampliamente citadas | **[CONFIRMAR FUENTE]**: revisar ediciones y páginas antes de publicar. |
| «Una empresa de Genomic Industries SpA» | Dato del sitio anterior | **[CONFIRMAR RAZÓN SOCIAL]** |
| Políticas de privacidad, cookies y términos | Borradores con marcadores | **Requieren asesoría legal.** |

## 6–8. Código

- HTML final: `index.html`
- CSS final: `css/styles.css`, más `css/fonts.css` con las fuentes
- JavaScript final: `js/main.js`, más `js/demo-data.js` con los datos simulados

Se cargan con `defer`, sin librerías ni peticiones a terceros (salvo el envío del formulario). Si el JavaScript falla, todo el contenido queda visible.

## 9. Recursos utilizados

| Recurso | Origen | Uso |
|---|---|---|
| `img/ref-dog-655.webp` | Pieza de campaña de Neurogenomic (recorte) | Hero |
| `img/ref-bottle-520.webp` | Pieza de campaña de Neurogenomic (recorte) | Problema |
| `img/ng-tracker-*.webp` | Render 3D propio (Blender) | Cómo funciona |
| `img/ng-box-{a,b,c}-*.webp` | Render 3D propio, marca ficticia BRISA | Caso ilustrativo |
| `img/seq/f_000–079.webp` | 80 renders 3D propios, marca ficticia MESTA | Demostración scroll-driven |
| `img/og-neurogenomic.jpg` | Composición propia | Open Graph / Twitter |
| Fuentes Anton, Space Grotesk, IBM Plex Mono | @fontsource, SIL OFL 1.1 | Tipografía (`fonts/LICENCIAS.md`) |
| Íconos de Problema y favicon | SVG inline propios | — |
| FormSubmit (formsubmit.co) | Servicio externo | Envío del formulario por correo |

Los renders se generan con los scripts del repositorio (`render/`).

## 10. Instalación

1. **Ver en local:** abre `index.html` con doble clic. Funciona sin servidor. Para probar el formulario, usa un servidor local: `python3 -m http.server` dentro de la carpeta y luego `http://localhost:8000`.
2. **Publicar:** sube la carpeta completa a cualquier hosting estático (Netlify, Vercel, GitHub Pages, cPanel, etc.) y conserva la estructura de carpetas.
3. **Dominio:** si no es `https://neurogenomic.cl/`, reemplázalo en `canonical`, `og:url`, `og:image`, `twitter:image` y en el JSON-LD de `index.html`.
4. **Formulario:**
   - Hoy envía a `cristiangm3005@gmail.com` mediante FormSubmit.
   - El primer envío desde el sitio publicado genera un correo «Activate Form»: ábrelo y confirma.
   - Para usar otro backend o un CRM, cambia `data-endpoint` en el `<form>`. Si lo dejas vacío, el formulario funciona en modo demostración y no envía.
5. **Legal:** completa los marcadores `[AGREGAR …]` de `privacidad.html`, `cookies.html` y `terminos.html` con asesoría legal. Cuando estén listos, quita `noindex`.
6. **Analítica:** no hay ninguna instalada. Antes de agregar Google Analytics, Meta Pixel u otra herramienta, implementa un banner de consentimiento y actualiza `cookies.html`.
7. **WordPress/Elementor:**
   - Sube `css/`, `js/`, `img/` y `fonts/` a tu tema o a la Biblioteca de medios.
   - Pega el contenido de `<main>` en un widget HTML.
   - Enlaza `styles.css`, `fonts.css`, `demo-data.js` y `main.js`, y ajusta las rutas.

## 11. Checklist responsive

- [x] 375 × 812 (móvil chico): sin scroll horizontal; CTA visible en el primer pantallazo (botón a 708–760 px).
- [x] 1440 × 900 (laptop): sin scroll horizontal, una sola columna de lectura cómoda.
- [ ] 320 px (iPhone SE 1.ª gen.): revisar el titular.
- [ ] 768 / 1024 px (tablet vertical/horizontal): revisar la demo (pasa a una columna bajo 1024 px).
- [ ] 1920 / 2560 px: el contenido se centra en un máximo de 1440 px.
- [x] Botones y enlaces de al menos 44 px de alto.
- [x] Tabla de evidencia convertida en bloques bajo 768 px.
- [x] Demo en móvil: escenario 4:5, puntos clave debajo, sin hover.
- [x] CTA fijo en móvil que se oculta en el formulario.
- [ ] Probar en Safari iOS y Chrome Android reales (el entorno de prueba fue Chromium).

## 12. Checklist SEO

- [x] Un solo H1; H2 por sección y H3 en tarjetas.
- [x] Title de 50 caracteres: «Neurogenomic | Neuromarketing y biometría en Chile».
- [x] Meta description de 119 caracteres.
- [x] Canonical (editable), Open Graph y Twitter Cards con imagen de 1200×630.
- [x] JSON-LD Organization + ProfessionalService, sin datos inventados.
- [x] Alt descriptivo en todas las imágenes; las ilustrativas lo indican.
- [x] Texto real (no imágenes) para todo el contenido, con términos clave: neuromarketing, eye tracking, facial coding, respuesta galvánica, packaging, e-commerce, investigación del consumidor.
- [x] Enlaces internos con anclas semánticas.
- [x] Páginas legales en borrador con `noindex`.
- [ ] Crear `sitemap.xml` y `robots.txt` al publicar.
- [ ] Registrar el sitio en Google Search Console.

## 13. Checklist de accesibilidad

- [x] Enlace «Saltar al contenido».
- [x] Orden de tabulación lógico (verificado: saltar → logo → menú → CTA → contenido).
- [x] Foco visible (contorno lima de 2 px).
- [x] Contraste AA: texto 17,6:1, secundario 8,1:1, terciario 4,9:1 (solo en ≥ 14 px), lima 16,2:1 sobre fondo.
- [x] Menú móvil con `aria-expanded`, `aria-controls`, cierre con Escape y foco al abrir.
- [x] Indicador de sección activa con `aria-current`.
- [x] Demo con `role="img"` y descripción completa; el canvas es decorativo (`aria-hidden`).
- [x] Formulario: etiquetas visibles, `aria-invalid`, `aria-describedby`, `aria-live` y foco en el primer error.
- [x] `prefers-reduced-motion`: sin animaciones; la demo se muestra en su estado final y completo.
- [x] Sin información solo en hover.
- [ ] Probar con NVDA/VoiceOver.

## 14. Checklist de conversión

- [x] Propuesta de valor y CTA en el primer pantallazo (escritorio y móvil).
- [x] CTA en hero, después de Servicios, después de Método, CTA fijo en móvil y formulario final.
- [x] Formulario de 7 campos (5 obligatorios + presupuesto opcional + consentimiento), sin datos biométricos.
- [x] Mensajes de error específicos y confirmación posterior al envío.
- [x] «Qué pasa después» en tres pasos, para reducir la incertidumbre.
- [x] Correo con asunto «Solicitud de diagnóstico · Nombre (Empresa)» y respuesta directa al solicitante.
- [ ] Activar FormSubmit y hacer un envío de prueba desde el sitio publicado.
- [ ] Definir el tiempo de respuesta comprometido y agregarlo bajo el botón.
- [ ] [AGREGAR TESTIMONIO AUTORIZADO] cuando exista.

## 15. Mejoras futuras priorizadas

1. **Alta:** completar y revisar legalmente privacidad, cookies y términos; confirmar los 8 principios de ética.
2. **Alta:** activar el formulario y conectarlo a un CRM o a un backend propio.
3. **Alta:** casos reales con autorización del cliente, cuando existan.
4. **Media:** analítica respetuosa con consentimiento (por ejemplo, Plausible o Matomo sin cookies) para medir la conversión.
5. **Media:** agregar AVIF como alternativa a WebP en los cuadros de la demo (unos 30 % menos de peso).
6. **Media:** página por servicio con más detalle (SEO de cola larga: «eye tracking packaging Chile», etc.).
7. **Baja:** versión en inglés.
8. **Baja:** una segunda secuencia para sitios web (eye tracking sobre una landing).
