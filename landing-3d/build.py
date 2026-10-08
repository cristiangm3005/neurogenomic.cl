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
ENDPOINT = "https://formsubmit.co/ajax/cristiangm3005@gmail.com"
FACES = [("Big Shoulders Display", "big-shoulders-display-latin-800-normal", 400),
         ("Schibsted Grotesk", "schibsted-grotesk-latin-400-normal", 400), ("Schibsted Grotesk", "schibsted-grotesk-latin-500-normal", 500),
         ("Schibsted Grotesk", "schibsted-grotesk-latin-600-normal", 600),
         ("Martian Mono", "martian-mono-latin-400-normal", 400), ("Martian Mono", "martian-mono-latin-500-normal", 500)]
TITLE = "Neurogenomic · Neurociencia + IA para decidir con evidencia"
DESC = ("Agencia chilena de neuromarketing: eye tracking, facial coding y respuesta galvánica cruzados con IA "
        "para validar marca, campañas, packaging y e-commerce antes de invertir.")


def fragment():
    s = (HERE / "src" / "landing.html").read_text(encoding="utf-8")
    faces = "".join(
        f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:swap;"
        f"src:url(data:font/woff2;base64,{base64.b64encode((VEND / 'fonts' / (fn + '.woff2')).read_bytes()).decode()}) format('woff2')}}"
        for fam, fn, wt in FACES)
    three = (VEND / "three.min.js").read_text(encoding="utf-8").replace("</script", "<\\/script")
    return (s.replace("{{FONTS}}", faces).replace("{{THREE}}", f"<script>{three}</script>")
             .replace("{{ENDPOINT}}", ENDPOINT).replace("{{CONTACT}}", "/contacto/").replace("{{PRIVACY}}", "/privacidad/"))


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
    f = HERE / "neurogenomic-landing-3d-elementor.json"
    f.write_text(json.dumps(tpl, ensure_ascii=False, indent=1), encoding="utf-8")
    json.loads(f.read_text(encoding="utf-8"))
    print("ok", len(page) // 1024, "KB")


if __name__ == "__main__":
    main()
