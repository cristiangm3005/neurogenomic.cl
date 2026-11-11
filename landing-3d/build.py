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
    f = HERE / "neurogenomic-landing-3d-elementor.json"
    f.write_text(json.dumps(tpl, ensure_ascii=False, indent=1), encoding="utf-8")
    json.loads(f.read_text(encoding="utf-8"))
    print("ok", len(page) // 1024, "KB")
    build_pages(el_css, zero)


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
        f = out / f"neurogenomic-{name}-elementor.json"
        f.write_text(json.dumps(tpl, ensure_ascii=False, indent=1), encoding="utf-8")
        json.loads(f.read_text(encoding="utf-8"))
        print("ok", name, len(page) // 1024, "KB")
    build_services(d, css, el_css, zero)


def emit(name, title, desc, path, frag, el_css, zero, outdir):
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
        emit(s["slug"], f'{s["nombre"]} · Servicios · Neurogenomic', s["lead"], url, style + body, el_css, zero, outdir)
    cards = "".join(f'<li><a href="/servicios/{s["slug"]}/"><b>S·{s["n"]}</b><h2>{e(s["nombre"])}</h2><p>{e(s["titulo"])}</p>'
                    f'<span>Valida: {e(s["valida"][0].lower() + s["valida"][1:])}</span></a></li>' for s in data)
    graph = [org(d), {"@type": "ItemList", "name": "Servicios de Neurogenomic", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + f"/servicios/{s['slug']}/", "name": s["nombre"]} for i, s in enumerate(data)]}]
    body = (head.replace('href="/servicios/">← <span>Todos los </span>servicios', 'href="/">← <span>Volver a la </span>portada') + '  <main class="lx-pg__main">\n'
            '    <p class="lx-k"><b>Servicios</b> Seis líneas, un método</p>\n    <h1 class="lx-h">Seis servicios. <em>Un framework.</em></h1>\n'
            '    <p class="lx-lead">Cada línea se contrata sola o integrada. Todas usan el mismo método: medir, modelar, construir y verificar.</p>\n'
            f'    <ul class="lx-svcs">{cards}</ul>\n  </main>\n' + foot + "  " + jsonld(graph) + "\n</div>\n")
    emit("servicios", "Servicios · Neurogenomic", "Branding, Business Intelligence, E-commerce, Marketing digital, SEO y Desarrollo web, validados con eye tracking, respuesta galvánica e IA.",
         "/servicios/", style + body, el_css, zero, HERE / "paginas")


if __name__ == "__main__":
    main()
