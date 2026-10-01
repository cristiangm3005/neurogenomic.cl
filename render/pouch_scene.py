"""Escena fotográfica: bolsa de café de especialidad (kraft) sobre pizarra, luz de estudio + contraluz lima.
Uso: python pouch_scene.py <ancho> <alto> <samples> <salida.png>
Además escribe <salida>.json con las posiciones proyectadas (0–1) de cada zona de la etiqueta."""
import bpy, bmesh, json, math, os, random, sys
from mathutils import Vector, Matrix, Euler
from bpy_extras.object_utils import world_to_camera_view

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pouch as P

RW, RH, SAMPLES, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
ROT_Z = math.radians(34)
random.seed(11)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------------- Bolsa ----------------
zs = []
for j in range(P.NZ + 1):
    k = j / P.NZ
    zs.append(P.H * (0.5 - 0.5 * math.cos(math.pi * k)) * 0.35 + P.H * k * 0.65)  # más densidad en extremos
verts, uvs_grid = [], []
TX0, TX1 = P.TEX_X
for z in zs:
    pts = P.ring(z)
    s = P.arc_from_front(pts)
    row = []
    for (x, y), X in zip(pts, s):
        verts.append((x, y, z))
        row.append(((X - TX0) / (TX1 - TX0), z / P.H))
    uvs_grid.append(row)
n = P.NT + 1
faces, face_uv = [], []
for j in range(P.NZ):
    for i in range(P.NT):
        a, b, c, d = j * n + i, j * n + i + 1, (j + 1) * n + i + 1, (j + 1) * n + i
        faces.append((a, b, c, d))
        face_uv.append((uvs_grid[j][i], uvs_grid[j][i + 1], uvs_grid[j + 1][i + 1], uvs_grid[j + 1][i]))
# tapa inferior y superior (abanico)
for (zi, z, flip) in ((0, zs[0], True), (P.NZ, zs[-1], False)):
    ci = len(verts); verts.append((0, 0, z))
    for i in range(P.NT):
        f = (zi * n + i, zi * n + i + 1, ci)
        faces.append(tuple(reversed(f)) if flip else f)
        face_uv.append(((.5, .02), (.5, .02), (.5, .02)))
me = bpy.data.meshes.new('pouch'); me.from_pydata(verts, [], faces); me.update()
uvl = me.uv_layers.new(name='UV')
li = 0
for poly, fu in zip(me.polygons, face_uv):
    for k, loop in enumerate(poly.loop_indices):
        uvl.data[loop].uv = fu[k]
for p_ in me.polygons: p_.use_smooth = True
bag = bpy.data.objects.new('Bag', me); sc.collection.objects.link(bag)
bag.rotation_euler = (0, 0, ROT_Z)
# arrugas sutiles
tex = bpy.data.textures.new('wr', 'CLOUDS'); tex.noise_scale = 0.018; tex.noise_depth = 3
disp = bag.modifiers.new('wr', 'DISPLACE'); disp.texture = tex; disp.strength = 0.0011; disp.mid_level = 0.5; disp.texture_coords = 'OBJECT'
tex2 = bpy.data.textures.new('wr2', 'CLOUDS'); tex2.noise_scale = 0.004; tex2.noise_depth = 2
disp2 = bag.modifiers.new('wr2', 'DISPLACE'); disp2.texture = tex2; disp2.strength = 0.00025; disp2.mid_level = 0.5; disp2.texture_coords = 'OBJECT'

