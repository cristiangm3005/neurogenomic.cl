"""Barra de eye tracking bajo un monitor de laboratorio (21:9).
Uso: python tracker_scene.py <ancho> <alto> <samples> <salida.png>"""
import bpy, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
RW, RH, SAMPLES, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------- Imagen de pantalla: lectura biométrica en vivo ----------
SW, SH = 2400, 1460
img = Image.new('RGB', (SW, SH), (2, 2, 3)); d = ImageDraw.Draw(img)
for x in range(0, SW, 80): d.line([(x, 0), (x, SH)], fill=(10, 11, 12))
for y in range(0, SH, 80): d.line([(0, y), (SW, y)], fill=(10, 11, 12))
glow = Image.new('L', (SW, SH), 0); g = ImageDraw.Draw(glow)
for cx, cy, r, a in [(1150, 620, 260, 255), (1500, 520, 160, 170), (820, 900, 130, 120)]:
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
glow = glow.filter(ImageFilter.GaussianBlur(90))
lime = Image.new('RGB', (SW, SH), (200, 255, 0))
img = Image.composite(lime, img, glow.point(lambda v: int(v * .05)))
d = ImageDraw.Draw(img)
pts = [(1150, 620), (1500, 520), (820, 900), (1280, 980), (1150, 600)]
d.line(pts, fill=(200, 255, 0), width=6)
for (x, y) in pts: d.ellipse([x - 26, y - 26, x + 26, y + 26], outline=(220, 255, 60), width=6)
ys = [1250 + 40 * math.sin(i / 14) + (90 if 120 < i < 140 else 0) for i in range(0, 300)]
d.line([(200 + i * 7, ys[i]) for i in range(300)], fill=(200, 245, 66), width=5)
for i, w in enumerate([340, 220, 520, 160]): d.rectangle([140, 140 + i * 60, 140 + w, 160 + i * 60], fill=(40, 44, 48))
img.save(os.path.join(HERE, '_screen.png'))

def principled(name, col, rough, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m

def box(name, size, loc, mat, bevel=0.002, seg=4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.active_object; o.name = name
    o.scale = size; bpy.ops.object.transform_apply(scale=True)
    if bevel:
        bv = o.modifiers.new('b', 'BEVEL'); bv.width = bevel; bv.segments = seg
    o.data.materials.append(mat)
    for p in o.data.polygons: p.use_smooth = True
    return o

plastic = principled('plastic', (0.012, 0.012, 0.013), 0.42, **{'Coat Weight': 0.15})
glass = principled('glass', (0.004, 0.004, 0.005), 0.06, **{'Specular IOR Level': 0.8})
alu = principled('alu', (0.05, 0.05, 0.055), 0.32, **{'Metallic': 1.0})

# Monitor (borde inferior visible) + pantalla emisiva
box('bezel', (0.70, 0.022, 0.42), (0, 0.0, 0.33), plastic, 0.004)
scr = bpy.data.materials.new('screen'); scr.use_nodes = True; nt = scr.node_tree
em = nt.nodes.new('ShaderNodeEmission'); tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(os.path.join(HERE, '_screen.png'))
em.inputs['Strength'].default_value = 1.1; nt.links.new(tx.outputs['Color'], em.inputs['Color'])
mix = nt.nodes.new('ShaderNodeMixShader'); gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.05
mix.inputs['Fac'].default_value = 0.05
nt.links.new(em.outputs['Emission'], mix.inputs[1]); nt.links.new(gl.outputs['BSDF'], mix.inputs[2])
nt.links.new(mix.outputs['Shader'], nt.nodes['Material Output'].inputs['Surface'])
nt.nodes.remove(nt.nodes['Principled BSDF'])
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -0.0115, 0.335), rotation=(math.pi / 2, 0, 0)); sp = bpy.context.active_object
sp.scale = (0.67, 0.39, 1); sp.data.materials.append(scr)

