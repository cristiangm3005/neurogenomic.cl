"""Plantilla NATIVA de Elementor Pro (sin widgets HTML) de la página de inicio de Neurogenomic,
con los recursos animados generados en Higgsfield referenciados por marcadores.

Uso: python3 elementor-nativo/build_nativo.py
Salida: elementor-nativo/neurogenomic-inicio-nativo-higgsfield.json

Claves de Motion Effects y Sticky verificadas contra el código de Elementor Pro
(modules/motion-fx/controls-group.php, modules/sticky/module.php); video y fondo de video
contra elementor/elementor (includes/widgets/video.php, includes/controls/groups/background.php).
"""
import hashlib, json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "neurogenomic-inicio-elementor-pro.json")

# ---------------------------------------------------------------- Marca (tokens de src/core/tokens.css)
BG, S1, TX, TX2, LIME = "#0A0B0D", "#111316", "#F2F3F0", "#A0A5B0", "#C8FF00"
LINE, LINE2 = "rgba(255,255,255,0.08)", "rgba(255,255,255,0.16)"
DISP, BODY, MONO = "Anton", "Space Grotesk", "IBM Plex Mono"
CONTACTO, SERVICIOS, TECNOLOGIA = "/contacto/", "/servicios/", "/tecnologia/"

# ---------------------------------------------------------------- Primitivas
_n = [0]


def uid():
    _n[0] += 1
    return hashlib.md5(f"ng-native-{_n[0]}".encode()).hexdigest()[:8]


def rid():
    _n[0] += 1
    return hashlib.md5(f"ng-item-{_n[0]}".encode()).hexdigest()[:7]


def sz(n, unit="px"):
    return {"unit": unit, "size": n, "sizes": []}