def mat_pouch():
    m = bpy.data.materials.new('kraft'); m.use_nodes = True
    nt = m.node_tree; N = nt.nodes; Lk = nt.links
    bsdf = N['Principled BSDF']
    col = N.new('ShaderNodeTexImage'); col.image = bpy.data.images.load(os.path.join(HERE, 'pouch_col.png'))
    bmp = N.new('ShaderNodeTexImage'); bmp.image = bpy.data.images.load(os.path.join(HERE, 'pouch_bump.png')); bmp.image.colorspace_settings.name = 'Non-Color'
    bn = N.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = 0.35; bn.inputs['Distance'].default_value = 0.0006
    Lk.new(col.outputs['Color'], bsdf.inputs['Base Color'])
    Lk.new(bmp.outputs['Color'], bn.inputs['Height']); Lk.new(bn.outputs['Normal'], bsdf.inputs['Normal'])
    # rugosidad: kraft mate, etiqueta algo más satinada
    rr = N.new('ShaderNodeMapRange'); Lk.new(bmp.outputs['Color'], rr.inputs['Value'])
    rr.inputs['From Min'].default_value = 0.3; rr.inputs['From Max'].default_value = 0.8
    rr.inputs['To Min'].default_value = 0.78; rr.inputs['To Max'].default_value = 0.6
    Lk.new(rr.outputs['Result'], bsdf.inputs['Roughness'])
    bsdf.inputs['Specular IOR Level'].default_value = 0.35
    return m
bag.data.materials.append(mat_pouch())

def surf(X, Z, off=0.0):
    """Punto en mundo sobre la bolsa + normal aproximada."""
    p0 = Vector(P.point_at(X, Z)); p1 = Vector(P.point_at(X + 0.001, Z)); p2 = Vector(P.point_at(X, Z + 0.001))
    nrm = (p1 - p0).cross(p2 - p0).normalized()
    if nrm.y > 0 and abs(X) < P.W / 2: nrm = -nrm
    R = Matrix.Rotation(ROT_Z, 4, 'Z')
    return R @ (p0 + nrm * off), (R.to_3x3() @ nrm).normalized()

# ---------------- Válvula desgasificadora ----------------
vp, vn = surf(0.0, 0.189, 0.0009)
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.0085, depth=0.0018, location=vp)
valve = bpy.context.active_object
valve.rotation_euler = vn.to_track_quat('Z', 'Y').to_euler()
bev = valve.modifiers.new('b', 'BEVEL'); bev.width = 0.0006; bev.segments = 3
mv = bpy.data.materials.new('valve'); mv.use_nodes = True
b = mv.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0.11, 0.075, 0.045, 1); b.inputs['Roughness'].default_value = 0.45
valve.data.materials.append(mv)
for k in range(5):
    a = k / 5 * math.tau
    hp = vp + vn * 0.001 + (Matrix.Rotation(a, 3, vn) @ vn.orthogonal().normalized()) * 0.0038
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.0007, depth=0.0006, location=hp)
    h = bpy.context.active_object; h.rotation_euler = valve.rotation_euler
    mh = bpy.data.materials.get('hole') or bpy.data.materials.new('hole'); mh.diffuse_color = (0, 0, 0, 1)
    if not mh.use_nodes:
        mh.use_nodes = True; mh.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.01, 0.008, 0.006, 1)
    h.data.materials.append(mh)

# ---------------- Granos de café ----------------
bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=20, radius=1)
for v in bm.verts:
    x, y, z = v.co
    if z > 0:  # cara plana con surco central
        z = z * 0.42 - 0.38 * math.exp(-(y / 0.13) ** 2) * (1 - x * x) ** .5
    v.co = Vector((x * 0.0062, y * 0.0047, z * 0.0034))
bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
bean_me = bpy.data.meshes.new('bean'); bm.to_mesh(bean_me); bm.free()
for p_ in bean_me.polygons: p_.use_smooth = True
mb = bpy.data.materials.new('bean'); mb.use_nodes = True
nt = mb.node_tree; bsdf = nt.nodes['Principled BSDF']
nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 900; nz.inputs['Detail'].default_value = 6
cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (0.05, 0.022, 0.01, 1); cr.color_ramp.elements[1].color = (0.13, 0.065, 0.03, 1)
nt.links.new(nz.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], bsdf.inputs['Base Color'])
bsdf.inputs['Roughness'].default_value = 0.34; bsdf.inputs['Coat Weight'].default_value = 0.25; bsdf.inputs['Coat Roughness'].default_value = 0.2
bean_me.materials.append(mb)
beans = []
def place(cx, cy, sx, sy, count, stack=False):
    for _ in range(count * 8):
        if count <= 0: break
        x, y = random.gauss(cx, sx), random.gauss(cy, sy)
        if any(math.hypot(x - bx, y - by) < 0.0115 for bx, by, _ in beans): continue
        # no dentro de la bolsa
        lx, ly = Matrix.Rotation(-ROT_Z, 2) @ Vector((x, y))
        if abs(lx) < P.W / 2 + 0.01 and abs(ly) < P.D0 / 2 + 0.012: continue
        beans.append((x, y, 0)); count -= 1
