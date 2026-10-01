#!/usr/bin/env python3
"""
Neurogenomic 2026 · build estático.

Fuente única: src/core/* + src/sections/*.html (cada sección = <style> + HTML + <script>).
Genera:
  - index.html, servicios.html, tecnologia.html, contacto.html  (sitio estático completo)
  - elementor/NN-*.html  (bloques autocontenidos para el widget HTML de Elementor)
  - IMAGENES.md          (lista de imágenes, proporciones y prompts)

Uso:  python3 build.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
SITE = "https://neurogenomic.cl"

# ---------------------------------------------------------------- URLs
URLS_STATIC = {
    "index": "index.html", "servicios": "servicios.html", "tecnologia": "tecnologia.html",
    "contacto": "contacto.html", "etica": "index.html#etica",
    "privacidad": "/privacidad/", "terminos": "/terminos/",
}
URLS_WP = {
    "index": "/", "servicios": "/servicios/", "tecnologia": "/tecnologia/",
    "contacto": "/contacto/", "etica": "/#etica",
    "privacidad": "/privacidad/", "terminos": "/terminos/",
}
IMG_STATIC = "img/"
IMG_WP = "/img/"  # reemplazar por la ruta de la Biblioteca de medios al subir las imágenes

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@300;400;500;600;700&display=swap">')

# ---------------------------------------------------------------- Imágenes
# key: (n, archivo, ancho, alto, proporción, alt, prompt, sizes, eager, retrato_movil)
IMAGES = {
    "hero": (1, "hero-eye", 2560, 1440, "16:9 (desktop) + 9:16 (móvil: hero-eye-portrait)",
             "Macrofotografía de un ojo humano con el iris en foco y una fina mira láser verde reflejada en la córnea",
             "Macro photograph of a human eye, extreme close-up, iris in sharp focus, a thin volt-green (#C8F542) laser crosshair reflected on the cornea, dark charcoal background, cinematic low-key lighting, hyper-realistic, 8K, shallow depth of field, editorial tech campaign",
             "100vw", True, True),
    "svc-branding": (2, "branding-package", 1600, 2000, "4:5",
             "Mano sosteniendo un envase de producto sin marca bajo un foco de estudio, con un mapa de calor de eye tracking proyectado sobre la caja",
             "Hand holding a premium unbranded product package under a studio spotlight, faint eye-tracking heatmap projected onto the box in green and yellow, black background, hyper-realistic product photography",
             "(min-width:1024px) 34vw, 100vw", False, False),
    "svc-bi": (3, "bi-dashboard", 2560, 1440, "16:9",
             "Ejecutivo en una sala de vidrio oscura mirando un tablero holográfico con líneas de datos biométricos",
             "Executive in a dark glass room looking at a holographic dashboard of biometric data lines, reflections on glass, volt-green accent light, cinematic, hyper-realistic",
             "(min-width:1024px) 34vw, 100vw", False, False),
    "facial": (4, "facial-coding", 1600, 2000, "4:5",
             "Retrato de cerca de un rostro con una microexpresión sutil, iluminación Rembrandt en estudio oscuro",
             "Close-up portrait of a person's face with subtle micro-expression, precise thin white facial landmark points overlaid, dark studio, Rembrandt lighting, hyper-realistic skin texture",
             "(min-width:1024px) 30vw, 100vw", False, False),
    "gsr": (5, "gsr-sensor", 2000, 2000, "1:1",
             "Yemas de los dedos apoyadas sobre electrodos biométricos mínimos con cables finos, con luz de contorno verde",
             "Fingertips resting on minimal biometric sensor electrodes with thin cables, black matte surface, single green rim light, macro photography, hyper-realistic",
             "(min-width:1024px) 30vw, 100vw", False, False),
    "lab": (6, "lab-session", 2560, 1097, "21:9",
             "Laboratorio de neuromarketing: participante frente a un monitor con una barra de eye tracking y un operador desenfocado al fondo",
             "Modern neuromarketing lab, participant seated in front of a monitor with a slim eye tracker bar, operator in soft focus behind, dark interior, green monitor glow, documentary photography, hyper-realistic",
             "(min-width:1024px) 42vw, 100vw", False, False),
    "ethics": (7, "ethics-fingerprint", 2560, 1440, "16:9",
             "Macro abstracta de una huella dactilar que se disuelve en partículas de datos cifrados",
             "Abstract macro of a fingerprint pattern dissolving into encrypted data particles, black background, volt-green highlights, hyper-realistic",
             "(min-width:1024px) 42vw, 100vw", False, False),
    "cta": (8, "cta-eye-contracted", 2560, 1440, "16:9 (desktop) + 9:16 (móvil: cta-eye-contracted-portrait)",
             "El mismo ojo del inicio, ahora con la pupila contraída",
             "Same framing as the hero: macro photograph of the same human eye, extreme close-up, pupil strongly contracted (miosis), iris in sharp focus, thin volt-green (#C8F542) crosshair reflected on the cornea, dark charcoal background, cinematic low-key lighting, hyper-realistic, 8K, editorial tech campaign",
             "100vw", False, True),
    "svc-ecommerce": (9, "ecommerce-checkout", 1600, 2000, "4:5",
             "Mano sosteniendo un teléfono con un checkout minimalista, con puntos de fijación verdes sobre el botón de pago",
             "Close-up of a hand holding a smartphone showing a minimal checkout screen, tiny volt-green eye-tracking fixation dots over the pay button, dark studio, single green rim light, hyper-realistic, editorial tech campaign",
             "(min-width:1024px) 34vw, 100vw", False, False),
    "svc-marketing": (10, "marketing-pretest", 1600, 2000, "4:5",
             "Participante mirando un aviso en una pantalla en penumbra, con el reflejo de la pieza en sus ojos",
             "Person in a dark room watching an ad on a screen, the ad reflected in their eyes, slim eye tracker bar under the screen, volt-green accent light, cinematic low-key, hyper-realistic, documentary style",
             "(min-width:1024px) 34vw, 100vw", False, False),
    "svc-seo": (11, "seo-search", 1600, 2000, "4:5",
             "Monitor en una sala oscura con una página de resultados de búsqueda y una respuesta generada por IA resaltada en verde",
             "Dark desk, a single monitor showing an abstract search results page with one AI-generated answer card highlighted by a thin volt-green outline, reflections on glossy desk, cinematic low-key, hyper-realistic, no logos",
             "(min-width:1024px) 34vw, 100vw", False, False),
    "svc-software": (12, "software-build", 1600, 2000, "4:5",
             "Manos de desarrollador sobre un teclado con código reflejado en lentes, luz verde de monitor",
             "Developer's hands on a mechanical keyboard, code reflected on glasses lens in the foreground, dark interior, green monitor glow, shallow depth of field, hyper-realistic, editorial tech campaign",
             "(min-width:1024px) 34vw, 100vw", False, False),
}
OG = ("og-neurogenomic.jpg", "1200×630", "Composición del hero (ojo macro) con el logotipo Neurogenomic, para compartir en redes")

WIDTHS = [768, 1280, 1920, 2560]


def picture(key, base):
    n, name, w, h, ratio, alt, prompt, sizes, eager, portrait = IMAGES[key]
    def ss(nm, ext, widths=WIDTHS):
        return ", ".join(f"{base}{nm}-{x}.{ext} {x}w" for x in widths)
    srcs = []
    if portrait:
        pw = [768, 1280]
        srcs.append(f'<source media="(max-width:767px)" type="image/avif" srcset="{ss(name + "-portrait", "avif", pw)}" sizes="100vw">')
        srcs.append(f'<source media="(max-width:767px)" type="image/webp" srcset="{ss(name + "-portrait", "webp", pw)}" sizes="100vw">')
    srcs.append(f'<source type="image/avif" srcset="{ss(name, "avif")}" sizes="{sizes}">')
    srcs.append(f'<source type="image/webp" srcset="{ss(name, "webp")}" sizes="{sizes}">')
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<!-- IMAGEN {n:02d} · {name} · {ratio}\n     PROMPT: "{prompt}" -->\n'
            f'<picture>{"".join(srcs)}'
            f'<img src="{base}{name}-1280.webp" width="{w}" height="{h}" alt="{html.escape(alt)}" {load} '
            f'onerror="this.classList.add(\'ng-is-missing\')"></picture>')


# ---------------------------------------------------------------- Servicios
SERVICES = [
    dict(id="svc-branding", key="branding", name="Branding", img="svc-branding", ratio="4/5",
         title="Identidad calibrada contra el cerebro del consumidor.",
         desc="Construimos identidades de marca probando cada decisión —nombre, color, tono, símbolo— contra respuesta emocional y atencional real, antes de salir al mercado.",
         chips=["Eye Tracking", "Facial Coding", "Naming", "Sistema Visual", "Brand Voice + IA"],
         problems=[("Marca sin diferenciación", "Identidades que se parecen a la categoría completa y no generan recuerdo espontáneo ni preferencia medible."),
                   ("Decisiones por comité", "Logos y mensajes aprobados por consenso interno, nunca testeados contra la reacción real del consumidor.")],
         stages=[("Auditoría biométrica", "Testeamos marca actual y referentes de categoría con eye tracking y codificación facial para mapear el terreno emocional disponible."),
                 ("Arquitectura de marca + IA", "Generamos y filtramos variantes de naming, paleta y tono con modelos de lenguaje, reduciendo a un set corto validado por hallazgos biométricos."),
                 ("Validación final", "El sistema ganador se testea de nuevo antes de producción, confirmando activación emocional y memorabilidad superiores al benchmark de categoría.")]),
    dict(id="svc-bi", key="business-intelligence", name="Business Intelligence", img="svc-bi", ratio="16/9",
         title="Datos biométricos y de negocio en un solo tablero.",
         desc="Integramos datos biométricos, de negocio y de comportamiento digital en un sistema único de decisión, con modelos predictivos que anticipan la respuesta del consumidor.",
         chips=["Dashboards", "Modelos Predictivos", "Data Biométrica", "Machine Learning"],
         problems=[("Datos en silos", "Métricas de ventas, marketing y comportamiento viven en sistemas separados que nunca se cruzan para generar una decisión."),
                   ("Reportes que miran al pasado", "Dashboards descriptivos que explican qué pasó, sin capacidad de anticipar qué va a pasar.")],
         stages=[("Unificación de fuentes", "Conectamos CRM, e-commerce, analítica web y data biométrica de estudios previos en una capa de datos común."),
                 ("Modelado predictivo", "Entrenamos modelos de IA sobre esa data unificada para anticipar churn, propensión de compra y respuesta a campañas antes de ejecutarlas."),
                 ("Dashboards accionables", "Construimos dashboards ejecutivos que traducen los modelos en alertas y recomendaciones de acción, no solo gráficos.")]),
    dict(id="svc-ecommerce", key="ecommerce", name="E-commerce", img="svc-ecommerce", ratio="4/5",
         title="Arquitecturas de conversión basadas en fricción cognitiva.",
         desc="Diseñamos tiendas y catálogos donde cada fricción del recorrido de compra fue eliminada con base en eye tracking real sobre el flujo de checkout.",
         chips=["UX de Conversión", "Eye Tracking de Checkout", "Shopify / Headless", "Personalización con IA"],
         problems=[("Abandono de carrito", "Flujos de compra con fricciones invisibles para el equipo interno, pero evidentes en el comportamiento ocular y de clics del usuario real."),
                   ("Catálogo genérico", "Fichas de producto que no priorizan la información que el cerebro realmente busca en los primeros segundos de decisión.")],
         stages=[("Diagnóstico de fricción", "Eye tracking y grabación de sesiones reales sobre el flujo de checkout actual para ubicar los puntos exactos de abandono."),
                 ("Rediseño del flujo", "Reconstrucción de fichas de producto, carrito y checkout priorizando jerarquía visual validada biométricamente."),
                 ("Personalización con IA", "Motor de recomendación y búsqueda asistido por IA que adapta el catálogo mostrado al perfil de comportamiento de cada visitante.")]),
    dict(id="svc-marketing", key="marketing-digital", name="Marketing Digital", img="svc-marketing", ratio="4/5",
         title="Campañas pre-validadas con biometría, no con intuición.",
         desc="Diseñamos y operamos campañas que ya fueron probadas contra reacción emocional y atencional real antes de invertir un solo peso en medios.",
         chips=["Paid Media", "Pre-testing Biométrico", "Copy con IA", "CRO"],
         problems=[("Presupuesto quemado en testing", "Probar creativos en producción real, gastando presupuesto de medios para descubrir qué no funciona."),
                   ("Creatividad sin sistema", "Piezas que dependen del gusto individual del equipo creativo, sin trazabilidad a un principio de comportamiento del consumidor.")],
         stages=[("Pre-testing biométrico", "Cada concepto creativo se testea con codificación facial y eye tracking en panel reducido antes de invertir en medios pagados."),
                 ("Producción asistida por IA", "Generamos variantes de copy y creativo con modelos de lenguaje e imagen, filtradas por los hallazgos del pre-testing."),
                 ("Optimización continua", "Operamos las campañas con testing A/B permanente, retroalimentando el modelo de audiencia con cada ciclo.")]),
    dict(id="svc-seo", key="seo", name="SEO técnico y de contenido", img="svc-seo", ratio="4/5",
         title="Visibilidad orgánica diseñada para motores e IA generativa.",
         desc="Posicionamos marcas en buscadores tradicionales y en los motores de respuesta de IA generativa, con contenido estructurado para ambos.",
         chips=["SEO Técnico", "AEO / GEO", "Contenido E-E-A-T", "Schema Markup"],
         problems=[("Invisibilidad orgánica", "Sitios técnicamente correctos pero sin estrategia de contenido, que pierden posiciones frente a competidores más agresivos."),
                   ("Ausencia en respuestas de IA", "Contenido que no está estructurado para ser citado por motores de respuesta y buscadores conversacionales, y pierde la nueva capa de visibilidad.")],
         stages=[("Auditoría técnica", "Revisión completa de arquitectura, velocidad, indexación y señales E-E-A-T sobre el sitio actual."),
                 ("Estrategia de contenido", "Mapa de intención de búsqueda cruzado con los dominios de atención y memoria, priorizando temas con mayor potencial de codificación de marca."),
                 ("Optimización para IA", "Estructuración de contenido y datos estructurados para maximizar la citabilidad en motores de respuesta generativa.")]),
    dict(id="svc-software", key="software", name="Desarrollo de Software", img="svc-software", ratio="4/5",
         title="Producto digital con IA integrada de punta a punta.",
         desc="Construimos productos digitales a medida —desde landing pages hasta plataformas internas— con inteligencia artificial integrada desde la arquitectura, no añadida después.",
         chips=["Web & Apps", "Integración de IA", "WordPress / Elementor", "Automatización"],
         problems=[("Deuda técnica heredada", "Plataformas construidas por distintos proveedores sin coherencia, lentas, difíciles de mantener o escalar."),
                   ("IA como feature decorativo", "Chatbots o funciones de IA añadidas superficialmente, sin conexión con el dato real de negocio o de comportamiento.")],
         stages=[("Arquitectura del producto", "Definición de stack, estructura de datos e integraciones necesarias antes de escribir una sola línea de interfaz."),
                 ("Desarrollo iterativo", "Construcción en ciclos cortos con entregas funcionales tempranas, validadas con usuarios reales en cada iteración."),
                 ("IA nativa al producto", "Modelos de lenguaje y automatización conectados directamente a los datos de negocio: recomendación, soporte, generación de contenido o análisis.")]),
]


def services_html():
    out = []
    for i, s in enumerate(SERVICES, 1):
        chips = "".join(f'<li class="ng-chip">{html.escape(c)}</li>' for c in s["chips"])
        probs = "".join(f"<li><h4>{html.escape(t)}</h4><p>{html.escape(d)}</p></li>" for t, d in s["problems"])
        stages = "".join(f'<li><span class="ng-mono">Etapa {k}</span><h4>{html.escape(t)}</h4><p>{html.escape(d)}</p></li>'
                         for k, (t, d) in enumerate(s["stages"], 1))
        out.append(f'''      <article class="ng-svc__ch" id="{s["id"]}" aria-labelledby="{s["id"]}-t">
        <div class="ng-svc__in">
          <div class="ng-svc__main">
            <p class="ng-svc__lbl ng-mono"><b>Servicio {i:02d} / 06</b><span>{html.escape(s["name"])}</span></p>
            <h3 class="ng-svc__t" id="{s["id"]}-t"><span class="ng-sr">{html.escape(s["name"])}: </span>{html.escape(s["title"])}</h3>
            <p class="ng-svc__d">{html.escape(s["desc"])}</p>
            <ul class="ng-chips" aria-label="Capacidades">{chips}</ul>
            <div class="ng-svc__solve"><p class="ng-svc__k ng-mono">Qué resolvemos</p><ul>{probs}</ul></div>
            <div class="ng-svc__how"><p class="ng-svc__k ng-mono">Cómo lo hacemos</p><ol class="ng-svc__tl"><li class="ng-svc__line" aria-hidden="true" style="position:absolute"><i></i></li>{stages}</ol></div>
            <a class="ng-btn ng-btn--volt ng-svc__cta" href="{{{{u:contacto}}}}?servicio={s["key"]}">Solicitar diagnóstico <span class="ng-sr">de {html.escape(s["name"])}</span><span class="ng-btn__i" aria-hidden="true">↗</span></a>
          </div>
          <figure class="ng-svc__fig">
            <div class="ng-media" style="aspect-ratio:{s["ratio"]}" data-ph="/img/{IMAGES[s["img"]][1]} · {IMAGES[s["img"]][4]}">{{{{img:{s["img"]}}}}}</div>
            <figcaption class="ng-mono" aria-hidden="true"><span>S·{i:02d}</span><span>{html.escape(s["name"])}</span></figcaption>
          </figure>
        </div>
      </article>''')
    return "\n".join(out)


# ---------------------------------------------------------------- Cabeceras de página
PAGEHEADS = {
    "servicios": dict(eyebrow="Servicios · Neuroscience-Driven Marketing Optimization",
                      title="Decisiones de marca basadas en evidencia, no en intuición.",
                      text="Neurogenomic traduce neurociencia del consumidor e inteligencia artificial en sistemas de marca, contenido y crecimiento que funcionan porque están diseñados sobre cómo el cerebro realmente decide.",
                      meta="06 servicios · 01 framework", media=None),
    "tecnologia": dict(eyebrow="Registro en vivo — sesión de medición biométrica",
                       title="La intuición no se mide. La atención, sí.",
                       text="Eye tracking, facial coding y respuesta galvánica, cruzados con modelos de IA propios, para convertir reacciones no conscientes en una decisión validada antes de construir.",
                       meta="03 señales · IA propia", media="lab"),
    "contacto": dict(eyebrow="Contacto · Formulario de cotización",
                     title="Empieza hoy.",
                     text="Cuéntanos qué servicio necesitas hoy. El diagnóstico inicial es la base de todo lo que viene después.",
                     meta="Diagnóstico inicial", media=None),
}

# ---------------------------------------------------------------- Páginas
PAGES = {
    "index": dict(file="index.html", path="/",
                  title="Neurogenomic · Neuromarketing e IA para decisiones de marca con evidencia",
                  desc="Agencia chilena de neuromarketing e inteligencia biométrica: eye tracking, facial coding y respuesta galvánica cruzados con IA para optimizar marca, campañas, e-commerce y software.",
                  sections=["nav", "s0-preloader", "s1-hero", "s2-gaze", "s3-stat", "s4-signals", "s5-services",
                            "s6-method", "s7-why", "s8-case", "s9-ethics", "s10-cta", "footer"]),
    "servicios": dict(file="servicios.html", path="/servicios/",
                      title="Servicios · Neurogenomic — Seis servicios, un framework de evidencia",
                      desc="Branding, Business Intelligence, E-commerce, Marketing Digital, SEO y Desarrollo de Software validados con biometría y modelos de IA.",
                      sections=["nav", "pagehead", "s5-services", "s6-method", "s7-why", "s10-cta", "footer"]),
    "tecnologia": dict(file="tecnologia.html", path="/tecnologia/",
                       title="Tecnología · Neurogenomic — Eye tracking, facial coding y GSR con IA",
                       desc="Biometría real: tres señales involuntarias (atención, emoción y activación) cruzadas con modelos de IA propios, bajo la Ley 21.719.",
                       sections=["nav", "pagehead", "s4-signals", "s2-gaze", "s3-stat", "s8-case", "s9-ethics", "s10-cta", "footer"]),
    "contacto": dict(file="contacto.html", path="/contacto/",
                     title="Contacto · Neurogenomic — Solicita tu diagnóstico",
                     desc="Formulario de cotización: cuéntanos qué servicio necesitas y agenda el diagnóstico inicial con Neurogenomic.",
                     sections=["nav", "pagehead", "contact-form", "footer"]),
}


def jsonld(page):
    org = {
        "@type": "Organization", "@id": SITE + "/#org", "name": "Neurogenomic", "url": SITE + "/",
        "slogan": "Neuroscience-Driven Marketing Optimization",
        "description": PAGES["index"]["desc"],
        "parentOrganization": {"@type": "Organization", "name": "Genomic Industries SpA"},
        "areaServed": ["CL", "Latinoamérica"],
        "sameAs": ["https://www.linkedin.com/company/neurogenomic-cl/"],
        "logo": SITE + "/img/og-neurogenomic.jpg",
    }
    graph = [org]
    if page in ("index", "servicios"):
        for s in SERVICES:
            graph.append({"@type": "Service", "@id": SITE + "/servicios/#" + s["id"], "name": s["name"],
                          "description": s["desc"], "serviceType": s["name"], "provider": {"@id": SITE + "/#org"},
                          "areaServed": "CL", "url": SITE + "/servicios/#" + s["id"]})
    graph.append({"@type": "WebPage", "url": SITE + PAGES[page]["path"], "name": PAGES[page]["title"],
                  "inLanguage": "es-CL", "isPartOf": {"@type": "WebSite", "url": SITE + "/", "name": "Neurogenomic"},
                  "publisher": {"@id": SITE + "/#org"}})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def read(p):
    return (SRC / p).read_text(encoding="utf-8")


def render(text, urls, imgbase, page=None):
    if "{{services}}" in text:
        text = text.replace("{{services}}", services_html())
    if page in PAGEHEADS and "{{ph:" in text:
        ph = PAGEHEADS[page]
        media = ""
        if ph["media"]:
            k = ph["media"]
            media = f'<div class="ng-media ng-ph__media" data-ph="/img/{IMAGES[k][1]} · {IMAGES[k][4]}" data-ng-reveal>{{{{img:{k}}}}}</div>'
        for k in ("eyebrow", "title", "text", "meta"):
            text = text.replace("{{ph:%s}}" % k, html.escape(ph[k]))
        text = text.replace("{{ph:media}}", media)
    text = re.sub(r"\{\{img:([\w-]+)\}\}", lambda m: picture(m.group(1), imgbase), text)
    text = re.sub(r"\{\{u:(\w+)\}\}", lambda m: urls[m.group(1)], text)
    assert "{{" not in text, re.findall(r"\{\{[^}]*\}\}", text)[:3]
    return text


def split_block(text):
    styles = re.findall(r"<style>(.*?)</style>", text, re.S)
    body = re.sub(r"<style>.*?</style>\s*", "", text, flags=re.S)
    return "\n".join(s.strip() for s in styles), body.strip()


def min_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "\n", css)
    return css.strip()


def build_page(key):
    pg = PAGES[key]
    tokens = read("core/tokens.css")
    core = read("core/core.js")
    css_parts, body_parts = [min_css(tokens)], []
    for s in pg["sections"]:
        block = render(read(f"sections/{s}.html"), URLS_STATIC, IMG_STATIC, key)
        css, body = split_block(block)
        css_parts.append(min_css(css))
        if s in ("nav", "s0-preloader"):
            body_parts.append(body)
        else:
            body_parts.append(body)
    # El contenido principal se envuelve en <main>
    nav = [b for s, b in zip(pg["sections"], body_parts) if s in ("nav", "s0-preloader")]
    foot = [b for s, b in zip(pg["sections"], body_parts) if s == "footer"]
    main = [b for s, b in zip(pg["sections"], body_parts) if s not in ("nav", "s0-preloader", "footer")]
    url = SITE + pg["path"]
    hero_preload = ""
    if key == "index":
        hero_preload = ('<link rel="preload" as="image" type="image/avif" imagesrcset="'
                        + ", ".join(f"{IMG_STATIC}hero-eye-{w}.avif {w}w" for w in WIDTHS)
                        + '" imagesizes="100vw" media="(min-width:768px)" fetchpriority="high">')
    doc = f"""<!doctype html>
