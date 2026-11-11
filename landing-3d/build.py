#!/usr/bin/env python3
"""Landing 3D de Neurogenomic: genera dos entregables autónomos a partir de src/landing.html.

  neurogenomic-landing-3d.html            página completa (abrir o subir tal cual)
  neurogenomic-landing-3d-elementor.json  plantilla de Elementor (Importar plantilla → Insertar, Elementor Canvas)

Ambos llevan dentro las tipografías y Three.js, así no dependen de CDNs que un plugin de caché o el hosting
puedan bloquear. Requiere vendor/three.min.js y vendor/fonts/*.woff2 (ver vendor/README.md).
Uso: python3 landing-3d/build.py
"""
import base64, json, secrets
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VEND = ROOT / "vendor"
FORM_TO = "cristiangm3005@gmail.com"            # destino de los formularios (FormSubmit)
ENDPOINT = f"https://formsubmit.co/ajax/{FORM_TO}"  # envío con JavaScript (sin salir de la página)
FORM_POST = f"https://formsubmit.co/{FORM_TO}"      # respaldo sin JavaScript: POST normal, nunca GET a la portada
MAIL = "contacto@neurogenomic.cl"                   # correo visible en el sitio
FACES = [("Big Shoulders Display", "big-shoulders-display-latin-800-normal", 400),
         ("Schibsted Grotesk", "schibsted-grotesk-latin-400-normal", 400), ("Schibsted Grotesk", "schibsted-grotesk-latin-500-normal", 500),
         ("Schibsted Grotesk", "schibsted-grotesk-latin-600-normal", 600),
         ("Martian Mono", "martian-mono-latin-400-normal", 400), ("Martian Mono", "martian-mono-latin-500-normal", 500)]
TITLE = "Neurogenomic · Neuromarketing y eye tracking en Chile"
SITE = "https://neurogenomic.cl"
DESC = ("Agencia chilena de neuromarketing: eye tracking, facial coding y respuesta galvánica cruzados con IA "
        "para validar marca, campañas, packaging y e-commerce antes de invertir.")


REG = []  # páginas para el archivo de importación de WordPress (WXR)
SEO = {
    "portada": "Neurogenomic · Neuromarketing y eye tracking en Chile",
    "contacto": "Contacto · Neurogenomic", "privacidad": "Política de privacidad · Neurogenomic",
    "metodo": "Método: cómo medimos y sus límites · Neurogenomic", "servicios": "Servicios de neuromarketing · Neurogenomic",
    "branding": "Branding probado con personas · Neurogenomic", "business-intelligence": "Business Intelligence y modelos predictivos · Neurogenomic",
    "ecommerce": "E-commerce y eye tracking de checkout · Neurogenomic", "marketing-digital": "Pre-test de piezas publicitarias · Neurogenomic",
    "seo": "SEO para buscadores y motores de IA · Neurogenomic", "desarrollo-web": "Desarrollo web con IA integrada · Neurogenomic",
}


def brandline(d):
    return f"Neurogenomic es una marca de {d['razon_social']}" + (f" · RUT {d['rut']}" if d.get("rut") else "")


def org(d):
    o = {"@type": "Organization", "@id": SITE + "/#organizacion", "name": "Neurogenomic", "url": SITE + "/", "email": d["correo"],
         "description": DESC, "areaServed": {"@type": "Country", "name": "Chile"},
         "knowsAbout": ["Neuromarketing", "Eye tracking", "Respuesta galvánica", "Investigación de consumidores"],
         "parentOrganization": {"@type": "Organization", "name": d["razon_social"]}}
    if d.get("telefono"):
        o["telephone"] = d["telefono"]
    return o


def jsonld(graph):
    txt = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/ld+json">{txt}</script>'