place(-0.115, -0.075, 0.03, 0.022, 26)
place(0.105, -0.095, 0.018, 0.014, 9)
place(-0.02, -0.16, 0.05, 0.02, 7)
place(0.02, -0.29, 0.06, 0.02, 5)      # primer plano, desenfocados
for x, y, _ in beans:
    o = bpy.data.objects.new('bean', bean_me); sc.collection.objects.link(o)
    flip = random.random() < 0.45
    o.location = (x, y, 0.0024 if flip else 0.0021)
    o.rotation_euler = (math.pi + random.uniform(-.15, .15) if flip else random.uniform(-.12, .12), random.uniform(-.12, .12), random.uniform(0, math.tau))
    s_ = random.uniform(.9, 1.12); o.scale = (s_, s_, s_)
# pequeño montículo: segunda capa
for x, y, _ in [b_ for b_ in beans if math.hypot(b_[0] + .115, b_[1] + .075) < .022][:7]:
    o = bpy.data.objects.new('bean', bean_me); sc.collection.objects.link(o)
    o.location = (x + random.uniform(-.004, .004), y + random.uniform(-.004, .004), 0.0062)
    o.rotation_euler = (random.uniform(-.5, .5), random.uniform(-.5, .5), random.uniform(0, math.tau))

# ---------------- Set: pizarra + fondo ----------------
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0)); floor = bpy.context.active_object
mf = bpy.data.materials.new('slate'); mf.use_nodes = True; nt = mf.node_tree; bsdf = nt.nodes['Principled BSDF']
n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 60; n1.inputs['Detail'].default_value = 10; n1.inputs['Roughness'].default_value = .62
c1 = nt.nodes.new('ShaderNodeValToRGB'); c1.color_ramp.elements[0].color = (0.006, 0.006, 0.007, 1); c1.color_ramp.elements[1].color = (0.022, 0.022, 0.024, 1)
nt.links.new(n1.outputs['Fac'], c1.inputs['Fac']); nt.links.new(c1.outputs['Color'], bsdf.inputs['Base Color'])
r1 = nt.nodes.new('ShaderNodeMapRange'); r1.inputs['To Min'].default_value = 0.5; r1.inputs['To Max'].default_value = 0.85
nt.links.new(n1.outputs['Fac'], r1.inputs['Value']); nt.links.new(r1.outputs['Result'], bsdf.inputs['Roughness'])
n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 900; n2.inputs['Detail'].default_value = 4
bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .18; bp.inputs['Distance'].default_value = 0.0004
nt.links.new(n2.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], bsdf.inputs['Normal'])
bsdf.inputs['Specular IOR Level'].default_value = 0.22
floor.data.materials.append(mf)
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 1.1, 1.0), rotation=(math.pi / 2, 0, 0)); wall = bpy.context.active_object
mw = bpy.data.materials.new('wall'); mw.use_nodes = True; mw.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.012, 0.012, 0.013, 1)
mw.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.9
wall.data.materials.append(mw)

# ---------------- Luces ----------------
def area(name, loc, target, size, power, color, shape='RECTANGLE', size_y=None, spread=180):
    l = bpy.data.lights.new(name, 'AREA'); l.energy = power; l.color = color; l.shape = shape; l.size = size; l.spread = math.radians(spread)
    if size_y: l.size_y = size_y
    o = bpy.data.objects.new(name, l); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return o
