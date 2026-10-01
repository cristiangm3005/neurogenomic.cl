"""Teléfono con un checkout ficticio, sobre pizarra, luz de estudio + contraluz lima (imagen del CTA final).
Uso: python phone_scene.py <ancho> <alto> <samples> <salida.png>  → además <salida>.json con la posición del botón «Pagar»."""
import bpy, json, math, os, sys
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RW, RH, SAMPLES, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
FS = os.environ.get('FONTS_DIR', os.path.join(HERE, 'node_modules', '@fontsource'))
def font(pkg, w, px): return ImageFont.truetype(f'{FS}/{pkg}/files/{pkg}-latin-{w}-normal.woff', int(px))

# ---------- Pantalla: checkout ficticio ----------
SW, SH = 1170, 2532
im = Image.new('RGB', (SW, SH), (246, 245, 241)); d = ImageDraw.Draw(im)
d.text((80, 150), '9:41', font=font('space-grotesk', 500, 46), fill=(20, 22, 26))
d.rectangle([0, 230, SW, 380], fill=(236, 234, 228))
d.text((80, 305), 'MESTA', font=font('space-grotesk', 700, 58), fill=(20, 22, 26), anchor='lm')
d.text((SW - 80, 305), 'Paso 3 de 3', font=font('ibm-plex-mono', 500, 34), fill=(110, 112, 118), anchor='rm')
d.text((80, 470), 'Confirma tu pedido', font=font('space-grotesk', 700, 76), fill=(20, 22, 26))
for i, (name, qty, price) in enumerate([('Huila · 250 g', '× 2', '$25.980'), ('Molinillo manual', '× 1', '$34.990')]):
    y = 640 + i * 230
    d.rounded_rectangle([80, y, 270, y + 190], 22, fill=(214, 205, 190) if i == 0 else (58, 60, 64))
    d.text((310, y + 50), name, font=font('space-grotesk', 500, 50), fill=(20, 22, 26))
    d.text((310, y + 120), qty, font=font('ibm-plex-mono', 500, 38), fill=(110, 112, 118))
    d.text((SW - 80, y + 80), price, font=font('space-grotesk', 500, 50), fill=(20, 22, 26), anchor='rm')
d.line([(80, 1150), (SW - 80, 1150)], fill=(214, 212, 205), width=4)
for i, (k, v) in enumerate([('Subtotal', '$60.970'), ('Envío', 'Gratis'), ('Total', '$60.970')]):
    y = 1210 + i * 95; b = i == 2
    d.text((80, y), k, font=font('space-grotesk', 700 if b else 400, 58 if b else 46), fill=(20, 22, 26))
    d.text((SW - 80, y), v, font=font('space-grotesk', 700 if b else 400, 58 if b else 46), fill=(20, 22, 26), anchor='ra')
d.rounded_rectangle([80, 1560, SW - 80, 1740], 26, outline=(200, 198, 190), width=4)
d.text((130, 1650), '•••• 4821', font=font('ibm-plex-mono', 500, 46), fill=(60, 62, 66), anchor='lm')
d.text((SW - 130, 1650), 'Cambiar', font=font('space-grotesk', 500, 42), fill=(90, 92, 98), anchor='rm')
BTN = (80, 2050, SW - 80, 2250)
d.rounded_rectangle(BTN, 36, fill=(20, 22, 26))
d.text(((BTN[0] + BTN[2]) / 2, (BTN[1] + BTN[3]) / 2), 'Pagar $60.970', font=font('space-grotesk', 700, 64), fill=(200, 255, 0), anchor='mm')
d.text((SW / 2, 2340), 'Pago seguro · Devolución en 30 días', font=font('ibm-plex-mono', 500, 32), fill=(130, 132, 138), anchor='mm')
scr_path = os.path.join(HERE, '_phone_screen.png'); im.save(scr_path)

# ---------- Escena ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
PW, PH, PD = 0.0716, 0.1476, 0.0078
def mat(name, col, rough, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*col, 1); b.inputs['Roughness'].default_value = rough
    for k, v in kw.items(): b.inputs[k].default_value = v
    return m