<html lang="es-CL" data-ng-page="{key}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(pg["title"])}</title>
<meta name="description" content="{html.escape(pg["desc"])}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0A0B0D">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CL">
<meta property="og:site_name" content="Neurogenomic">
<meta property="og:title" content="{html.escape(pg["title"])}">
<meta property="og:description" content="{html.escape(pg["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og-neurogenomic.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{FONTS}
{hero_preload}
<style>
{chr(10).join(css_parts)}
</style>
<script>
{core.strip()}
</script>
<script type="application/ld+json">
{jsonld(key)}
</script>
</head>
<body>
{chr(10).join(nav)}
<main id="ng-main">
{chr(10).join(main)}
</main>
{chr(10).join(foot)}
</body>
</html>
"""
    (ROOT / pg["file"]).write_text(doc, encoding="utf-8")
    return pg["file"]


ELEMENTOR = [
    ("00-global-nav", "nav", "index", "Header fijo, barra de progreso, menú móvil, cursor de fijación y grano. Pégalo en el header (Theme Builder) o al inicio de cada página."),
    ("01-s0-preloader", "s0-preloader", "index", "Solo en la página de inicio, justo después del header."),
    ("02-s1-hero", "s1-hero", "index", ""),
    ("03-s2-asi-mira", "s2-gaze", "index", ""),
    ("04-s3-dato-95", "s3-stat", "index", ""),
    ("05-s4-tecnologia", "s4-signals", "index", ""),
    ("06-s5-servicios", "s5-services", "index", ""),
    ("07-s6-metodo", "s6-method", "index", ""),
    ("08-s7-por-que", "s7-why", "index", ""),
    ("09-s8-caso", "s8-case", "index", ""),
    ("10-s9-etica", "s9-ethics", "index", ""),
    ("11-s10-cta-final", "s10-cta", "index", ""),
    ("12-footer", "footer", "index", "Pégalo en el footer (Theme Builder)."),
    ("13-pagehead-servicios", "pagehead", "servicios", "Cabecera con H1 de /servicios/."),
    ("14-pagehead-tecnologia", "pagehead", "tecnologia", "Cabecera con H1 de /tecnologia/."),
    ("15-pagehead-contacto", "pagehead", "contacto", "Cabecera con H1 de /contacto/."),
    ("16-contacto-formulario", "contact-form", "contacto", "Formulario en 4 pasos. Conecta el envío en data-endpoint."),
]


def build_elementor():
    out = ROOT / "elementor"
    out.mkdir(exist_ok=True)
    tokens = min_css(read("core/tokens.css"))
    core = read("core/core.js").strip()
    for fname, sec, page, note in ELEMENTOR:
        block = render(read(f"sections/{sec}.html"), URLS_WP, IMG_WP, page)
        css, body = split_block(block)
        head = (f"<!-- NEUROGENOMIC · Bloque Elementor «{fname}»\n"
                f"     Pegar completo en un widget HTML de Elementor (ancho completo, sin padding).\n"
                f"     Incluye tokens + núcleo NG (idempotentes: pueden repetirse en varios bloques).\n"
                + (f"     Nota: {note}\n" if note else "")
                + "     Imágenes: reemplaza /img/ por la URL de la Biblioteca de medios. -->\n")
        txt = (head + FONTS + "\n<style>\n" + tokens + "\n" + min_css(css) + "\n</style>\n"
               + "<script>\n" + core + "\n</script>\n" + body + "\n")
        (out / f"{fname}.html").write_text(txt, encoding="utf-8")


def build_images_md():
    rows = ["# Imágenes necesarias · Neurogenomic 2026", "",
            "Todas en AVIF + WebP, nítidas (sin blur ni velos), color grading hacia negros profundos con toques de verde volt `#C8F542`.",
            "Exporta cada imagen en **768 / 1280 / 1920 / 2560 px** de ancho con el patrón `nombre-ANCHO.avif` y `nombre-ANCHO.webp`",
            "(p. ej. `hero-eye-1920.avif`). Las variantes `-portrait` (9:16) solo necesitan 768 y 1280.", "",
            "Mientras una imagen no exista, el sitio muestra un placeholder técnico con el nombre del archivo (no una imagen rota).", "",
            "| # | Archivo base | Proporción | Dónde se usa | Prompt de generación |", "|---|---|---|---|---|"]
    where = {"hero": "S1 Hero", "svc-branding": "S5 Servicio 01 Branding", "svc-bi": "S5 Servicio 02 BI",
             "facial": "S4 panel C·02 Facial coding", "gsr": "S4 panel C·03 GSR", "lab": "S6 Método + cabecera Tecnología",
             "ethics": "S9 Ética", "cta": "S10 CTA final (cierre narrativo)", "svc-ecommerce": "S5 Servicio 03 E-commerce",
             "svc-marketing": "S5 Servicio 04 Marketing", "svc-seo": "S5 Servicio 05 SEO", "svc-software": "S5 Servicio 06 Software"}
    for k, v in sorted(IMAGES.items(), key=lambda kv: kv[1][0]):
        n, name, w, h, ratio, alt, prompt, *_ = v
        extra = " *(añadida: el brief no traía prompt para este servicio)*" if n >= 9 else ""
        extra = " *(variante del hero, pupila contraída)*" if k == "cta" else extra
        rows.append(f"| {n:02d} | `{name}` | {ratio} | {where[k]}{extra} | {prompt} |")
    rows += ["", f"| OG | `{OG[0]}` | 1200×630 | Open Graph / redes | {OG[2]} |", "",
             "Para la variante móvil del hero y del CTA, genera el mismo prompt en **9:16** y nómbralo `hero-eye-portrait` / `cta-eye-contracted-portrait`.",
             "", "Ajusta la variable CSS `--ng-pupil` (por defecto `64% 46%`) en `.ng-hero__media img` y `.ng-cta__media img` para que el zoom de scroll apunte exactamente a la pupila de tu foto."]
    (ROOT / "IMAGENES.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    files = [build_page(k) for k in PAGES]
    build_elementor()
    build_images_md()
    print("OK:", ", ".join(files), "+ elementor/ + IMAGENES.md")