# Barra de eye tracking
bar = box('bar', (0.34, 0.026, 0.021), (0, -0.016, 0.106), plastic, 0.006, 6)
front = box('front', (0.322, 0.002, 0.013), (0, -0.0295, 0.106), glass, 0.0015, 3)
ir = principled('ir', (0.02, 0.0, 0.0), 0.3, **{'Emission Color': (1, 0.05, 0.02, 1), 'Emission Strength': 2.5})
for sx in (-0.12, 0.12):
    for k in range(4):
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.0019, depth=0.001, location=(sx + (k - 1.5) * 0.0062, -0.0306, 0.106), rotation=(math.pi / 2, 0, 0))
        bpy.context.active_object.data.materials.append(ir)
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.0052, depth=0.0016, location=(0, -0.0308, 0.106), rotation=(math.pi / 2, 0, 0))
bpy.context.active_object.data.materials.append(alu)
bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=0.0034, depth=0.001, location=(0, -0.0318, 0.106), rotation=(math.pi / 2, 0, 0))
bpy.context.active_object.data.materials.append(principled('lens', (0.0, 0.0, 0.0), 0.02, **{'Coat Weight': 1.0}))
status = principled('led', (0, 0, 0), 0.3, **{'Emission Color': (0.78, 1.0, 0.0, 1), 'Emission Strength': 6})
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.0009, depth=0.0008, location=(0.15, -0.0307, 0.1105), rotation=(math.pi / 2, 0, 0))
bpy.context.active_object.data.materials.append(status)

# Escritorio + fondo
bpy.ops.mesh.primitive_plane_add(size=4); desk = bpy.context.active_object
md = bpy.data.materials.new('desk'); md.use_nodes = True; nt = md.node_tree; b = nt.nodes['Principled BSDF']
n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 60; n1.inputs['Detail'].default_value = 10
c1 = nt.nodes.new('ShaderNodeValToRGB'); c1.color_ramp.elements[0].color = (0.006, 0.006, 0.007, 1); c1.color_ramp.elements[1].color = (0.02, 0.02, 0.022, 1)
nt.links.new(n1.outputs['Fac'], c1.inputs['Fac']); nt.links.new(c1.outputs['Color'], b.inputs['Base Color'])
b.inputs['Roughness'].default_value = 0.4; desk.data.materials.append(md)
box('stand', (0.08, 0.16, 0.012), (0, 0.05, 0.006), alu, 0.003)
box('neck', (0.05, 0.02, 0.13), (0, 0.04, 0.07), alu, 0.004)

def area(loc, target, size, power, color, size_y=None, spread=180):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = power; l.color = color; l.size = size; l.spread = math.radians(spread)
    if size_y: l.shape = 'RECTANGLE'; l.size_y = size_y
    o = bpy.data.objects.new('a', l); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
area((-0.6, -0.5, 0.45), (0, 0, 0.1), 0.5, 16, (1.0, 0.94, 0.86))
area((0.0, -0.25, 0.32), (0.0, -0.03, 0.11), 0.03, 0.9, (0.72, 1.0, 0.0), size_y=0.5, spread=12)
area((0.2, -0.7, 0.05), (0, 0, 0.1), 0.8, 1.2, (0.9, 0.95, 1.0))
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)

cd = bpy.data.cameras.new('c'); cd.lens = 55
cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (-0.34, -0.6, 0.15)
cam.rotation_euler = (Vector((0.03, -0.02, 0.128)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
fo = bpy.data.objects.new('f', None); sc.collection.objects.link(fo); fo.location = (-0.04, -0.03, 0.106)
cd.dof.use_dof = True; cd.dof.focus_object = fo; cd.dof.aperture_fstop = 2.0
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.render.resolution_x = RW; sc.render.resolution_y = RH
sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = 0.0
try: sc.view_settings.look = 'AgX - Punchy'
except Exception: pass
sc.render.filepath = OUT; sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print('DONE', OUT)
