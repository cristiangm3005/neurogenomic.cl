# Landing B2B Neurogenomic — diagnóstico, arquitectura y copy

Archivos: `landing.html` (publicable, usa `img/` e `img/seq/`) y `neurogenomic-landing.html` (un solo archivo, todo incrustado).
Fuente: `landing/src/landing.html`. Build: `python3 landing/build_landing.py [--frames carpeta_png]`.

---

## 1. Diagnóstico del archivo anterior (`neurogenomic-index.html`)

| Área | Problema | Corrección |
|---|---|---|
| **Propuesta de valor** | El H1 («El marketing digital cambió») describe el mercado, no lo que obtiene el cliente. | H1 orientado a resultado: «Valida antes de lanzar», con un subtítulo que dice qué se mide y qué decisión se toma. |
| **Claridad comercial** | No se dice para quién trabaja Neurogenomic ni qué entrega. | Línea «Para equipos de marketing, marca, e-commerce y producto…» y entregable explícito («qué lanzar, qué ajustar, qué descartar»). |
| **Narrativa** | Diez secciones con mucha atmósfera (preloader, perro, lata, botella, 95 %) antes de llegar a servicios y método. | Problema → servicios → método → demo → aplicaciones → caso → evidencia → ética → formulario. |
| **Afirmaciones científicas** | «95 % de las decisiones son no conscientes (Zaltman)», «80 %», «3 s», «95 % de las acciones…»: cifras populares sin respaldo metodológico sólido o mal atribuidas. | Eliminadas. La sección Evidencia explica qué mide cada técnica **y qué no**, con referencias metodológicas reales. |
| **Facial coding** | Se presentaba como lectura directa de emociones. | Se aclara que mide movimientos faciales y que inferir emociones depende del contexto (Barrett et al., 2019). |
| **Cumplimiento legal** | «Cumplimiento verificable (Ley 21.719 + NMSBA)», «AES-256 de extremo a extremo»: afirmaciones de cumplimiento automático y de seguridad no verificadas. | Se reemplazan por compromisos de diseño y una nota: «considerando… no reemplaza una evaluación legal específica». |
| **Caso** | «Una versión generó mayor atención sostenida…» se leía como un resultado real. | Rotulado de forma visible como **ejemplo ilustrativo, marca ficticia, datos simulados**. |
| **Demo** | Lecturas «en vivo» (FIX 214 ms, μS, valencia) que podían interpretarse como datos reales. | Toda visualización lleva la etiqueta «Ilustrativo · marca ficticia · datos simulados». |
| **CTA y formulario** | El CTA llevaba a otra página, a un formulario de cuatro pasos y diez campos. | Formulario en la misma página, de un solo paso y seis campos (cinco obligatorios), con validación en línea y un «qué pasa después» en tres pasos. |
| **Rendimiento** | GSAP + ScrollTrigger + Lenis por CDN, preloader, cursor personalizado, varios bucles rAF y 600 KB de imágenes incrustadas. | Cero librerías JS, un único bucle de scroll con rAF, canvas que se redibuja solo al cambiar el fotograma y carga progresiva de la secuencia. |
| **Scroll** | El scroll suavizado (Lenis) agrega inercia y puede sentirse «lento». | Scroll nativo. Las animaciones de revelado usan `animation-timeline: view()`, con respaldo IntersectionObserver. |
| **Accesibilidad** | Cursor que oculta el puntero del sistema, texto partido por letras y mucho texto en mono pequeño. | Puntero nativo, texto normal, `prefers-reduced-motion` completo, foco visible, landmarks y `aria-live` en el formulario. |
| **SEO** | Título genérico y JSON-LD con servicios que no coinciden con la oferta. | Título y descripción con las palabras de búsqueda (eye tracking, packaging, campañas, Chile), un H1 por página y JSON-LD con Organization, WebSite y 6 Service. |

## 2. Arquitectura