def dim(t, r=None, b=None, l=None, unit="px"):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    return {"unit": unit, "top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "isLinked": t == r == b == l}


def gap(n):
    return {"column": str(n), "row": str(n), "isLinked": True, "unit": "px", "size": n}


def link(u):
    return {"url": u, "is_external": "", "nofollow": "", "custom_attributes": ""}


def media(u, alt=""):
    return {"url": u, "id": 0, "alt": alt}


def typo(family, size, size_t=None, size_m=None, weight="400", lh=None, ls=None, tt=None, p="typography"):
    s = {f"{p}_typography": "custom", f"{p}_font_family": family, f"{p}_font_size": sz(size), f"{p}_font_weight": weight}
    if size_t: s[f"{p}_font_size_tablet"] = sz(size_t)
    if size_m: s[f"{p}_font_size_mobile"] = sz(size_m)
    if lh: s[f"{p}_line_height"] = sz(lh, "em")
    if ls is not None: s[f"{p}_letter_spacing"] = sz(ls, "em")
    if tt: s[f"{p}_text_transform"] = tt
    return s


def w(wtype, settings):
    return {"id": uid(), "elType": "widget", "widgetType": wtype, "settings": settings, "elements": [], "isInner": False}


def c(settings, elements, inner=True):
    base = {"content_width": "full"} if inner else {}
    base.update(settings)
    return {"id": uid(), "elType": "container", "isInner": inner, "settings": base, "elements": elements}


# ---------------------------------------------------------------- Movimiento nativo (Pro)
def enter(delay=0, anim="fadeInUp"):
    """Entrance Animation de widget."""
    return {"_animation": anim, "animation_duration": "", "_animation_delay": delay}


def scroll_y(speed=2, direction="", rng=(0, 100), devices=("desktop", "tablet")):
    """Motion Effects › Scrolling › Vertical Scroll (parallax suave)."""
    return {"motion_fx_motion_fx_scrolling": "yes", "motion_fx_translateY_effect": "yes",
            "motion_fx_translateY_direction": direction, "motion_fx_translateY_speed": {"unit": "px", "size": speed, "sizes": []},
            "motion_fx_translateY_affectedRange": {"unit": "%", "size": "", "sizes": {"start": rng[0], "end": rng[1]}},
            "motion_fx_devices": list(devices)}


def fade_out(level=10, rng=(50, 100)):
    """Motion Effects › Scrolling › Transparency (Fade Out). Se suma a scroll_y."""
    return {"motion_fx_motion_fx_scrolling": "yes", "motion_fx_opacity_effect": "yes", "motion_fx_opacity_direction": "in-out",
            "motion_fx_opacity_level": {"unit": "px", "size": level, "sizes": []},
            "motion_fx_opacity_range": {"unit": "%", "size": "", "sizes": {"start": rng[0], "end": rng[1]}}}


def scroll_x(speed=2, direction=""):
    return {"motion_fx_motion_fx_scrolling": "yes", "motion_fx_translateX_effect": "yes", "motion_fx_translateX_direction": direction,
            "motion_fx_translateX_speed": {"unit": "px", "size": speed, "sizes": []},
            "motion_fx_translateX_affectedRange": {"unit": "%", "size": "", "sizes": {"start": 0, "end": 100}},
            "motion_fx_devices": ["desktop", "tablet"]}


def mouse_track(speed=0.6):
    return {"motion_fx_motion_fx_mouse": "yes", "motion_fx_mouseTrack_effect": "yes", "motion_fx_mouseTrack_direction": "negative",
            "motion_fx_mouseTrack_speed": {"unit": "px", "size": speed, "sizes": []}}


def tilt(speed=2):
    return {"motion_fx_motion_fx_mouse": "yes", "motion_fx_tilt_effect": "yes", "motion_fx_tilt_direction": "",
            "motion_fx_tilt_speed": {"unit": "px", "size": speed, "sizes": []}}


# ---------------------------------------------------------------- Widgets con la tipografía de marca
def mono(text, color=LIME, size=12, align="left", **kw):
    s = {"title": text, "header_size": "p", "align": align, "title_color": color, **typo(MONO, size, None, 11, "500", 1.5, 0.12, "uppercase")}
    s.update(kw)
    return w("heading", s)


def display(text, tag="h2", size=96, size_t=64, size_m=44, color=TX, align="left", **kw):
    s = {"title": text, "header_size": tag, "align": align, "title_color": color, **typo(DISP, size, size_t, size_m, "400", 0.96, 0, "uppercase")}
    s.update(kw)
    return w("heading", s)


def title(text, tag="h3", size=26, size_m=22, color=TX, weight="600", **kw):
    s = {"title": text, "header_size": tag, "title_color": color, **typo(BODY, size, None, size_m, weight, 1.15, -0.01)}
    s.update(kw)
    return w("heading", s)


def para(html, color=TX2, size=18, size_m=16, weight="300", **kw):
    s = {"editor": html, "text_color": color, **typo(BODY, size, None, size_m, weight, 1.55)}
    s.update(kw)
    return w("text-editor", s)


def btn(text, href, primary=True, **kw):
    s = {"text": text, "link": link(href), "size": "md", "align_mobile": "justify",
         **typo(BODY, 15, None, None, "600", 1, 0.02),
         "border_border": "solid", "border_width": dim(1),
         "border_radius": dim(6), "text_padding": dim(16, 26, 16, 26)}
    if primary:
        s.update({"button_text_color": BG, "background_color": LIME, "border_color": LIME,
                  "hover_color": BG, "button_background_hover_color": "#D9FF4D", "button_hover_border_color": "#D9FF4D",
                  "hover_animation": "float"})
    else:
        s.update({"button_text_color": TX, "background_color": "rgba(0,0,0,0)", "border_color": LINE2,
                  "hover_color": BG, "button_background_hover_color": TX, "button_hover_border_color": TX})
    s.update(kw)
    return w("button", s)


def pill(text):
    """Etiqueta con borde (chip): heading con fondo/borde por Advanced, sin estilos inline."""
    return w("heading", {"title": text, "header_size": "span", "title_color": TX, **typo(MONO, 12, None, 11, "500", 1.2, 0.08, "uppercase"),
                         "_element_width": "auto", "_padding": dim(8, 14, 8, 14), "_border_border": "solid", "_border_width": dim(1),
                         "_border_color": LINE2, "_border_radius": dim(999)})


def pills(items, **kw):
    return c({"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(8), "flex_align_items": "center", **kw}, [pill(t) for t in items])


def note(text, **kw):
    return para(f"<p>{text}</p>", color=TX2, size=13, size_m=13, weight="400", **kw)


def section(sid, label, elements, pad=(120, 120), bg=BG, extra=None, inner_gap=40, min_h=None):
    s = {"_title": label, "_element_id": sid, "content_width": "boxed", "boxed_width": sz(1360),
         "flex_direction": "column", "flex_gap": gap(inner_gap), "flex_gap_mobile": gap(28),
         "padding": dim(pad[0], 40, pad[1], 40), "padding_tablet": dim(88, 28, 88, 28), "padding_mobile": dim(64, 16, 64, 16),
         "background_background": "classic", "background_color": bg,
         "border_border": "solid", "border_width": dim(1, 0, 0, 0), "border_color": LINE}
    if min_h: s["min_height"] = sz(min_h, "vh")
    if extra: s.update(extra)
    return c(s, elements, inner=False)


IMG = "https://raw.githubusercontent.com/cristiangm3005/neurogenomic.cl/8b3e2a5c17b57e69194a56346bd894c6b3d7f52d/img/"


def img(name):
    return IMG + name


def bg_scroll(name, name_m, overlay=0.82, pos="center center"):
    """Fondo de imagen del contenedor (escritorio + móvil) con Motion Effects de fondo:
    parallax vertical y zoom al hacer scroll, y un leve seguimiento del mouse. El degradado deja legible el texto."""
    return {"overflow": "hidden", "background_background": "classic", "background_image": media(img(name)), "background_image_mobile": media(img(name_m)),
            "background_position": pos, "background_position_mobile": "center center", "background_size": "cover",
            "background_repeat": "no-repeat",
            "background_overlay_background": "gradient", "background_overlay_color": BG, "background_overlay_color_stop": sz(0, "%"),
            "background_overlay_color_b": "rgba(10,11,13,0.25)", "background_overlay_color_b_stop": sz(75, "%"),
            "background_overlay_gradient_angle": {"unit": "deg", "size": 90, "sizes": []},
            "background_overlay_opacity": {"unit": "px", "size": overlay, "sizes": []},
            "background_motion_fx_motion_fx_scrolling": "yes",
            "background_motion_fx_translateY_effect": "yes", "background_motion_fx_translateY_direction": "",
            "background_motion_fx_translateY_speed": {"unit": "px", "size": 3, "sizes": []},
            "background_motion_fx_translateY_affectedRange": {"unit": "%", "size": "", "sizes": {"start": 0, "end": 100}},
            "background_motion_fx_scale_effect": "yes", "background_motion_fx_scale_direction": "out-in",
            "background_motion_fx_scale_speed": {"unit": "px", "size": 3, "sizes": []},
            "background_motion_fx_scale_range": {"unit": "%", "size": "", "sizes": {"start": 0, "end": 100}},
            "background_motion_fx_devices": ["desktop", "tablet", "mobile"],
            "background_motion_fx_motion_fx_mouse": "yes", "background_motion_fx_mouseTrack_effect": "yes",
            "background_motion_fx_mouseTrack_direction": "negative",
            "background_motion_fx_mouseTrack_speed": {"unit": "px", "size": 0.6, "sizes": []},
            # En móvil el texto ocupa todo el ancho: oscurecido vertical parejo en vez del degradado lateral
            # La capa del parallax de fondo se pinta encima del degradado: se reordena para que el texto siempre sea legible
            "custom_css": "selector::before,selector>.elementor-background-overlay{z-index:1!important}selector>.e-con-inner{position:relative;z-index:2}"
                          "@media (max-width:767px){selector::before,selector>.elementor-background-overlay{background-image:linear-gradient(180deg,rgba(10,11,13,.4) 0%,rgba(10,11,13,.85) 100%)!important;opacity:1!important}}"}


def reveal(base, top, alt_base, alt_top, extra=None):
    """Dos imágenes alineadas: la foto y, encima, la misma foto con el mapa de calor, que aparece con el scroll
    (Motion Effects › Transparency › Fade In). Es la versión nativa del comparador del sitio."""
    under = w("image", {"image": media(img(base), alt_base), "image_size": "full", "width": sz(100, "%"),
                        "image_border_radius": dim(6)})
    over = w("image", {"image": media(img(top), alt_top), "image_size": "full", "width": sz(100, "%"), "image_border_radius": dim(6),
                       "_position": "absolute", "_offset_orientation_h": "start", "_offset_x": sz(0), "_offset_orientation_v": "start",
                       "_offset_y": sz(0), "_element_width": "initial", "_element_custom_width": sz(100, "%"), "_z_index": 2,
                       "motion_fx_motion_fx_scrolling": "yes", "motion_fx_opacity_effect": "yes", "motion_fx_opacity_direction": "out-in",
                       "motion_fx_opacity_level": {"unit": "px", "size": 10, "sizes": []},
                       "motion_fx_opacity_range": {"unit": "%", "size": "", "sizes": {"start": 15, "end": 55}},
                       "motion_fx_devices": ["desktop", "tablet", "mobile"]})
    s = {"flex_direction": "column", "overflow": "hidden", "border_border": "solid", "border_width": dim(1), "border_color": LINE,
         "border_radius": dim(6), "animation": "fadeInUp"}
    s.update(extra or {})
    return c(s, [under, over])


def steps(items, delay0=0):
    """Fila de 4 ítems numerados (capítulos): 23% → 48% → 100%."""
    cards = []
    for i, (n, t) in enumerate(items):
        cards.append(c({"width": sz(23, "%"), "width_tablet": sz(48, "%"), "width_mobile": sz(100, "%"), "flex_direction": "column",
                        "flex_gap": gap(8), "padding": dim(18, 0, 0, 0), "border_border": "solid", "border_width": dim(1, 0, 0, 0),
                        "border_color": LINE2, "border_hover_border": "solid", "border_hover_width": dim(1, 0, 0, 0),
                        "border_hover_color": LIME, "border_hover_transition": {"unit": "px", "size": 0.3, "sizes": []},
                        "animation": "fadeInUp", "animation_delay": delay0 + i * 120},
                       [mono(n), para(f"<p>{t}</p>", color=TX, size=16, size_m=15, weight="400")]))
    return c({"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(24), "flex_align_items": "stretch"}, cards)


def chapter(sid, label, kicker, h, text, after, bgimg, bgimg_m):
    return section(sid, label, [
        mono(kicker, **enter(0)),
        display(h, size=104, size_t=68, size_m=42, **enter(100), _element_width="initial", _element_custom_width=sz(1100),
                _element_custom_width_mobile=sz(100, "%"), **scroll_y(1.5)),
        para(f"<p>{text}</p>", color=TX, size=20, size_m=17, **enter(200), _element_width="initial", _element_custom_width=sz(760),
             _element_custom_width_mobile=sz(100, "%")),
        *after,
    ], pad=(160, 160), min_h=100, extra={**bg_scroll(bgimg, bgimg_m), "flex_justify_content": "center"})


def card(children, wd=31, wd_t=48, delay=0, href=None):
    s = {"width": sz(wd, "%"), "width_tablet": sz(wd_t, "%"), "width_mobile": sz(100, "%"), "_flex_align_self": "stretch",
         "flex_direction": "column", "flex_gap": gap(12), "padding": dim(28), "padding_mobile": dim(22),
         "background_background": "classic", "background_color": S1,
         "border_border": "solid", "border_width": dim(1), "border_color": LINE, "border_radius": dim(6),
         "border_hover_border": "solid", "border_hover_width": dim(1), "border_hover_color": LIME,
         "border_hover_transition": {"unit": "px", "size": 0.3, "sizes": []},
         "animation": "fadeInUp", "animation_delay": delay}
    if href:
        s.update({"html_tag": "a", "link": link(href)})
    return c(s, children)


def grid(cards, gp=20, fixed=False):
    """fixed=True: una sola fila de columnas (nowrap) que se apila en tablet y móvil (R6b.1); si no, grilla con wrap."""
    if fixed:
        return c({"flex_direction": "row", "flex_wrap": "nowrap", "flex_direction_tablet": "column", "flex_direction_mobile": "column",
                  "flex_gap": gap(gp), "flex_align_items": "stretch"}, cards)
    return c({"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(gp), "flex_align_items": "stretch"}, cards)


def head(n, h, text=None, h_size=88):
    out = [mono(n, **enter(0)), display(h, size=h_size, size_t=60, size_m=40, **enter(100))]
    if text:
        out.append(para(f"<p>{text}</p>", **enter(200), _element_width="initial", _element_custom_width=sz(760),
                        _element_custom_width_mobile=sz(100, "%")))
    return out


def two(left, right, wl=48, wr=48, align="center"):
    return c({"flex_direction": "row", "flex_wrap": "nowrap", "flex_direction_tablet": "column", "flex_direction_mobile": "column", "flex_gap": gap(56),
              "flex_gap_mobile": gap(28), "flex_align_items": align},
             [c({"width": sz(wl, "%"), "width_tablet": sz(100, "%"), "flex_direction": "column", "flex_gap": gap(24)}, left),
              c({"width": sz(wr, "%"), "width_tablet": sz(100, "%"), "flex_direction": "column", "flex_gap": gap(16)}, right)])


def checklist(items, icon, icon_color, tag_text, tag_color):
    rows = []
    for code, t in items:
        rows.append(c({"flex_direction": "row", "flex_wrap": "nowrap", "flex_gap": gap(14), "flex_align_items": "center",
                       "padding": dim(14, 0, 14, 0), "border_border": "solid", "border_width": dim(0, 0, 1, 0), "border_color": LINE},
                      [w("icon", {"selected_icon": {"value": icon, "library": "fa-solid"}, "primary_color": icon_color, "size": sz(14),
                                  "_element_width": "auto"}),
                       mono(code, color=TX2, _element_width="auto", hide_mobile="hidden-mobile"),
                       w("heading", {"title": t, "header_size": "p", "title_color": TX, **typo(BODY, 16, None, 15, "400", 1.35),
                                     "_flex_size": "custom", "_flex_grow": 1, "_flex_shrink": 1}),
                       mono(tag_text, color=tag_color, align="right", _element_width="auto")]))
    return rows


# ================================================================ PÁGINA
content = []

# ---- Encabezado: sticky, con fondo que aparece al hacer scroll (sticky_effects_offset + Custom CSS)
links = [("Inicio", "#inicio"), ("Servicios", "#servicios"), ("Tecnología", "#tecnologia"), ("Ética", "#etica"), ("Contacto", "#contacto-cta")]
menu_html = "<p>" + "<br>".join(f'<a href="{u}">{t}</a>' for t, u in links) + "<br><br>" + "<br>".join(
    f'<a href="{u}">{t} ↘</a>' for t, u in [("Así mira tu cliente", "#asi-mira"), ("Packaging", "#packaging"),
                                            ("Señales y herramientas", "#tecnologia"), ("Caso", "#caso")]) + "</p>"
content.append(c({
    "_title": "Encabezado (sticky)", "content_width": "boxed", "boxed_width": sz(1360), "flex_direction": "row", "flex_wrap": "nowrap",
    "flex_justify_content": "space-between", "flex_align_items": "center", "flex_gap": gap(24),
    "padding": dim(18, 40, 18, 40), "padding_tablet": dim(14, 28, 14, 28), "padding_mobile": dim(12, 16, 12, 16),
    "background_background": "classic", "background_color": "rgba(10,11,13,0)", "z_index": 100,
    "sticky": "top", "sticky_on": ["desktop", "tablet", "mobile"], "sticky_offset": 0, "sticky_effects_offset": 80,
    "custom_css": "selector{transition:background-color .35s ease,border-color .35s ease;border-bottom:1px solid transparent}\n"
                  "selector.elementor-sticky--effects{background-color:rgba(10,11,13,.94)!important;border-bottom-color:rgba(255,255,255,.08)}",
}, [
    w("heading", {"title": "NEUROGENOMIC", "header_size": "div", "link": link("#inicio"), "title_color": TX,
                  **typo(DISP, 28, None, 22, "400", 1, 0.02, "uppercase"), "_element_width": "auto"}),
    c({"flex_direction": "row", "flex_wrap": "nowrap", "flex_gap": gap(28), "flex_align_items": "center",
       "width": sz(52, "%"), "flex_justify_content": "center", "hide_mobile": "hidden-mobile", "hide_tablet": "hidden-tablet"},
      [w("heading", {"title": t, "header_size": "span", "link": link(u), "title_color": TX, **typo(BODY, 15, None, None, "500", 1),
                     "_element_width": "auto", "custom_css": "selector a:hover{color:%s}" % LIME}) for t, u in links]),
    btn("Empieza hoy ↗", CONTACTO, True, size="sm", hide_mobile="hidden-mobile", hover_animation="",
        text_padding=dim(12, 20, 12, 20), _element_width="auto"),
    w("toggle", {"tabs": [{"_id": rid(), "tab_title": "Menú", "tab_content": menu_html}],
                 "selected_icon": {"value": "fas fa-bars", "library": "fa-solid"},
                 "selected_active_icon": {"value": "fas fa-times", "library": "fa-solid"}, "title_html_tag": "div",
                 "hide_desktop": "hidden-desktop", "hide_tablet": "", "_element_width": "auto",
                 "title_color": TX, "tab_active_color": LIME, "content_color": TX, "icon_color": LIME, "icon_active_color": LIME,
                 "border_width": sz(0), "title_background": "rgba(0,0,0,0)", "content_background_color": BG,
                 **typo(BODY, 15, None, None, "600", 1, p="title_typography"),
                 **typo(BODY, 18, None, None, "500", 2.2, p="content_typography")}),
], inner=False))

# ---- 01 Hero (video V01)
content.append(section("inicio", "Hero · imagen 1", [
    c({"flex_direction": "row", "flex_wrap": "nowrap", "flex_justify_content": "space-between", "flex_direction_mobile": "column",
       "flex_gap": gap(16)},
      [mono("REC · Neurona · sinapsis activa", color=TX, _element_width="auto"),
       mono("Neurociencia + IA para decidir con evidencia", color=TX2, align="right", _element_width="auto", hide_mobile="hidden-mobile")]),
    c({"flex_direction": "row", "flex_wrap": "nowrap", "flex_direction_tablet": "column", "flex_direction_mobile": "column", "flex_align_items": "flex-end",
       "flex_gap": gap(48), "flex_gap_mobile": gap(28)}, [
        c({"width": sz(68, "%"), "width_tablet": sz(100, "%"), "flex_direction": "column", "flex_gap": gap(24)}, [
            mono("Neuroscience-Driven Marketing Optimization", size=14, **enter(0)),
            w("heading", {"title": "El marketing<br>digital <span>cambió.</span>", "header_size": "h1", "title_color": TX,
                          **typo(DISP, 176, 112, 60, "400", 0.96, 0, "uppercase"),
                          "custom_css": "selector span{color:%s}" % LIME, **enter(150), **scroll_y(3), **fade_out(10, (45, 100))}),
            para("<p>Neuromarketing potenciado por inteligencia artificial.</p>", color=TX, size=24, size_m=19, weight="500", **enter(300)),
            para("<p>Analizamos procesos cerebrales subconscientes y los potenciamos con modelos predictivos para maximizar la conversión.</p>",
                 **enter(400), _element_width="initial", _element_custom_width=sz(640), _element_custom_width_mobile=sz(100, "%")),
            c({"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(12), "flex_direction_mobile": "column", "animation": "fadeInUp",
               "animation_delay": 500},
              [btn("Empieza hoy ↗", CONTACTO, True), btn("Así mira tu cliente ↓", "#asi-mira", False)]),
            mono("Eye tracking · GSR · Facial coding", color=TX2, **enter(600)),
        ]),
        c({"width": sz(28, "%"), "width_tablet": sz(100, "%"), "flex_direction": "column", "padding": dim(0, 0, 0, 20),
           "border_border": "solid", "border_width": dim(0, 0, 0, 6), "border_color": TX},
          [display("Todos miran.<br>Nosotros medimos.", tag="p", size=46, size_t=40, size_m=30, color=LIME,
                   **enter(700, "fadeIn"), **mouse_track(0.6))]),
    ]),
], pad=(140, 72), min_h=92, extra={**bg_scroll("el/el-hero.webp", "el/el-hero-movil.webp", 0.7),
                                   "flex_justify_content": "space-between", "border_width": dim(0)}))

# ---- Capítulo 01 (video V02)
content.append(chapter("cap-neurona", "Capítulo 01 · imagen 2", "Capítulo 01 / 05 · Origen neuronal",
                       "Cada decisión empieza antes de las palabras.",
                       "Percepción, atención y emoción se activan en milisegundos, muchas veces antes de que una persona pueda explicar por qué prefiere algo. Las decisiones de compra nacen de esos procesos cognitivos y emocionales. Ahí comienza nuestro trabajo.",
                       [steps([("01 Percepción", "Qué se detecta primero"), ("02 Atención", "Dónde se queda la mirada"),
                               ("03 Emoción", "Qué genera una reacción"), ("04 Decisión", "Qué inclina la elección")], 300)],
                       "el/el-cap1.webp", "el/el-cap1-movil.webp"))

# ---- Capítulo 02 (video V03)
content.append(chapter("cap-senales", "Capítulo 02 · imagen 3", "Capítulo 02 / 05 · Señales y comportamiento",
                       "De impulsos a señales medibles.",
                       "Con consentimiento informado, registramos mirada, expresión facial y respuesta electrodérmica. Neurogenomic interpreta esos datos neuroconductuales para reconocer señales asociadas a atención, emoción, motivación, preferencia e intención de compra.",
                       [pills(["Atención", "Emoción", "Motivación", "Preferencia", "Intención de compra"], animation="fadeInUp", animation_delay=300),
                        note("Las señales describen reacciones del grupo estudiado; no leen pensamientos ni identifican a personas.")],
                       "el/el-cap2.webp", "el/el-cap2-movil.webp"))

# ---- 01 Así mira tu cliente (video destacado V04)
cols = [("Qué se mide", "Dónde se detiene la mirada, en qué orden y cómo varía la activación."),
        ("Qué revela", "Qué elementos captan atención, cuáles se ignoran y dónde sube la activación."),
        ("Qué decisión permite", "Priorizar, ajustar o descartar elementos antes de producir.")]
content.append(section("asi-mira", "01 · Así mira tu cliente · imagen 4", [
    *head("01 · Eye tracking + IA", "Así mira tu cliente"),
    grid([card([mono(a, color=TX2), para(f"<p>{b}</p>", color=TX, size=17, size_m=16, weight="400")], 31, 100, i * 120)
          for i, (a, b) in enumerate(cols)], fixed=True),
    reveal("el/el-demo-clean.webp", "el/el-demo-heat.webp", "Bolsa de café de una marca ficticia sobre una mesa oscura",
           "La misma bolsa con fijaciones de mirada, recorrido y mapa de calor simulados sobre la marca y el origen"),
    note("Demostración visual. No corresponde a datos de un estudio real."),
]))

# ---- 02 Packaging (video destacado V05)
zones = [("01 Tapa", "Primera fijación"), ("02 Etiqueta", "Permanencia alta"), ("03 Hombro y cuello", "Revisitas"), ("04 Base", "Mirada breve")]
content.append(section("packaging", "02 · Packaging · imagen 5", [
    two([*head("02 · Inteligencia biométrica", "Tu packaging tiene una mirada para ganar.",
               "Mira lo que tus compradores realmente observan antes de comprar.", 80),
         *[c({"flex_direction": "row", "flex_wrap": "nowrap", "flex_direction_mobile": "column", "flex_justify_content": "space-between",
              "flex_gap": gap(16), "flex_gap_mobile": gap(4),
              "padding": dim(14, 0, 14, 0), "border_border": "solid", "border_width": dim(0, 0, 1, 0), "border_color": LINE,
              "animation": "fadeInUp", "animation_delay": 200 + i * 100},
             [title(a, "h3", 18, 16, _element_width="auto"), mono(b, color=TX2, align="right", align_mobile="left", _element_width="auto")])
           for i, (a, b) in enumerate(zones)],
         mono("Eye tracking · Respuesta GSR · Facial coding", color=TX2)],
        [mono("Eye tracking · packaging · Ilustrativo", color=TX2),
         reveal("el/el-botella-foto.webp", "el/el-botella-heat.webp", "Botella de bebida sin marca con etiqueta negra",
                "La misma botella con un mapa de calor de mirada: más atención en la etiqueta, luego la tapa y el hombro"),
         note("Demostración visual. No corresponde a datos de un estudio real.")], 46, 50),
]))

# ---- 03 Lo que no se dice
content.append(section("lo-que-no-se-dice", "03 · Señal no consciente", [
    *head("03 · Señal no consciente", "Lo que no se dice sí se mide.",
          "Una encuesta recoge lo que la persona cree que siente. La mirada, el gesto y la piel registran lo que realmente pasa, antes de que lo pueda explicar."),
]))

# ---- Capítulo 03 (video V06)
content.append(chapter("cap-datos", "Capítulo 03 · imagen 6", "Capítulo 03 / 05 · Centro de datos e IA",
                       "La IA encuentra patrones en los datos.",
                       "Los flujos de datos llegan a una arquitectura donde modelos de inteligencia artificial sincronizan señales, las depuran y las cruzan con información de negocio para detectar patrones de consumo, segmentar audiencias y anticipar qué alternativa tiene más probabilidad de funcionar.",
                       [steps([("01 Precisión", "Señales sincronizadas y depuradas"), ("02 Análisis predictivo", "Escenarios antes de invertir"),
                               ("03 Automatización", "Reportes y dashboards al día"), ("04 Ética", "Resultados agregados, nunca perfiles individuales")], 300)],
                       "el/el-cap3.webp", "el/el-cap3-movil.webp"))

# ---- 04 Tecnología
signals = [("C·01 · Eye tracking", "Señal 01", "Atención", "Dónde mira, en qué orden y qué ignora por completo."),
           ("C·02 · Facial coding", "Señal 02", "Emoción", "La microexpresión que aparece antes de que piense la respuesta."),
           ("C·03 · Respuesta galvánica", "Señal 03", "Activación", "La intensidad de la reacción, aunque el rostro se mantenga neutro.")]
tools = [("01 · Captura", "Experimentos y señales", "Diseño del estímulo, registro de mirada, rostro y piel.",
          "Tobii Pro Lab · iMotions · Pupil Labs · PsychoPy · OpenFace · MediaPipe · OpenCV"),
         ("02 · Datos", "Limpieza y estructura", "Sincronización de señales, depuración y bases consultables.",
          "Python · SQL · PostgreSQL · BigQuery · pandas · NumPy · SciPy · R · Jupyter · Git · Docker"),
         ("03 · Modelos", "Análisis e IA", "Procesamiento de señales, estadística y modelos predictivos.",
          "NeuroKit2 · scikit-learn · PyTorch · TensorFlow · Hugging Face · statsmodels · XGBoost"),
         ("04 · Decisión", "Visualización y activación", "Reportes, dashboards y la implementación en tus canales.",
          "Power BI · Tableau · Looker Studio · Plotly · Matplotlib · Google Analytics 4 · Figma · WordPress · Shopify · React")]
content.append(section("tecnologia", "04 · Tecnología", [
    *head("04 · Tecnología", "Tres señales que no dependen de lo que se declara.",
          "Eye tracking, facial coding y respuesta galvánica, cruzados con modelos de IA propios, para convertir reacciones no conscientes en una decisión validada antes de construir."),
    grid([card([mono(a), mono(b, color=TX2), title(t, "h3", 34, 26), para(f"<p>{d}</p>", size=16, size_m=15)], 31, 100, i * 120)
          for i, (a, b, t, d) in enumerate(signals)], fixed=True),
    title("Las herramientas detrás del dato.", "h3", 40, 28, **enter(0)),
    para("<p>De la señal cruda a la decisión: el software con el que capturamos, procesamos, modelamos y mostramos cada estudio.</p>", **enter(100)),
    grid([card([mono(a), title(t, "h4", 20, 18), para(f"<p>{d}</p>", size=15, size_m=15),
                para(f"<p>{tags}</p>", color=TX, size=13, size_m=13, weight="400")], 22.5, 48, i * 100)
          for i, (a, t, d, tags) in enumerate(tools)], 16),
    note("Herramientas de referencia: el stack se ajusta a cada proyecto."),
]))

# ---- 05 Ética
trust = [("fas fa-file-signature", "Consentimiento informado", "Cada participante sabe qué se mide, para qué y puede retirarse cuando quiera."),
         ("fas fa-user-secret", "Seudonimización", "Las señales se guardan con un código, separadas del nombre y de los datos de contacto."),
         ("fas fa-lock", "Acceso restringido", "Solo el equipo del estudio accede a los registros, con permisos por proyecto."),
         ("fas fa-users", "Resultados agregados", "Entregamos patrones del grupo, nunca perfiles de personas individuales."),
         ("fas fa-hourglass-half", "Retención definida", "Acordamos con el cliente cuánto tiempo se conservan los datos y cuándo se eliminan.")]
ib = lambda ic, t, d, i: w("icon-box", {
    "selected_icon": {"value": ic, "library": "fa-solid"}, "view": "default", "position": "top", "title_text": t, "description_text": d,
    "title_size": "h4", "primary_color": LIME, "icon_size": sz(22), "icon_space": sz(14), "text_align": "left", "title_color": TX,
    "description_color": TX2, **typo(BODY, 18, None, 17, "600", 1.25, p="title_typography"),
    **typo(BODY, 15, None, None, "300", 1.5, p="description_typography"),
    "_element_width": "initial", "_element_custom_width": sz(18, "%"), "_element_custom_width_tablet": sz(48, "%"),
    "_element_custom_width_mobile": sz(100, "%"), **enter(i * 100)})
content.append(section("etica", "05 · Ética y datos", [
    *head("05 · Ética y datos", "Medimos reacciones. Con reglas claras.",
          "Una señal biométrica es un dato sensible. Por eso cada estudio parte con consentimiento informado, usa solo los datos necesarios y entrega resultados agregados, no perfiles individuales."),
    mono("Centro de confianza · Cómo tratamos los datos biométricos", color=TX2),
    c({"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(20), "flex_align_items": "stretch"},
      [ib(*t, i) for i, t in enumerate(trust)]),
    two([mono("Protocolo · Lo que cumplimos", color=TX2),
         *checklist([("C·01", "Consentimiento que se entiende"), ("C·02", "Acceso restringido y datos separados de la identidad"),
                     ("C·03", "Revisión legal de cada proyecto según su jurisdicción"), ("C·04", "Derecho a salir, siempre")],
                    "fas fa-check-circle", LIME, "OK", LIME)],
        [mono("Líneas rojas · Lo que no hacemos", color=TX2),
         *checklist([("R·01", "No vendemos datos"), ("R·02", "No perfilamos individuos"), ("R·03", "No diseñamos manipulación"),
                     ("R·04", "No medimos a menores sin resguardo")], "fas fa-ban", "#FF6B5B", "Bloqueado", "#FF8A7D")], 48, 48, "flex-start"),
    note("Las obligaciones legales dependen del tipo de estudio, los datos tratados, la ubicación de los participantes y la jurisdicción aplicable. Recomendamos revisar cada proyecto con asesoría legal especializada. Mencionar la Ley 21.719 no constituye una certificación de cumplimiento."),
]))

# ---- Capítulo 04 (video V07)
content.append(chapter("cap-estrategia", "Capítulo 04 · imagen 7", "Capítulo 04 / 05 · Del insight a la estrategia",
                       "Del insight a la estrategia.",
                       "La IA convierte los datos en rutas y mapas de decisión: qué mensaje priorizar, qué diseño producir, a qué segmento hablarle y qué experiencia ajustar. Así el conocimiento científico y tecnológico se transforma en decisiones de marketing.",
                       [pills(["Neuromarketing", "Branding", "Comunicación", "Experiencia de usuario", "Optimización comercial", "Personalización"],
                              animation="fadeInUp", animation_delay=300)],
                       "el/el-cap4.webp", "el/el-cap4-movil.webp"))

# ---- 06 Servicios
svcs = [("S·01", "Branding", "Nombre, color, tono y símbolo probados contra la reacción del público antes de lanzar.", "Qué propuesta de marca desarrollar.", "svc-branding"),
        ("S·02", "Business Intelligence", "Datos biométricos, de negocio y de comportamiento digital en un solo tablero.", "Qué hallazgos priorizar.", "svc-bi"),
        ("S·03", "E-commerce", "Fichas, carrito y checkout rediseñados a partir de dónde se traba la mirada del usuario.", "Qué fricción resolver primero.", "svc-ecommerce"),
        ("S·04", "Marketing digital", "Pre-test biométrico de avisos y videos antes de invertir en medios.", "Qué pieza pautar y qué editar.", "svc-marketing"),
        ("S·05", "SEO técnico y de contenido", "Visibilidad en buscadores y en motores de respuesta con IA.", "Qué contenido estructurar primero.", "svc-seo"),
        ("S·06", "Desarrollo de software", "Sitios, apps y automatizaciones con la IA integrada desde la arquitectura.", "Qué flujo construir y cómo.", "svc-software")]
content.append(section("servicios", "06 · Servicios", [
    *head("06 · Servicios", "Seis servicios. Un framework.",
          "Cada línea se puede contratar sola o integrada. La medición biométrica y el análisis con IA conectan todas."),
    grid([card([mono(f"{n} →"), title(t, "h3", 26, 22), para(f"<p>{d}</p>", size=16, size_m=15),
                mono("Decisión que valida", color=TX2), para(f"<p>{dec}</p>", color=TX, size=15, size_m=15, weight="500")],
               31, 48, (i % 3) * 120, SERVICIOS + "#" + a) for i, (n, t, d, dec, a) in enumerate(svcs)]),
    pills(["Eye tracking", "Facial coding", "Respuesta galvánica", "Análisis con IA"]),
    btn("Ver el detalle de cada servicio →", SERVICIOS, False, _element_width="auto"),
    display("Branding ◆ Business Intelligence ◆ E-commerce ◆ Marketing digital ◆ SEO ◆ Desarrollo de software ◆", tag="p",
            size=64, size_t=48, size_m=32, color=TX2, **scroll_x(3)),
], extra={"overflow": "hidden"}))

# ---- 07 Método
met = [("01", "Medir", "Biometría aplicada sobre el estímulo, la marca o el flujo actual: eye tracking, codificación facial, respuesta galvánica."),
       ("02", "Modelar", "La IA cruza mirada, gesto y piel con datos de negocio para identificar patrones y anticipar la respuesta del consumidor."),
       ("03", "Construir", "Diseño, contenido o producto se ejecutan sobre las opciones ya validadas, no sobre la primera idea que pareció correcta."),
       ("04", "Verificar", "Cada entregable se vuelve a testear contra el comportamiento real antes y después de salir a producción.")]
content.append(section("metodo", "07 · Método", [
    *head("07 · Método", "Un proceso, seis aplicaciones."),
    btn("Ver los seis servicios →", SERVICIOS, False, _element_width="auto"),
    grid([card([display(n, tag="p", size=72, size_t=60, size_m=48, color=LIME), title(t, "h3", 28, 22), para(f"<p>{d}</p>", size=16, size_m=15)],
               22.5, 48, i * 120) for i, (n, t, d) in enumerate(met)], 16),
]))

# ---- 08 Caso
case = [("01 · Desafío · Antes", "Votos internos · sin mayoría", "Tres propuestas y un equipo dividido.",
         "Marketing, ventas y diseño defendían versiones distintas. Cada opinión era razonable, pero no había un criterio común para decidir antes de imprimir.",
         ["3 versiones", "Sin consenso", "Riesgo de reimpresión"]),
        ("02 · Aplicación · Medición", "A · B · C", "Una góndola simulada, junto a la competencia.",
         "Las tres versiones se mostraron en su contexto real de compra, rodeadas de otros productos. Cada participante buscó el producto mientras registrábamos su mirada y su expresión facial.",
         ["Eye tracking", "Facial coding", "Orden aleatorio"]),
        ("03 · Resultado · Ilustrativo", "Atención sostenida · Respuesta emocional · Comparación relativa, sin escala", "Una versión ganó en las dos señales.",
         "La versión B concentró más atención sostenida y una respuesta emocional más positiva. El debate se cerró con evidencia compartida, no con jerarquía, y A y C dejaron ideas para ajustar B.",
         ["Ranking por versión", "Heatmaps", "Ajustes recomendados"])]
content.append(section("caso", "08 · Caso", [
    *head("08 · Caso", "Un packaging, tres versiones, una respuesta clara."),
    mono("Marca anonimizada. Representación ilustrativa.", color=TX2),
    grid([card([mono(a), mono(b, color=TX2, size=11), title(t, "h3", 24, 21), para(f"<p>{d}</p>", size=16, size_m=15), pills(tags)],
               31, 100, i * 140) for i, (a, b, t, d, tags) in enumerate(case)], fixed=True),
]))

# ---- Capítulo 05 (video V08)
content.append(chapter("cap-consumidor", "Capítulo 05 · imagen 8", "Capítulo 05 / 05 · Consumidor y experiencia",
                       "Convierte datos en decisiones que conectan.",
                       "Al final del recorrido está una persona. Comprender mejor sus necesidades, intereses y contexto permite ofrecer productos, mensajes y experiencias más relevantes: mejor experiencia de cliente, más conexión entre marca y audiencia y una conversión que se sostiene, sin manipular a nadie.",
                       [steps([("01 Relevancia", "Ofertas que responden a una necesidad real"), ("02 Experiencia", "Menos fricción en cada canal"),
                               ("03 Conexión", "Mensajes que la audiencia reconoce como propios"), ("04 Conversión", "Crecimiento medido con evidencia")], 300),
                        c({"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(12), "flex_direction_mobile": "column"},
                          [btn("Agendar demostración ↗", CONTACTO, True), btn("Solicita una evaluación estratégica →", CONTACTO, False)])],
                       "el/el-cap5.webp", "el/el-cap5-movil.webp"))

# ---- 09 Diagnóstico (CTA + formulario rápido nativo)
form = w("form", {
    "form_name": "Neurogenomic · Diagnóstico rápido",
    "form_fields": [
        {"_id": rid(), "custom_id": "email", "field_type": "email", "field_label": "Correo", "placeholder": "tu@empresa.cl",
         "required": "true", "width": "100"},
        {"_id": rid(), "custom_id": "acepto", "field_type": "acceptance", "field_label": "",
         "acceptance_text": 'Acepto que Neurogenomic use este correo solo para responder mi solicitud (<a href="/privacidad/">privacidad</a>).',
         "required": "true", "width": "100"},
    ],
    "show_labels": "", "input_size": "md", "button_text": "Agendar demo →", "button_size": "md", "button_width": "100",
    "submit_actions": ["email"], "email_to": "cristiangm3005@gmail.com", "email_subject": "Nueva solicitud de demo desde el sitio",
    "email_content": "[all-fields]", "email_from_name": "Neurogenomic web", "email_content_type": "html",
    "success_message": "Gracias. Te escribimos pronto.", "error_message": "No pudimos enviar tu solicitud. Intenta de nuevo.",
    "required_field_message": "Este campo es obligatorio.", "invalid_message": "Revisa el correo ingresado.",
    "field_text_color": TX, "field_background_color": S1, "field_border_color": LINE2, "field_border_radius": dim(6),
    **typo(BODY, 16, None, None, "400", 1.4, p="field_typography"),
    "button_background_color": LIME, "button_text_color": BG, "button_background_hover_color": "#D9FF4D", "button_hover_color": BG,
    "button_border_radius": dim(6), **typo(BODY, 15, None, None, "600", 1, p="button_typography"),
    "html_color": TX2, "label_color": TX2,
})
content.append(section("contacto-cta", "09 · Diagnóstico + formulario", [
    two([*head("09 · Diagnóstico", "¿Construimos tu próxima decisión con evidencia?",
               "Cuéntanos qué quieres evaluar: una marca, una campaña, un packaging o un sitio web. Revisamos el desafío y te proponemos el método adecuado.", 80),
         btn("Agendar diagnóstico ↗", CONTACTO, True, _element_width="auto", **enter(300))],
        [c({"flex_direction": "column", "flex_gap": gap(16), "padding": dim(28), "padding_mobile": dim(20), "background_background": "classic",
            "background_color": S1, "border_border": "solid", "border_width": dim(1), "border_color": LINE, "border_radius": dim(6),
            "animation": "fadeInUp", "animation_delay": 200},
           [title("¿Sin tiempo? Déjanos tu correo y te escribimos", "h3", 22, 19), form]),
         w("image", {"image": media(img("ng-phone-920.webp"), "Teléfono con una tienda online ficticia y un mapa de atención sobre la ficha de producto"),
                     "image_size": "full", "width": sz(70, "%"), "width_mobile": sz(90, "%"), "align": "center",
                     "caption_source": "custom", "caption": "Ilustrativo · tienda ficticia", "caption_color": TX2,
                     **typo(MONO, 11, None, None, "500", 1.4, 0.1, "uppercase", p="caption_typography"),
                     **enter(300), **scroll_y(2, "negative"), "motion_fx_devices": ["desktop", "tablet"]})], 58, 38, "flex-end"),
]))

# ---- Pie de página
foot_col = lambda h, items: c({"width": sz(20, "%"), "width_tablet": sz(31, "%"), "width_mobile": sz(100, "%"), "flex_direction": "column",
                               "flex_gap": gap(4), "flex_align_items_mobile": "center"},
                              [mono(h, color=TX2, align_mobile="center"),
                               w("icon-list", {"icon_list": [{"_id": rid(), "text": t, "link": link(u),
                                                              "selected_icon": {"value": "", "library": ""}} for t, u in items],
                                               "space_between": sz(6), "text_color": TX, "text_color_hover": LIME, "icon_align_mobile": "center",
                                               **typo(BODY, 15, None, None, "400", 2.2, p="icon_typography")})])
content.append(c({
    "_title": "Pie de página", "content_width": "boxed", "boxed_width": sz(1360), "flex_direction": "column", "flex_gap": gap(40),
    "padding": dim(88, 40, 32, 40), "padding_tablet": dim(64, 28, 28, 28), "padding_mobile": dim(48, 16, 24, 16),
    "background_background": "classic", "background_color": BG, "border_border": "solid", "border_width": dim(1, 0, 0, 0), "border_color": LINE,
    "overflow": "hidden",
}, [
    c({"flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(24), "flex_justify_content": "space-between"}, [
        c({"width": sz(28, "%"), "width_tablet": sz(100, "%"), "width_mobile": sz(100, "%"), "flex_direction": "column", "flex_gap": gap(12), "flex_align_items_mobile": "center"},
          [w("heading", {"title": "NEUROGENOMIC", "header_size": "div", "title_color": TX, **typo(DISP, 32, None, 26, "400", 1, 0.02, "uppercase"),
                         "align_mobile": "center"}),
           para("<p>Neuroscience-Driven Marketing Optimization. Una empresa de Genomic Industries SpA.</p>", size=15, size_m=15, align_mobile="center")]),
        foot_col("Empresa", [("Inicio", "/"), ("Servicios", SERVICIOS), ("Tecnología", TECNOLOGIA), ("Contacto", CONTACTO)]),
        foot_col("Servicios", [("Branding", SERVICIOS + "#svc-branding"), ("Business Intelligence", SERVICIOS + "#svc-bi"),
                               ("E-commerce", SERVICIOS + "#svc-ecommerce"), ("Marketing digital", SERVICIOS + "#svc-marketing"),
                               ("SEO", SERVICIOS + "#svc-seo"), ("Desarrollo de software", SERVICIOS + "#svc-software")]),
        foot_col("Contacto", [("LinkedIn", "https://www.linkedin.com/company/neurogenomic-cl/"), ("Privacidad y ética", "/privacidad/"),
                              ("Términos de uso", "/terminos/")]),
    ]),
    display("NEUROGENOMIC", tag="p", size=240, size_t=150, size_m=64, color=S1, align="center", **scroll_x(2, "negative")),
    c({"flex_direction": "row", "flex_wrap": "wrap", "flex_justify_content": "space-between", "flex_direction_mobile": "column",
       "flex_align_items_mobile": "center", "flex_gap": gap(8)},
      [mono("© 2026 Neurogenomic. Todos los derechos reservados.", color=TX2, size=11, _element_width="auto"),
       mono("neurogenomic.cl", color=TX2, size=11, _element_width="auto")]),
], inner=False))

# ---------------------------------------------------------------- Ajustes de página: canvas, fondo y movimiento reducido
PAGE_CSS = """/* Neurogenomic · ajustes globales de la página (Custom CSS de Elementor Pro) */
body{background:#0A0B0D}
html{scroll-behavior:smooth}
a:focus-visible,.elementor-button:focus-visible{outline:2px solid #C8FF00;outline-offset:3px}
/* prefers-reduced-motion: sin entradas ni parallax; el mapa de calor queda visible */
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .elementor-invisible{visibility:visible!important}
  .animated{animation:none!important}
  .elementor-motion-effects-element,.elementor-motion-effects-layer{transform:none!important;opacity:1!important}
  .elementor-button{transition:none!important}
}"""

tpl = {"title": "Neurogenomic · Inicio (Elementor Pro nativo)", "type": "page", "version": "0.4",
       "page_settings": {"template": "elementor_canvas", "hide_title": "yes", "background_background": "classic",
                         "background_color": BG, "custom_css": PAGE_CSS},
       "content": content}

if __name__ == "__main__":
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(tpl, f, ensure_ascii=False, separators=(",", ":"))
    print(OUT, os.path.getsize(OUT), "bytes")
