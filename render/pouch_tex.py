"""Textura impresa de la bolsa: kraft con fibras + etiqueta de papel algodón + textos laterales."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from pouch import H, TEX_X, W

HERE = os.path.dirname(__file__)
FS = os.environ.get('FONTS_DIR', os.path.join(HERE, 'node_modules', '@fontsource'))
def font(pkg, w, px):
    return ImageFont.truetype(f'{FS}/{pkg}/files/{pkg}-latin-{w}-normal.woff', int(px))

PPM = 9000  # px por metro
TW = int((TEX_X[1] - TEX_X[0]) * PPM); TH = int(H * PPM)
rng = np.random.default_rng(7)

def px(X, Z):
    return ((X - TEX_X[0]) * PPM, (H - Z) * PPM)

def mm(v):
    return v / 1000 * PPM

# ---------- Kraft ----------
def noise(shape, scale):
    small = rng.random((max(2, shape[0] // scale), max(2, shape[1] // scale)))
    return np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((shape[1], shape[0]), Image.BICUBIC), dtype=np.float32) / 255

n1 = noise((TH, TW), 220) * .5 + noise((TH, TW), 40) * .3 + noise((TH, TW), 6) * .2
fib = Image.new('L', (TW, TH), 0); fd = ImageDraw.Draw(fib)
for _ in range(9000):  # fibras de papel
    x, y = rng.random() * TW, rng.random() * TH
    a = rng.normal(0, .35); L = rng.random() * 46 + 8
    fd.line([(x, y), (x + np.cos(a) * L, y + np.sin(a) * L)], fill=int(rng.random() * 120 + 60), width=1)
fib = np.asarray(fib.filter(ImageFilter.GaussianBlur(.6)), dtype=np.float32) / 255
base = np.array([150, 100, 58], np.float32)
col = base[None, None, :] * (0.93 + n1[..., None] * .12) - fib[..., None] * np.array([38, 30, 22])
col += rng.normal(0, 4, (TH, TW, 1))
img = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8), 'RGB')
bump = Image.fromarray(np.clip((n1 * .55 + fib * .6) * 200, 0, 255).astype(np.uint8), 'L')

d = ImageDraw.Draw(img); bd = ImageDraw.Draw(bump)
INK = (24, 22, 20)

# ---------- Etiqueta frontal (96 × 130 mm) ----------
LW, LH = 0.096, 0.130
LZ0 = 0.045                         # borde inferior de la etiqueta
lx0, ly0 = px(-LW / 2, LZ0 + LH)
lx1, ly1 = px(LW / 2, LZ0)
lab = noise((int(ly1 - ly0), int(lx1 - lx0)), 4) * .6 + noise((int(ly1 - ly0), int(lx1 - lx0)), 60) * .4
paper = np.array([238, 232, 219], np.float32)[None, None, :] * (0.975 + lab[..., None] * .035)
img.paste(Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)), (int(lx0), int(ly0)))
bd.rectangle([lx0, ly0, lx1, ly1], fill=150)
bd.rectangle([lx0 - 3, ly0 - 3, lx1 + 3, ly1 + 3], outline=210, width=3)

anchors = {}
def L(xmm, ymm):  # coordenadas dentro de la etiqueta (mm desde arriba-izq) → px textura y (X,Z) en metros
    X = -LW / 2 + xmm / 1000; Z = LZ0 + LH - ymm / 1000
    return px(X, Z), (X, Z)

def text(xmm, ymm, s, f, fill=INK, anchor='mm', track=0, key=None):
    (x, y), XZ = L(xmm, ymm)
    if track:
        ws = [f.getlength(c) for c in s]; tw = sum(ws) + track * (len(s) - 1)
        cx = x - tw / 2 if anchor[0] == 'm' else x
        for c, w_ in zip(s, ws):
            d.text((cx, y), c, font=f, fill=fill, anchor='l' + anchor[1]); cx += w_ + track
    else:
        d.text((x, y), s, font=f, fill=fill, anchor=anchor)
    if key: anchors[key] = XZ

text(48, 20, 'MESTA', font('space-grotesk', 700, mm(13)), track=mm(3.2), key='logo')
text(48, 30.5, 'TOSTADORES · SANTIAGO', font('ibm-plex-mono', 500, mm(2.6)), track=mm(.5))
(rx0, ry), _ = L(14, 36); (rx1, _), _ = L(82, 36); d.line([(rx0, ry), (rx1, ry)], fill=INK, width=4)
text(48, 43, 'CAFÉ DE ESPECIALIDAD', font('ibm-plex-mono', 500, mm(3.1)), track=mm(.7))
text(48, 61, 'HUILA', font('anton', 400, mm(21)), track=mm(1.2), key='origin')
text(48, 75, 'COLOMBIA · 1.750 m', font('ibm-plex-mono', 400, mm(3.3)), track=mm(.4))
text(48, 87, 'NOTAS DE CATA', font('ibm-plex-mono', 500, mm(2.3)), fill=(110, 104, 96), track=mm(.6))
text(48, 94, 'Cacao · Panela · Naranja', font('space-grotesk', 500, mm(4.6)), key='notes')
(rx0, ry), _ = L(8, 102); (rx1, _), _ = L(88, 102); d.line([(rx0, ry), (rx1, ry)], fill=INK, width=3)
text(10, 112, '250 g', font('anton', 400, mm(8.4)), anchor='lm', key='weight')
anchors['weight'] = (anchors['weight'][0] + 0.009, anchors['weight'][1])
text(52, 109.5, 'GRANO', font('ibm-plex-mono', 500, mm(2.6)), anchor='mm', track=0)
text(52, 114.5, 'ENTERO', font('ibm-plex-mono', 500, mm(2.6)), anchor='mm', track=0)
text(48, 124.5, 'TOSTADO 24·09·26 · LOTE 0926-H · CONSUMIR ANTES DE 03·27', font('ibm-plex-mono', 400, mm(1.7)), fill=(90, 86, 80), key='fine')
# sello circular "tueste medio"
(cx, cy), _ = L(79, 112)
r = mm(8)
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 64, 40), width=5)
d.text((cx, cy - mm(2)), 'TUESTE', font=font('ibm-plex-mono', 500, mm(1.9)), fill=(150, 64, 40), anchor='mm')
d.text((cx, cy + mm(2.2)), 'MEDIO', font=font('ibm-plex-mono', 500, mm(1.9)), fill=(150, 64, 40), anchor='mm')

# ---------- Kraft: abre-fácil y lateral ----------
x0, y0 = px(-W / 2 + 0.006, 0.212); x1, _ = px(W / 2 - 0.006, 0.212)
for xx in np.arange(x0, x1, mm(3)):
    d.line([(xx, y0), (xx + mm(1.6), y0)], fill=(70, 50, 34), width=4)
d.text(px(W / 2 - 0.008, 0.2165), 'ABRIR AQUÍ', font=font('ibm-plex-mono', 500, mm(2.2)), fill=(60, 44, 30), anchor='rm')
anchors['tear'] = (0.0, 0.212)
# cierre zip (relieve)
zx0, zy = px(-W / 2, 0.2045); zx1, _ = px(W / 2, 0.2045)
bd.line([(zx0, zy), (zx1, zy)], fill=250, width=int(mm(2.2)))
d.line([(zx0, zy), (zx1, zy)], fill=(136, 98, 64), width=int(mm(2.2)))

side = Image.new('RGBA', (int(mm(118)), int(mm(9))), (0, 0, 0, 0)); sd = ImageDraw.Draw(side)
f = font('ibm-plex-mono', 500, mm(2.7))
sd.text((0, mm(1.5)), 'PROCESO LAVADO · VARIEDAD CASTILLO', font=f, fill=(48, 36, 26, 230))
sd.text((0, mm(5.5)), 'ENVASE RECICLABLE · VÁLVULA DESGASIFICADORA', font=f, fill=(48, 36, 26, 230))
side = side.rotate(90, expand=True)
sx, sy = px(-W / 2 - 0.0215, 0.17)
img.paste(side, (int(sx - side.width / 2), int(sy)), side)
anchors['side'] = (-W / 2 - 0.0215, 0.11)

img.save(os.path.join(HERE, 'pouch_col.png')); bump.save(os.path.join(HERE, 'pouch_bump.png'))
json.dump({'anchors': anchors, 'label': [LW, LH, LZ0]}, open(os.path.join(HERE, 'pouch_tex.json'), 'w'))
print('tex', TW, TH, anchors)