| # | Sección | Objetivo | Pregunta del visitante que responde |
|---|---|---|---|
| 1 | Hero | Resultado + para quién + CTA | ¿Qué hace y para quién? |
| 2 | Problema | Dolor de negocio (opinión declarada ≠ comportamiento) | ¿Qué problema resuelve? |
| 3 | Servicios | Seis líneas, cada una con «qué validamos» | ¿Qué me pueden entregar? |
| 4 | Método | Definir → Medir → Analizar → Recomendar | ¿Cómo trabajan? |
| 5 | Demo scroll-driven | Secuencia de 80 fotogramas en canvas + capas biométricas | ¿Cómo se ve una lectura? |
| 6 | Aplicaciones | Seis decisiones concretas | ¿Qué decisión me ayudan a validar? |
| 7 | Caso ilustrativo | Comparación A/B/C, rotulada como ficticia | ¿Qué tipo de resultado obtengo? |
| 8 | Evidencia y fuentes | Alcance y límites de cada técnica + referencias | ¿Es serio? |
| 9 | Ética y privacidad | Compromisos + nota legal prudente | ¿Mis datos y los de los participantes están protegidos? |
| 10 | CTA + formulario | Seis campos y respuesta con propuesta de alcance | ¿Cómo empiezo? |

**Animación de la demo (sección 5).** La sección mide 460 vh y contiene un bloque *sticky* de 100 svh. El progreso (0–1) sale de `getBoundingClientRect` en un único `requestAnimationFrame` por scroll, y se usa así:

- **Fotograma:** `round(progreso × 79)`. Son renders reales de Blender: la luz se enciende y la cámara orbita hasta quedar de frente.
- **Capas:** se dibujan en el mismo canvas usando las coordenadas de cada zona del packaging **en ese fotograma** (`landing/data/seq.json`), así que siguen a la bolsa mientras la cámara se mueve.
- **Fases:** estímulo (0–18 %), fijaciones (18–38 %), recorrido (38–58 %), mapa de calor (58–78 %) y zonas ciegas (78–100 %).
- **Carga:** al acercarse a la sección se precargan los fotogramas 1 de cada 8, luego 1 de cada 4, de 2 y el resto. Si falta un fotograma, se muestra el más cercano ya cargado.

## 3. Copy

**Hero**
- Etiqueta: Neuromarketing · Biometría · IA — Chile
- H1: **Valida antes de lanzar.**
- Subtítulo: Medimos cómo reaccionan personas reales a tu packaging, campaña o sitio web —qué miran, qué expresan, cuánto los activa— y lo convertimos en recomendaciones claras: qué lanzar, qué ajustar y qué descartar.
- Para quién: Para equipos de marketing, marca, e-commerce y producto que necesitan decidir con evidencia y no por intuición o por comité.
- CTA: Solicitar diagnóstico → · Ver cómo funciona ↓
- Técnicas: Eye tracking · Facial coding · Respuesta galvánica (GSR) · Análisis con IA

**01 · El problema** — *Lo que la gente dice no siempre explica lo que hace.*
Encuestas y focus groups recogen opiniones declaradas. Son útiles, pero tienen un límite: las personas no siempre saben —o no logran explicar— qué captó su atención o qué les generó rechazo. Cuando una decisión se toma por intuición o por comité, el error aparece después del lanzamiento, cuando corregir cuesta más.
- A. Un packaging que no se ve en la góndola: la marca o el beneficio clave quedan fuera del recorrido de la mirada.
- B. Campañas que se prueban gastando medios: se descubre qué no funciona cuando el presupuesto ya está invertido.
- C. Sitios y checkouts con fricción invisible: los usuarios abandonan y nadie reporta por qué.