def fragment():
    d = legal_data(quiet=True)
    s = (HERE / "src" / "landing.html").read_text(encoding="utf-8")
    s = (s.replace("{{BRANDLINE}}", brandline(d)).replace("{{SITE}}", SITE)
          .replace("{{JSONLD}}", jsonld([org(d), {"@type": "WebSite", "@id": SITE + "/#sitio", "url": SITE + "/", "name": "Neurogenomic",
                                                   "inLanguage": "es-CL", "publisher": {"@id": SITE + "/#organizacion"}}])))
    faces = "".join(
        f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:swap;"
        f"src:url(data:font/woff2;base64,{base64.b64encode((VEND / 'fonts' / (fn + '.woff2')).read_bytes()).decode()}) format('woff2')}}"
        for fam, fn, wt in FACES)
    three = (VEND / "three.min.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
    return (s.replace("{{FONTS}}", faces).replace("{{THREE}}", f"<script>{three}</script>")
             .replace("{{POUCH}}", "data:image/webp;base64," + base64.b64encode((ROOT / "img" / "ng-pouch-1600.webp").read_bytes()).decode())
             .replace("{{ENDPOINT}}", ENDPOINT).replace("{{FORM_POST}}", FORM_POST).replace("{{MAIL}}", MAIL)
             .replace("{{CONTACT}}", "/contacto/").replace("{{PRIVACY}}", "/privacidad/"))


def main():
    frag = fragment()
    page = ("<!doctype html>\n<html lang=\"es-CL\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
            f"<title>{TITLE}</title>\n<meta name=\"description\" content=\"{DESC}\">\n"
            "<meta name=\"theme-color\" content=\"#050607\">\n"
            "<style>html,body{margin:0;background:#050607}</style>\n</head>\n<body>\n" + frag + "\n</body>\n</html>\n")
    (HERE / "neurogenomic-landing-3d.html").write_text(page, encoding="utf-8")

    zero = {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
    el_css = ("<style>.lx-el.e-con{--padding-top:0px;--padding-right:0px;--padding-bottom:0px;--padding-left:0px;--gap:0px;--row-gap:0px;--column-gap:0px;padding:0}"
              ".lx-el>.elementor-widget-html,.lx-el .elementor-widget-container{margin:0;padding:0}</style>\n")
    widget = {"id": secrets.token_hex(4), "elType": "widget", "widgetType": "html", "isInner": False, "elements": [],
              "settings": {"html": el_css + frag, "_margin": zero, "_padding": zero}}
    cont = {"id": secrets.token_hex(4), "elType": "container", "isInner": False, "elements": [widget],
            "settings": {"container_type": "flex", "content_width": "full", "flex_direction": "column",
                         "flex_gap": {"column": "0", "row": "0", "isLinked": True, "unit": "px", "size": 0},
                         "padding": zero, "padding_tablet": zero, "padding_mobile": zero, "margin": zero,
                         "_title": "Landing 3D Neurogenomic (bloque completo)", "css_classes": "lx-el"}}
    tpl = {"title": "Neurogenomic · Landing 3D", "type": "page", "version": "0.4",
           "page_settings": {"template": "elementor_canvas", "hide_title": "yes",
                             "background_background": "classic", "background_color": "#050607"},
           "content": [cont]}
    # Código para pegar directamente en un widget HTML de Elementor (mismo contenido que la plantilla)
    (HERE / "neurogenomic-landing-3d-widget.html").write_text(
        "<!-- NEUROGENOMIC · Landing 3D · pegar completo en un widget HTML (página con plantilla Elementor Canvas) -->\n" + el_css + frag, encoding="utf-8")
    REG.append(dict(group=1, title="Portada", slug="portada", parent=None, content=tpl["content"], desc=DESC))
    f = HERE / "neurogenomic-landing-3d-elementor.json"
    f.write_text(json.dumps(tpl, ensure_ascii=False, indent=1), encoding="utf-8")
    json.loads(f.read_text(encoding="utf-8"))
    print("ok", len(page) // 1024, "KB")
    build_pages(el_css, zero)
    build_wxr()


# ---------------------------------------------------------------- Páginas interiores
PAGES = {
    "contacto": ("Contacto · Neurogenomic", "Escríbenos para evaluar tu marca, campaña, packaging o sitio web con neuromarketing e IA.", "/contacto/"),
    "privacidad": ("Política de privacidad · Neurogenomic", "Cómo Neurogenomic trata los datos personales y biométricos: finalidades, plazos, seguridad y derechos.", "/privacidad/"),
    "metodo": ("Método: cómo medimos y sus límites · Neurogenomic", "Qué mide y qué no mide el eye tracking, la respuesta galvánica y el movimiento facial; tamaños de muestra y limitaciones de cada estudio.", "/metodo/"),
}


def faces_css(names=None):
    return "".join(
        f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:swap;"
        f"src:url(data:font/woff2;base64,{base64.b64encode((VEND / 'fonts' / (fn + '.woff2')).read_bytes()).decode()}) format('woff2')}}"
        for fam, fn, wt in FACES)


def legal_data(quiet=False):
    import re
    d = json.loads((HERE / "datos-legales.json").read_text(encoding="utf-8"))
    d = {k: (v or "").strip() for k, v in d.items() if not k.startswith("_")}
    d["telefono_tel"] = re.sub(r"[^\d+]", "", d.get("telefono", ""))
    d["whatsapp_wa"] = re.sub(r"\D", "", d.get("whatsapp", ""))
    for k in ("rut", "domicilio", "fecha_actualizacion"):
        if not d.get(k) and not quiet:
            print(f"  aviso: datos-legales.json → «{k}» vacío; esa línea no se publica en /privacidad/")
    return d


def fill(s, d):
    import re
    # [[opt:campo]] … [[/opt]] se publica solo si el campo tiene valor
    s = re.sub(r"\[\[opt:(\w+)\]\](.*?)\[\[/opt\]\]", lambda m: m.group(2) if d.get(m.group(1)) else "", s, flags=re.S)
    s = re.sub(r"\[\[noopt:(\w+)\]\](.*?)\[\[/noopt\]\]", lambda m: "" if d.get(m.group(1)) else m.group(2), s, flags=re.S)
    s = re.sub(r"\{\{d:(\w+)\}\}", lambda m: d.get(m.group(1), ""), s)
    return s


def build_pages(el_css, zero):
    import html as H
    d = legal_data()
    css = (HERE / "src" / "paginas.css").read_text(encoding="utf-8")
    out = HERE / "paginas"
    out.mkdir(exist_ok=True)
    for name, (title, desc, path) in PAGES.items():
        s = (HERE / "src" / f"{name}.html").read_text(encoding="utf-8")
        graph = [org(d), {"@type": "WebPage", "url": SITE + path, "name": title, "inLanguage": "es-CL", "publisher": {"@id": SITE + "/#organizacion"}}]
        frag = fill(s.replace("{{FONTS}}", faces_css()).replace("{{CSS}}", css).replace("{{ENDPOINT}}", ENDPOINT)
                    .replace("{{FORM_POST}}", FORM_POST).replace("{{SITE}}", SITE).replace("{{BRANDLINE}}", brandline(d))
                    .replace("{{JSONLD}}", jsonld(graph)), d)
        assert "{{" not in frag and "[[" not in frag, f"marcador sin reemplazar en {name}"
        page = ("<!doctype html>\n<html lang=\"es-CL\">\n<head>\n<meta charset=\"utf-8\">\n"
                "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
                f"<title>{H.escape(title)}</title>\n<meta name=\"description\" content=\"{H.escape(desc)}\">\n"
                "<style>html,body{margin:0;background:#050607}</style>\n</head>\n<body>\n" + frag + "\n</body>\n</html>\n")
        (out / f"neurogenomic-{name}.html").write_text(page, encoding="utf-8")
        (out / f"neurogenomic-{name}-widget.html").write_text(
            f"<!-- NEUROGENOMIC · {title} · pegar completo en un widget HTML (página {path}, plantilla Elementor Canvas) -->\n" + el_css.replace("lx-el", "lx-el") + frag, encoding="utf-8")
        widget = {"id": secrets.token_hex(4), "elType": "widget", "widgetType": "html", "isInner": False, "elements": [],
                  "settings": {"html": el_css + frag, "_margin": zero, "_padding": zero}}
        cont = {"id": secrets.token_hex(4), "elType": "container", "isInner": False, "elements": [widget],
                "settings": {"container_type": "flex", "content_width": "full", "flex_direction": "column",
                             "flex_gap": {"column": "0", "row": "0", "isLinked": True, "unit": "px", "size": 0},
                             "padding": zero, "padding_tablet": zero, "padding_mobile": zero, "margin": zero,
                             "_title": f"{title} (bloque completo)", "css_classes": "lx-el"}}
        tpl = {"title": f"Neurogenomic · {name.capitalize()}", "type": "page", "version": "0.4",
               "page_settings": {"template": "elementor_canvas", "hide_title": "yes",
                                 "background_background": "classic", "background_color": "#050607"},
               "content": [cont]}
        REG.append(dict(group=2, title={"contacto": "Contacto", "privacidad": "Privacidad", "metodo": "Método"}[name], slug=name, parent=None,
                        content=tpl["content"], desc=desc))
        f = out / f"neurogenomic-{name}-elementor.json"
        f.write_text(json.dumps(tpl, ensure_ascii=False, indent=1), encoding="utf-8")
        json.loads(f.read_text(encoding="utf-8"))
        print("ok", name, len(page) // 1024, "KB")
    build_services(d, css, el_css, zero)
    # Variante de Privacidad para cuando se instale Google Analytics 4 (archivo 04 de importación)
    dg = dict(d, analitica="Google Analytics 4")
    title, desc, path = PAGES["privacidad"]
    s = (HERE / "src" / "privacidad.html").read_text(encoding="utf-8")
    graph = [org(dg), {"@type": "WebPage", "url": SITE + path, "name": title, "inLanguage": "es-CL", "publisher": {"@id": SITE + "/#organizacion"}}]
    frag = fill(s.replace("{{FONTS}}", faces_css()).replace("{{CSS}}", css).replace("{{SITE}}", SITE).replace("{{BRANDLINE}}", brandline(dg))
                .replace("{{JSONLD}}", jsonld(graph)), dg)
    REG.append(dict(group=4, title="Privacidad", slug="privacidad", parent=None, desc=desc,
                    content=[{"id": secrets.token_hex(4), "elType": "container", "isInner": False, "settings": {"container_type": "flex", "content_width": "full", "flex_direction": "column", "padding": zero, "margin": zero, "css_classes": "lx-el", "_title": f"{title} (bloque completo)"},
                              "elements": [{"id": secrets.token_hex(4), "elType": "widget", "widgetType": "html", "isInner": False, "elements": [], "settings": {"html": el_css + frag, "_margin": zero, "_padding": zero}}]}]))


def emit(name, title, desc, path, frag, el_css, zero, outdir, wp=None):
    """Escribe una página en sus tres formatos: HTML suelto, bloque para widget y plantilla de Elementor."""
    import html as H
    outdir.mkdir(parents=True, exist_ok=True)
    page = ("<!doctype html>\n<html lang=\"es-CL\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
            f"<title>{H.escape(title)}</title>\n<meta name=\"description\" content=\"{H.escape(desc)}\">\n"
            "<style>html,body{margin:0;background:#050607}</style>\n</head>\n<body>\n" + frag + "\n</body>\n</html>\n")
    (outdir / f"neurogenomic-{name}.html").write_text(page, encoding="utf-8")
    (outdir / f"neurogenomic-{name}-widget.html").write_text(
        f"<!-- NEUROGENOMIC · {title} · pegar completo en un widget HTML (página {path}, plantilla Elementor Canvas) -->\n" + el_css + frag, encoding="utf-8")
    widget = {"id": secrets.token_hex(4), "elType": "widget", "widgetType": "html", "isInner": False, "elements": [],
              "settings": {"html": el_css + frag, "_margin": zero, "_padding": zero}}
    cont = {"id": secrets.token_hex(4), "elType": "container", "isInner": False, "elements": [widget],
            "settings": {"container_type": "flex", "content_width": "full", "flex_direction": "column",
                         "flex_gap": {"column": "0", "row": "0", "isLinked": True, "unit": "px", "size": 0},
                         "padding": zero, "padding_tablet": zero, "padding_mobile": zero, "margin": zero,
                         "_title": f"{title} (bloque completo)", "css_classes": "lx-el"}}
    tpl = {"title": f"Neurogenomic · {title.split(' · ')[0]}", "type": "page", "version": "0.4",
           "page_settings": {"template": "elementor_canvas", "hide_title": "yes", "background_background": "classic", "background_color": "#050607"},
           "content": [cont]}
    if wp:
        REG.append(dict(group=3, title=wp[0], slug=name, parent=wp[1], content=tpl["content"], desc=desc))
    f = outdir / f"neurogenomic-{name}-elementor.json"
    f.write_text(json.dumps(tpl, ensure_ascii=False, indent=1), encoding="utf-8")
    json.loads(f.read_text(encoding="utf-8"))
    print("ok", name, len(page) // 1024, "KB")


def build_services(d, css, el_css, zero):
    """Índice /servicios/ y una página por servicio, desde servicios.json."""
    import html as H
    e = H.escape
    data = json.loads((HERE / "servicios.json").read_text(encoding="utf-8"))["servicios"]
    head = ('<div class="lx-pg">\n  <header class="lx-pg__top">\n    <a class="lx-pg__brand" href="/" aria-label="Neurogenomic, volver a la portada">Neuro<b>genomic</b></a>\n'
            '    <a class="lx-pg__back" href="/servicios/">← <span>Todos los </span>servicios</a>\n  </header>\n')
    foot = (f'  <footer class="lx-foot"><span>© 2026 · {e(brandline(d))}</span><span class="lx-foot__l"><a href="mailto:{e(d["correo"])}">{e(d["correo"])}</a>'
            '<a href="/">Portada</a><a href="/metodo/">Método</a><a href="/contacto/">Contacto</a><a href="/privacidad/">Privacidad y datos</a></span></footer>\n')
    style = "<style>\n" + faces_css() + "\n" + css + "\n</style>\n"
    outdir = HERE / "paginas" / "servicios"
    services = []
    for s in data:
        url = f"/servicios/{s['slug']}/"
        plazo = s.get("plazo") or "Se define en el diagnóstico"
        precio = s.get("precio") or "A cotizar"
        probs = "".join(f'<li><h3>{e(t)}</h3><p>{e(x)}</p></li>' for t, x in s["problemas"])
        ents = "".join(f'<li><b>{i + 1:02d}</b><div><h3>{e(t)}</h3><p>{e(x)}</p></div></li>' for i, (t, x) in enumerate(s["entregables"]))
        nav = "".join(f'<a href="/servicios/{o["slug"]}/"{" aria-current=\"page\"" if o is s else ""}>{e(o["nombre"])}</a>' for o in data)
        graph = [org(d), {"@type": "Service", "@id": SITE + url, "url": SITE + url, "name": s["nombre"], "serviceType": s["nombre"],
                          "description": s["lead"], "provider": {"@id": SITE + "/#organizacion"}, "areaServed": {"@type": "Country", "name": "Chile"}}]
        body = (head + '  <main class="lx-pg__main">\n'
                f'    <p class="lx-k"><b>Servicio S·{s["n"]}</b> {e(s["nombre"])}</p>\n'
                f'    <h1 class="lx-h">{e(s["titulo"])}</h1>\n    <p class="lx-lead">{e(s["lead"])}</p>\n'
                f'    <p class="lx-valida"><span>Decisión que valida</span>{e(s["valida"])}</p>\n'
                '    <div class="lx-svc">\n      <div>\n'
                f'        <section class="lx-svc__sec"><h2>Problemas que resuelve</h2><ul class="lx-svc__p">{probs}</ul></section>\n'
                f'        <section class="lx-svc__sec"><h2>Qué entregamos</h2><ol class="lx-svc__d">{ents}</ol></section>\n'
                f'        <section class="lx-svc__sec"><h2>Cómo medimos</h2><p class="lx-svc__m">{e(s["medicion"])} <a href="/metodo/">Ver método y limitaciones →</a></p></section>\n'
                '      </div>\n'
                '      <aside class="lx-buy" aria-label="Cómo contratar">\n'
                f'        <dl><div><dt>Plazo típico</dt><dd>{e(plazo)}</dd></div><div><dt>Inversión</dt><dd>{e(precio)}</dd></div></dl>\n'
                '        <p>Se contrata solo o integrado con otros servicios. El primer paso es un diagnóstico para definir alcance, plazo y presupuesto.</p>\n'
                '        <a class="lx-btn" href="/contacto/">Solicitar diagnóstico <span aria-hidden="true">→</span></a>\n'
                '      </aside>\n    </div>\n'
                f'    <nav class="lx-svc__nav" aria-label="Otros servicios">{nav}</nav>\n  </main>\n' + foot + "  " + jsonld(graph) + "\n</div>\n")
        services.append((s["slug"], f'{s["nombre"]} · Servicios · Neurogenomic', s["lead"], url, style + body, s["nombre"]))
    cards = "".join(f'<li><a href="/servicios/{s["slug"]}/"><b>S·{s["n"]}</b><h2>{e(s["nombre"])}</h2><p>{e(s["titulo"])}</p>'
                    f'<span>Valida: {e(s["valida"][0].lower() + s["valida"][1:])}</span></a></li>' for s in data)
    graph = [org(d), {"@type": "ItemList", "name": "Servicios de Neurogenomic", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + f"/servicios/{s['slug']}/", "name": s["nombre"]} for i, s in enumerate(data)]}]
    body = (head.replace('href="/servicios/">← <span>Todos los </span>servicios', 'href="/">← <span>Volver a la </span>portada') + '  <main class="lx-pg__main">\n'
            '    <p class="lx-k"><b>Servicios</b> Seis líneas, un método</p>\n    <h1 class="lx-h">Seis servicios. <em>Un framework.</em></h1>\n'
            '    <p class="lx-lead">Cada línea se contrata sola o integrada. Todas usan el mismo método: medir, modelar, construir y verificar.</p>\n'
            f'    <ul class="lx-svcs">{cards}</ul>\n  </main>\n' + foot + "  " + jsonld(graph) + "\n</div>\n")
    emit("servicios", "Servicios · Neurogenomic", "Branding, Business Intelligence, E-commerce, Marketing digital, SEO y Desarrollo web, validados con eye tracking, respuesta galvánica e IA.",
         "/servicios/", style + body, el_css, zero, HERE / "paginas", wp=("Servicios", None))
    # Los servicios van después del índice: en WordPress son páginas hijas de «Servicios» (/servicios/<slug>/)
    for slug, title, desc, url, frag, nombre in services:
        emit(slug, title, desc, url, frag, el_css, zero, outdir, wp=(nombre, "servicios"))


def php_ser(d):
    """Serializa un dict de textos como lo guarda WordPress (los ajustes de página de Elementor)."""
    out = "".join(f's:{len(k.encode())}:"{k}";s:{len(v.encode())}:"{v}";' for k, v in d.items())
    return f"a:{len(d)}:{{{out}}}"


def build_wxr():
    """Archivos de importación de WordPress (Herramientas › Importar › WordPress): crean todas las páginas de una vez,
    con su slug, la página superior de los servicios, la plantilla Elementor Canvas, el contenido de Elementor y el
    título y la descripción para Yoast SEO o Rank Math. Tres archivos para no superar los límites de subida habituales."""
    def cdata(s):
        return "<![CDATA[" + str(s).replace("]]>", "]]]]><![CDATA[>") + "]]>"
    ids = {r["slug"]: 9101 + i for i, r in enumerate(r for r in REG if r["group"] != 4)}
    settings = php_ser({"hide_title": "yes", "background_background": "classic", "background_color": "#050607"})
    names = {1: "01-portada", 2: "02-contacto-privacidad-metodo", 3: "03-servicios", 4: "04-privacidad-con-analitica"}
    outdir = HERE / "subir"
    outdir.mkdir(exist_ok=True)
    for g, fname in names.items():
        items = []
        for i, r in enumerate([r for r in REG if r["group"] == g]):
            meta = [("_wp_page_template", "elementor_canvas"), ("_elementor_edit_mode", "builder"), ("_elementor_template_type", "wp-page"),
                    ("_elementor_version", "3.33.0"), ("_elementor_page_settings", settings),
                    ("_elementor_data", json.dumps(r["content"], ensure_ascii=False)),
                    ("_yoast_wpseo_title", SEO[r["slug"]]), ("_yoast_wpseo_metadesc", r["desc"]),
                    ("rank_math_title", SEO[r["slug"]]), ("rank_math_description", r["desc"])]
            path = (f"/servicios/{r['slug']}/" if r["parent"] else ("/" if r["slug"] == "portada" else f"/{r['slug']}/"))
            items.append(
                "<item>\n"
                f"<title>{cdata(r['title'])}</title>\n<link>{SITE}{path}</link>\n<pubDate>Wed, 11 Nov 2026 12:00:00 +0000</pubDate>\n"
                f"<dc:creator>{cdata('neurogenomic')}</dc:creator>\n<guid isPermaLink=\"false\">{SITE}/?page_id={ids[r['slug']]}</guid>\n"
                "<description></description>\n<content:encoded><![CDATA[]]></content:encoded>\n<excerpt:encoded><![CDATA[]]></excerpt:encoded>\n"
                f"<wp:post_id>{ids[r['slug']]}</wp:post_id>\n<wp:post_date>{cdata('2026-11-11 09:00:00')}</wp:post_date>\n"
                f"<wp:post_date_gmt>{cdata('2026-11-11 12:00:00')}</wp:post_date_gmt>\n"
                f"<wp:post_modified>{cdata('2026-11-11 09:00:00')}</wp:post_modified>\n<wp:post_modified_gmt>{cdata('2026-11-11 12:00:00')}</wp:post_modified_gmt>\n"
                f"<wp:comment_status>{cdata('closed')}</wp:comment_status>\n<wp:ping_status>{cdata('closed')}</wp:ping_status>\n"
                f"<wp:post_name>{cdata(r['slug'])}</wp:post_name>\n<wp:status>{cdata('publish')}</wp:status>\n"
                f"<wp:post_parent>{ids[r['parent']] if r['parent'] else 0}</wp:post_parent>\n<wp:menu_order>{i}</wp:menu_order>\n"
                f"<wp:post_type>{cdata('page')}</wp:post_type>\n<wp:post_password><![CDATA[]]></wp:post_password>\n<wp:is_sticky>0</wp:is_sticky>\n"
                + "".join(f"<wp:postmeta>\n<wp:meta_key>{cdata(k)}</wp:meta_key>\n<wp:meta_value>{cdata(v)}</wp:meta_value>\n</wp:postmeta>\n" for k, v in meta)
                + "</item>\n")
        xml = ('<?xml version="1.0" encoding="UTF-8" ?>\n'
               '<rss version="2.0" xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/" xmlns:content="http://purl.org/rss/1.0/modules/content/" '
               'xmlns:wfw="http://wellformedweb.org/CommentAPI/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wp="http://wordpress.org/export/1.2/">\n'
               f"<channel>\n<title>Neurogenomic</title>\n<link>{SITE}</link>\n<description>Páginas de neurogenomic.cl</description>\n<language>es-CL</language>\n"
               f"<wp:wxr_version>1.2</wp:wxr_version>\n<wp:base_site_url>{SITE}</wp:base_site_url>\n<wp:base_blog_url>{SITE}</wp:base_blog_url>\n"
               "<wp:author><wp:author_id>1</wp:author_id><wp:author_login><![CDATA[neurogenomic]]></wp:author_login>"
               "<wp:author_email><![CDATA[contacto@neurogenomic.cl]]></wp:author_email><wp:author_display_name><![CDATA[Neurogenomic]]></wp:author_display_name>"
               "<wp:author_first_name><![CDATA[]]></wp:author_first_name><wp:author_last_name><![CDATA[]]></wp:author_last_name></wp:author>\n"
               + "".join(items) + "</channel>\n</rss>\n")
        f = outdir / f"{fname}.xml"
        f.write_text(xml, encoding="utf-8")
        import xml.etree.ElementTree as ET
        ET.parse(f)  # el archivo debe ser XML válido
        print("ok", f.name, round(f.stat().st_size / 1048576, 2), "MB")


if __name__ == "__main__":
    main()