bpy.ops.mesh.primitive_cube_add(size=1); body = bpy.context.active_object
body.scale = (PW, PD, PH); bpy.ops.object.transform_apply(scale=True)
bv = body.modifiers.new('b', 'BEVEL'); bv.width = 0.009; bv.segments = 10; bv.limit_method = 'NONE'
for p in body.data.polygons: p.use_smooth = True
body.data.materials.append(mat('frame', (0.06, 0.062, 0.068), 0.28, Metallic=0.9))
# vidrio frontal negro + pantalla
bpy.ops.mesh.primitive_plane_add(size=1); glass = bpy.context.active_object
glass.scale = (PW - 0.0035, PH - 0.0035, 1); bpy.ops.object.transform_apply(scale=True)
glass.rotation_euler = (math.pi / 2, 0, 0); glass.location = (0, -PD / 2 - 0.0002, 0)
glass.data.materials.append(mat('glass', (0.004, 0.004, 0.005), 0.05, **{'Coat Weight': 1.0}))
scr = bpy.data.materials.new('screen'); scr.use_nodes = True; nt = scr.node_tree
em = nt.nodes.new('ShaderNodeEmission'); tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = bpy.data.images.load(scr_path)
em.inputs['Strength'].default_value = 0.34; nt.links.new(tx.outputs['Color'], em.inputs['Color'])
gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.04
mix = nt.nodes.new('ShaderNodeMixShader'); mix.inputs['Fac'].default_value = 0.015
nt.links.new(em.outputs['Emission'], mix.inputs[1]); nt.links.new(gl.outputs['BSDF'], mix.inputs[2])
nt.links.new(mix.outputs['Shader'], nt.nodes['Material Output'].inputs['Surface']); nt.nodes.remove(nt.nodes['Principled BSDF'])
SWm, SHm = PW - 0.0075, PH - 0.0075
bpy.ops.mesh.primitive_plane_add(size=1); screen = bpy.context.active_object
screen.scale = (SWm, SHm, 1); bpy.ops.object.transform_apply(scale=True)
screen.rotation_euler = (math.pi / 2, 0, 0); screen.location = (0, -PD / 2 - 0.0004, 0)
screen.data.materials.append(scr)
# isla de cámara (detalle en el reverso que se ve por el borde)
phone = [body, glass, screen]
# pose: apoyado en un soporte, inclinado hacia atrás y girado
pivot = bpy.data.objects.new('pivot', None); sc.collection.objects.link(pivot)
for o in phone: o.parent = pivot
pivot.rotation_euler = (math.radians(-14), 0, math.radians(-22))
pivot.location = (0, 0, PH / 2 * math.cos(math.radians(14)) + PD / 2 * math.sin(math.radians(14)) + 0.0015)
# soporte
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.022, 0.004)); st = bpy.context.active_object
st.scale = (0.05, 0.05, 0.008); bpy.ops.object.transform_apply(scale=True); st.rotation_euler.z = math.radians(-22)
st.modifiers.new('b', 'BEVEL').width = 0.002
st.data.materials.append(mat('stand', (0.035, 0.036, 0.04), 0.35, Metallic=1.0))
# suelo pizarra
bpy.ops.mesh.primitive_plane_add(size=4); fl = bpy.context.active_object
mf = bpy.data.materials.new('slate'); mf.use_nodes = True; nt = mf.node_tree; b = nt.nodes['Principled BSDF']
n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 60; n1.inputs['Detail'].default_value = 10
c1 = nt.nodes.new('ShaderNodeValToRGB'); c1.color_ramp.elements[0].color = (0.006, 0.006, 0.007, 1); c1.color_ramp.elements[1].color = (0.022, 0.022, 0.024, 1)
nt.links.new(n1.outputs['Fac'], c1.inputs['Fac']); nt.links.new(c1.outputs['Color'], b.inputs['Base Color'])
b.inputs['Roughness'].default_value = 0.55; b.inputs['Specular IOR Level'].default_value = 0.25
fl.data.materials.append(mf)
def area(loc, target, size, power, color, size_y=None, spread=180):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = power; l.color = color; l.size = size; l.spread = math.radians(spread)
    if size_y: l.shape = 'RECTANGLE'; l.size_y = size_y
    o = bpy.data.objects.new('a', l); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
area((-0.55, -0.15, 0.42), (0, 0, 0.08), 0.45, 9, (1.0, 0.93, 0.84))
area((0.12, 0.3, 0.13), (0.0, 0.0, 0.12), 0.03, 1.3, (0.72, 1.0, 0.0), size_y=0.25, spread=12)
area((0.5, -0.6, 0.12), (0, 0, 0.06), 0.8, 0.8, (0.9, 0.95, 1.0))
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)
cd = bpy.data.cameras.new('c'); cd.lens = 70
cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0.02, -0.62, 0.2)
cam.rotation_euler = (Vector((0.005, 0, 0.078)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
bpy.context.view_layer.update()
cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.4
fo = bpy.data.objects.new('f', None); sc.collection.objects.link(fo)
fo.location = screen.matrix_world @ Vector((0, 0, 0)); cd.dof.focus_object = fo
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.render.resolution_x = RW; sc.render.resolution_y = RH
sc.view_settings.view_transform = 'AgX'
try: sc.view_settings.look = 'AgX - Medium High Contrast'
except Exception: pass
# Proyección del botón «Pagar» y de las esquinas de la pantalla
def scr_pt(u, v):  # u,v en 0-1 de la textura de pantalla (v hacia abajo)
    p = screen.matrix_world @ Vector(((u - .5) * SWm, (.5 - v) * SHm, 0))
    c = world_to_camera_view(sc, cam, p); return [round(c.x, 4), round(1 - c.y, 4)]
data = {'btn': scr_pt(.5, (BTN[1] + BTN[3]) / 2 / SH), 'btn_l': scr_pt(BTN[0] / SW, (BTN[1] + BTN[3]) / 2 / SH),
        'btn_r': scr_pt(BTN[2] / SW, (BTN[1] + BTN[3]) / 2 / SH), 'title': scr_pt(.35, 510 / SH), 'total': scr_pt(.5, 1400 / SH),
        'screen': [scr_pt(0, 0), scr_pt(1, 0), scr_pt(1, 1), scr_pt(0, 1)]}
json.dump(data, open(os.path.splitext(OUT)[0] + '.json', 'w'))
print('PHONE', json.dumps(data))
sc.render.filepath = OUT; sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
print('DONE')
