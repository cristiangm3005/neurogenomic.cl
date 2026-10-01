#!/usr/bin/env python3
"""
Genera la landing B2B de Neurogenomic a partir de landing/src/landing.html.

  python3 landing/build_landing.py [--frames DIR_PNG]

Salidas (en la raíz del repo):
  landing.html                 → usa img/ e img/seq/ (para publicar)
  neurogenomic-landing.html    → un solo archivo: imágenes y fotogramas incrustados

--frames: carpeta con los PNG de render/seq_scene.py (f_000.png… + seq.json). Si se indica,
          convierte los fotogramas a WebP en img/seq/ y actualiza landing/data/seq.json.
"""
import base64, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "landing" / "src" / "landing.html"
DATA = ROOT / "landing" / "data"
SEQ_DIR = ROOT / "img" / "seq"
FORM_ENDPOINT = "https://formsubmit.co/ajax/cristiangm3005@gmail.com"


def convert_frames(src_dir, width=1280, quality=72):
    from PIL import Image
    src_dir = Path(src_dir)
    SEQ_DIR.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    seq = json.loads((src_dir / "seq.json").read_text())
    for i in range(seq["frames"]):
        im = Image.open(src_dir / f"f_{i:03d}.png").convert("RGB")
        if im.width != width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(SEQ_DIR / f"f_{i:03d}.webp", quality=quality, method=6)
    seq["size"] = [width, round(seq["size"][1] * width / seq["size"][0])]
    (DATA / "seq.json").write_text(json.dumps(seq, separators=(",", ":")))
    print("frames:", seq["frames"], "→", SEQ_DIR)


def render(img_base, frames_inline=False):
    s = SRC.read_text(encoding="utf-8")
    seq = (DATA / "seq.json").read_text().strip()
    box = (ROOT / "src" / "data" / "boxes.json").read_text().strip()
    s = s.replace("/*SEQ_DATA*/null", seq).replace("/*BOX_DATA*/null", box)
    s = s.replace("{{ENDPOINT}}", FORM_ENDPOINT).replace("{{IMG}}", img_base)
    if frames_inline:
        n = json.loads(seq)["frames"]
        uris = [data_uri(SEQ_DIR / f"f_{i:03d}.webp") for i in range(n)]
        s = s.replace("/*SEQ_FRAMES*/null", json.dumps(uris))
    assert "{{" not in s, re.findall(r"\{\{[^}]*\}\}", s)[:3]
    return s


def data_uri(path):
    return "data:image/webp;base64," + base64.b64encode(Path(path).read_bytes()).decode()


def inline_images(s):
    """Reemplaza src/srcset/preload de img/… por data URIs (elige la variante ≤ 1300 px)."""
    def best(srcset):
        c = []
        for part in srcset.split(","):
            b = part.split()
            if b:
                c.append((int(b[1][:-1]) if len(b) > 1 else 0, b[0]))
        c.sort()
        return ([x for x in c if x[0] <= 1300] or c[:1])[-1][1]

    def img_tag(m):
        tag = m.group(0)
        ss = re.search(r'srcset="([^"]+)"', tag)
        path = best(ss.group(1)) if ss else re.search(r'src="([^"]+)"', tag).group(1)
        tag = re.sub(r'\s(srcset|sizes)="[^"]*"', "", tag)
        return re.sub(r'src="[^"]+"', f'src="{data_uri(ROOT / path)}"', tag)

    s = re.sub(r"<img [^>]*>", img_tag, s)
    s = re.sub(r'<link rel="preload" as="image"[^>]*>', "", s)
    return s


if __name__ == "__main__":
    if "--frames" in sys.argv:
        convert_frames(sys.argv[sys.argv.index("--frames") + 1])
    (ROOT / "landing.html").write_text(render("img/"), encoding="utf-8")
    solo = inline_images(render("img/", frames_inline=True))
    (ROOT / "neurogenomic-landing.html").write_text(solo, encoding="utf-8")
    print("OK: landing.html, neurogenomic-landing.html (%d KB)" % (len(solo.encode()) // 1024))