**02 · Servicios** — *Qué podemos validar contigo.* Cada servicio parte de una pregunta de negocio concreta y termina en una recomendación accionable.
1. Packaging y marca: qué se ve primero, qué se entiende y qué pasa desapercibido en tu envase, logo o identidad visual.
2. Campañas y publicidad: pre-test de avisos, videos y key visuals antes de invertir en medios.
3. Sitios web y e-commerce: dónde se detiene la mirada, dónde aparece la fricción y qué se ignora en tu landing, ficha de producto o checkout.
4. Experiencias digitales: pruebas de experiencia con biometría para apps, plataformas y flujos de producto.
5. Análisis de datos: cruzamos los resultados biométricos con lo que declaran los participantes y con tus métricas de negocio, en tableros claros.
6. Implementación: branding, contenido, SEO y desarrollo para aplicar lo validado, si lo necesitas.

**03 · Método** — *De la pregunta a la decisión en cuatro pasos.*
1. Definir: acordamos la decisión que quieres validar, los estímulos a comparar y el perfil de participantes.
2. Medir: sesiones con personas reales. Usamos eye tracking, codificación facial o respuesta galvánica según lo que necesitemos responder.
3. Analizar: procesamos las señales y las cruzamos con lo que los participantes declaran. La IA ayuda a encontrar patrones; la interpretación la valida el equipo.
4. Recomendar: entregamos hallazgos, sus límites y recomendaciones concretas: qué mantener, qué ajustar y qué descartar.

**04 · Demostración** — *Así se lee una mirada.* (Ilustrativo · marca ficticia · datos simulados)
Estímulo → Fijaciones → Recorrido → Mapa de calor → Zonas ciegas.

**05 · Aplicaciones** — *Decisiones que puedes validar.*
- ¿Cuál de estas versiones de packaging elegir antes de imprimir?
- ¿El nuevo logo se reconoce y se diferencia de la categoría?
- ¿El aviso muestra la marca a tiempo y genera reacción?
- ¿Se entiende la propuesta de valor de la landing?
- ¿Dónde se traba el checkout?
- ¿Qué capta la atención en la góndola o el exhibidor?

**06 · Caso ilustrativo** — *Tres versiones de packaging, una pregunta.* (Ejemplo ilustrativo · marca ficticia · no es un cliente ni un resultado real)
- La pregunta: un equipo debe elegir entre tres diseños y no hay acuerdo interno.
- Cómo se mediría: participantes del público objetivo ven las tres versiones en una góndola simulada mientras registramos mirada y expresión.
- Qué entrega: una comparación de dónde va la atención en cada versión y qué elementos conviene ajustar.

**07 · Evidencia y fuentes** — *Qué mide cada técnica y qué no.* Tabla de alcance y límites, con seis referencias metodológicas:
Holmqvist et al. (2011), Duchowski (2017), Ekman y Friesen (1978), Barrett et al. (2019), Boucsein (2012) y Plassmann et al. (2015). Se aclara que son referencias generales, no estudios de Neurogenomic.

**08 · Ética y privacidad** — *Medimos reacciones, no perfilamos personas.* Consentimiento informado · Datos mínimos · Resultados agregados · Sin venta de datos · Sin manipulación · Menores, con resguardos.
Nota: «Diseñamos nuestros procesos considerando la normativa chilena de protección de datos personales (Ley 19.628 y Ley 21.719) y el código de ética de la NMSBA. Cada proyecto se revisa caso a caso; esta declaración no reemplaza una evaluación legal específica.»

**09 · Diagnóstico** — *Cuéntanos qué decisión necesitas validar.* Te respondemos con una propuesta de alcance: qué medir, con qué técnica, con quiénes y en qué plazo.
Formulario: nombre, correo de trabajo, empresa, qué quieres validar, mensaje, teléfono (opcional) y consentimiento. Botón: «Solicitar diagnóstico →».

## 4. Antes de publicar, confirma

- **Compromisos de ética:** cada uno (consentimiento, datos mínimos, sin venta de datos, menores, etc.) debe reflejar prácticas reales de Neurogenomic. Si alguno no aplica, ajústalo.
- **Referencias:** son obras publicadas y ampliamente citadas; aun así, revisa las citas antes de publicar.
- **Formulario:** el primer envío desde el sitio publicado dispara el correo de activación de FormSubmit a cristiangm3005@gmail.com.
