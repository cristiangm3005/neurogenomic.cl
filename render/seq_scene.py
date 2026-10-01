"""Secuencia de fotogramas para la animación scroll-driven (estilo «image sequence» en canvas).
Reutiliza la escena de pouch_scene.py: la cámara se acerca y orbita mientras la luz principal se enciende.
Uso: python seq_scene.py <frames> <ancho> <alto> <samples> <dir_salida>
Salida: f_000.png … + seq.json (posiciones proyectadas de cada zona, por fotograma)."""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
N, RW, RH, SAMPLES, OUTD = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
os.makedirs(OUTD, exist_ok=True)

# Construye la escena con pouch_scene.py (sin su bloque final de anclas/render)
src = open(os.path.join(HERE, 'pouch_scene.py'), encoding='utf-8').read()
src = src.split('# ---------------- Anclas proyectadas')[0]
sys.argv = [sys.argv[0], str(RW), str(RH), str(SAMPLES), os.path.join(OUTD, 'unused.png')]
g = {'__file__': os.path.join(HERE, 'pouch_scene.py'), '__name__': 'seq'}
exec(compile(src, 'pouch_scene.py', 'exec'), g)

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
sc, cam, surf, P = g['sc'], g['cam'], g['surf'], g['P']
info = json.load(open(os.path.join(HERE, 'pouch_tex.json')))
key = bpy.data.objects['key'].data; fill = bpy.data.objects['fill'].data
top = bpy.data.objects['top'].data; halo = bpy.data.objects['halo'].data
sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.02
sc.cycles.seed = 7

def ease(t): return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t

LW, LH, LZ0 = info['label']
def poly(X0, X1, Z0, Z1, n=3):
    pts = []
    for i in range(n + 1): pts.append((X0 + (X1 - X0) * i / n, Z0))
    for i in range(n + 1): pts.append((X1, Z0 + (Z1 - Z0) * i / n))
    for i in range(n + 1): pts.append((X1 - (X1 - X0) * i / n, Z1))
    for i in range(n + 1): pts.append((X0, Z1 - (Z1 - Z0) * i / n))
    return pts
BLIND = {
    'side': poly(-P.W / 2 - 0.035, -P.W / 2 - 0.007, 0.04, 0.175),
    'fine': poly(-LW / 2 + 0.004, LW / 2 - 0.004, LZ0 + 0.0015, LZ0 + 0.0095),
    'tear': poly(-P.W / 2 + 0.005, P.W / 2 - 0.005, 0.2085, 0.219),
}
vp = bpy.data.objects['Cylinder'].location.copy()  # válvula (primer cilindro creado)

out = {'frames': N, 'size': [RW, RH], 'anchors': {}, 'blind': {k: [] for k in BLIND}}
def proj(p):
    c = world_to_camera_view(sc, cam, p)
    return [round(c.x, 4), round(1 - c.y, 4)]

for f in range(N):
    t = f / (N - 1)
    e = ease(t)
    # Cámara: órbita de izquierda a frente + dolly in
    ang = math.radians(lerp(-40, 4, e)); r = lerp(1.32, 1.02, e); h = lerp(0.36, 0.2, e)
    cam.location = (math.sin(ang) * r, -math.cos(ang) * r, h)
    look = Vector((lerp(-0.02, 0.0, e), 0.0, lerp(0.15, 0.118, e)))
    cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Y').to_euler()
    # Luz: la escena «se enciende» en el primer tercio
    k = ease(min(1.0, t / 0.4))
    key.energy = lerp(2.5, 32, k); fill.energy = lerp(0.3, 2.2, k); top.energy = lerp(0.0, 5, k); halo.energy = lerp(1.0, 5, k)
    bpy.context.view_layer.update()
    for name, (X, Z) in info['anchors'].items():
        out['anchors'].setdefault(name, []).append(proj(surf(X, Z, 0.0005)[0]))
    out['anchors'].setdefault('valve', []).append(proj(vp))
    out['anchors'].setdefault('beans', []).append(proj(Vector((-0.115, -0.075, 0.004))))
    for b, pts in BLIND.items():
        out['blind'][b].append([proj(surf(X, Z, 0.0005)[0]) for X, Z in pts])
    sc.render.filepath = os.path.join(OUTD, f'f_{f:03d}.png')
    if os.path.exists(sc.render.filepath) and os.path.getsize(sc.render.filepath) > 0:
        continue  # ya renderizado (permite reanudar)
    bpy.ops.render.render(write_still=True)
    print('FRAME', f, flush=True)

json.dump(out, open(os.path.join(OUTD, 'seq.json'), 'w'), separators=(',', ':'))
print('DONE')