area('key', (-0.55, -0.45, 0.55), (0, 0, 0.12), 0.45, 32, (1.0, 0.93, 0.84))
area('rim', (0.28, 0.24, 0.14), (0.0, -0.02, 0.2), 0.06, 7, (0.70, 1.0, 0.0), size_y=0.45, spread=28)
area('rim2', (-0.28, 0.24, 0.15), (0.0, -0.02, 0.21), 0.05, 3.5, (0.75, 1.0, 0.1), size_y=0.4, spread=28)
area('fill', (0.65, -0.7, 0.22), (0, 0, 0.1), 0.9, 2.2, (0.9, 0.95, 1.0))
area('top', (0.0, -0.05, 0.6), (0, 0, 0.2), 0.25, 5, (1, 1, 1))
sp = bpy.data.lights.new('halo', 'SPOT'); sp.energy = 5; sp.spot_size = math.radians(70); sp.spot_blend = 1.0; sp.color = (0.95, 0.92, 0.85)
spo = bpy.data.objects.new('halo', sp); sc.collection.objects.link(spo); spo.location = (0.02, 0.2, 0.04)
spo.rotation_euler = (Vector((0.02, 1.1, 0.3)) - spo.location).to_track_quat('-Z', 'Y').to_euler()
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)

# ---------------- Cámara ----------------
cam_d = bpy.data.cameras.new('cam'); cam_d.lens = 68; cam_d.sensor_width = 36
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0.0, -0.98, 0.2)
look = Vector((0.0, 0.0, 0.118))
cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Y').to_euler()
focus, _ = surf(0.0, 0.112, 0.0)
fo = bpy.data.objects.new('focus', None); sc.collection.objects.link(fo); fo.location = focus
cam_d.dof.use_dof = True; cam_d.dof.focus_object = fo; cam_d.dof.aperture_fstop = 2.8

# ---------------- Render ----------------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES
sc.cycles.use_adaptive_sampling = True; sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.render.resolution_x = RW; sc.render.resolution_y = RH; sc.render.resolution_percentage = 100
sc.render.filepath = OUT; sc.render.image_settings.file_format = 'PNG'
sc.view_settings.view_transform = 'AgX'
sc.view_settings.exposure = -0.2
for look_ in ('AgX - Punchy', 'Punchy', 'AgX - Medium High Contrast'):
    try: sc.view_settings.look = look_; break
    except Exception: pass
sc.cycles.max_bounces = 6; sc.cycles.glossy_bounces = 3; sc.cycles.transmission_bounces = 2
sc.render.threads_mode = 'AUTO'

# ---------------- Anclas proyectadas ----------------
bpy.context.view_layer.update()
info = json.load(open(os.path.join(HERE, 'pouch_tex.json')))
def proj(p):
    c = world_to_camera_view(sc, cam, p)
    return [round(c.x, 4), round(1 - c.y, 4)]
A = {k: proj(surf(X, Z, 0.0005)[0]) for k, (X, Z) in info['anchors'].items()}
A['valve'] = proj(vp)
A['beans'] = proj(Vector((-0.115, -0.075, 0.004)))
A['beans2'] = proj(Vector((0.105, -0.095, 0.004)))
def poly(X0, X1, Z0, Z1, nx=6, nz=6):
    pts = []
    for i in range(nx + 1): pts.append(proj(surf(X0 + (X1 - X0) * i / nx, Z0, .0005)[0]))
    for i in range(nz + 1): pts.append(proj(surf(X1, Z0 + (Z1 - Z0) * i / nz, .0005)[0]))
    for i in range(nx + 1): pts.append(proj(surf(X1 - (X1 - X0) * i / nx, Z1, .0005)[0]))
    for i in range(nz + 1): pts.append(proj(surf(X0, Z1 - (Z1 - Z0) * i / nz, .0005)[0]))
    return pts
LW, LH, LZ0 = info['label']
blind = {
    'side': poly(-P.W / 2 - 0.035, -P.W / 2 - 0.007, 0.04, 0.175),
    'fine': poly(-LW / 2 + 0.004, LW / 2 - 0.004, LZ0 + 0.0015, LZ0 + 0.0095),
    'tear': poly(-P.W / 2 + 0.005, P.W / 2 - 0.005, 0.2085, 0.219),
}
label = poly(-LW / 2, LW / 2, LZ0, LZ0 + LH)
json.dump({'size': [RW, RH], 'anchors': A, 'blind': blind, 'label': label}, open(os.path.splitext(OUT)[0] + '.json', 'w'))
print('ANCHORS', json.dumps(A))
bpy.ops.render.render(write_still=True)
print('DONE', OUT)
