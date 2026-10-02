"""Botella de bebida genérica (sin marca ni textos) fotografiada en estudio oscuro.
Uso: python bottle_scene.py <ancho> <alto> <samples> <salida.png>  → salida.png + salida.json
El JSON trae las zonas de interés proyectadas (0–1 sobre la foto) y la silueta, para calibrar el mapa de calor."""
import bpy, json, math, os, sys
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

RW, RH, SAMPLES, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]

# Perfil exterior (radio, altura) en metros: base, cuerpo, hombro, cuello y boca
PROFILE = [(0.0, 0.0), (0.028, 0.0), (0.0335, 0.004), (0.0345, 0.012), (0.0345, 0.135), (0.034, 0.148),
           (0.031, 0.165), (0.025, 0.182), (0.0185, 0.196), (0.0135, 0.208), (0.0125, 0.218), (0.0125, 0.226)]
SEG = 128


def lathe(name, prof, closed_top=False):
    """Superficie de revolución a partir de un perfil (r, z)."""
    verts, faces = [], []
    for r, z in prof:
        for i in range(SEG):
            a = i / SEG * 2 * math.pi
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for j in range(len(prof) - 1):
        for i in range(SEG):
            a, b = j * SEG + i, j * SEG + (i + 1) % SEG
            faces.append((a, b, b + SEG, a + SEG))
    if closed_top:
        faces.append(tuple(range((len(prof) - 1) * SEG, len(prof) * SEG)))
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    return ob


def principled(name, **kw):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    for k, v in kw.items():
        b.inputs[k].default_value = v
    return m, m.node_tree, b


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# Vidrio (con grosor) y líquido ámbar oscuro
glass = lathe('glass', PROFILE)
sol = glass.modifiers.new('s', 'SOLIDIFY'); sol.thickness = 0.0022; sol.offset = -1
mg, _, _ = principled('glass', **{'Base Color': (0.86, 0.95, 0.9, 1), 'Roughness': 0.03, 'IOR': 1.5, 'Transmission Weight': 1.0})
glass.data.materials.append(mg)
liq_prof = [(0.0, 0.0035), (0.0315, 0.0035), (0.032, 0.012), (0.032, 0.135), (0.0315, 0.148), (0.0288, 0.165),
            (0.0232, 0.182), (0.0172, 0.193), (0.0, 0.193)]
liquid = lathe('liquid', liq_prof)
ml, nt, b = principled('liquid', **{'Base Color': (0.55, 0.16, 0.035, 1), 'Roughness': 0.02, 'IOR': 1.34, 'Transmission Weight': 1.0})
vol = nt.nodes.new('ShaderNodeVolumeAbsorption'); vol.inputs['Color'].default_value = (0.5, 0.1, 0.02, 1); vol.inputs['Density'].default_value = 26
nt.links.new(vol.outputs['Volume'], nt.nodes['Material Output'].inputs['Volume'])
liquid.data.materials.append(ml)

# Etiqueta lisa: banda negra mate con un filete lima (sin textos)
band = lathe('label', [(0.0352, 0.064), (0.0352, 0.122)])
mlab, nt, b = principled('label', **{'Roughness': 0.38})
tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
nt.links.new(tc.outputs['Object'], sep.inputs['Vector'])
ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.interpolation = 'CONSTANT'
els = ramp.color_ramp.elements
els[0].position = 0.0; els[0].color = (0.005, 0.005, 0.006, 1)
e1 = els.new(0.86); e1.color = (0.55, 0.85, 0.0, 1)
e2 = els.new(0.885); e2.color = (0.005, 0.005, 0.006, 1)
els[-1].position = 1.0; els[-1].color = (0.005, 0.005, 0.006, 1)
mp = nt.nodes.new('ShaderNodeMapRange'); mp.inputs['From Min'].default_value = 0.064; mp.inputs['From Max'].default_value = 0.122
nt.links.new(sep.outputs['Z'], mp.inputs['Value']); nt.links.new(mp.outputs['Result'], ramp.inputs['Fac'])
nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
band.data.materials.append(mlab)

# Tapa corona metálica (cilindro con estrías)
cap_prof = [(0.0, 0.2335), (0.0138, 0.2335), (0.0146, 0.2318), (0.0148, 0.222), (0.0152, 0.2195)]
cap = lathe('cap', cap_prof)
disp = cap.modifiers.new('w', 'SOLIDIFY'); disp.thickness = 0.0008
mc, nt, b = principled('cap', **{'Base Color': (0.62, 0.64, 0.66, 1), 'Metallic': 1.0, 'Roughness': 0.28})
wave = nt.nodes.new('ShaderNodeTexWave'); wave.wave_type = 'BANDS'; wave.bands_direction = 'X'
wave.inputs['Scale'].default_value = 3.2
bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .35
tc2 = nt.nodes.new('ShaderNodeTexCoord'); nt.links.new(tc2.outputs['Object'], wave.inputs['Vector'])
nt.links.new(wave.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
cap.data.materials.append(mc)

# Suelo pizarra oscuro y fondo negro (misma luz que las demás piezas del sitio)
bpy.ops.mesh.primitive_plane_add(size=4); fl = bpy.context.active_object
mf, nt, b = principled('slate', **{'Roughness': 0.8, 'Specular IOR Level': 0.04})
n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 60; n1.inputs['Detail'].default_value = 10
c1 = nt.nodes.new('ShaderNodeValToRGB'); c1.color_ramp.elements[0].color = (0.004, 0.004, 0.0045, 1); c1.color_ramp.elements[1].color = (0.014, 0.014, 0.016, 1)
nt.links.new(n1.outputs['Fac'], c1.inputs['Fac'])
# Suelo mate puro: sin reflejo especular (evita el brillo rasante de las luces traseras por efecto Fresnel)
dif = nt.nodes.new('ShaderNodeBsdfDiffuse'); nt.links.new(c1.outputs['Color'], dif.inputs['Color'])
nt.links.new(dif.outputs['BSDF'], nt.nodes['Material Output'].inputs['Surface'])
fl.data.materials.append(mf)


def area(loc, target, size, power, color, size_y=None, spread=180):
    l = bpy.data.lights.new('a', 'AREA'); l.energy = power; l.color = color; l.size = size; l.spread = math.radians(spread)
    if size_y: l.shape = 'RECTANGLE'; l.size_y = size_y
    o = bpy.data.objects.new('a', l); sc.collection.objects.link(o); o.location = loc
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


area((-0.26, -0.34, 0.3), (0, 0, 0.15), 0.12, 2.6, (1.0, 0.94, 0.86), size_y=0.32, spread=35)  # principal cálida, acotada a la botella
area((0.34, 0.3, 0.13), (0, 0, 0.13), 0.03, 26, (0.78, 1.0, 0.0), size_y=0.26, spread=12)   # contraluz lima
area((-0.34, 0.3, 0.13), (0, 0, 0.13), 0.03, 9, (0.85, 0.92, 1.0), size_y=0.26, spread=12)   # filo frío
area((0.0, 0.5, 0.2), (0, 0, 0.12), 0.06, 16, (1.0, 0.85, 0.6), size_y=0.18, spread=14)   # brillo a través del líquido
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)

cd = bpy.data.cameras.new('c'); cd.lens = 70; cd.sensor_fit = 'VERTICAL'; cd.sensor_height = 24
cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0.0, -1.0, 0.17); look = Vector((0, 0, 0.122))
cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Y').to_euler()
cd.dof.use_dof = True; cd.dof.focus_distance = 1.0; cd.dof.aperture_fstop = 5.6

sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 16; sc.cycles.transmission_bounces = 16; sc.cycles.transparent_max_bounces = 16
sc.cycles.caustics_refractive = False; sc.cycles.caustics_reflective = False  # sin charcos de luz en el suelo
sc.render.resolution_x = RW; sc.render.resolution_y = RH
sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = 0.1
try: sc.view_settings.look = 'AgX - Punchy'
except Exception: pass
bpy.context.view_layer.update()


def proj(p):
    c = world_to_camera_view(sc, cam, Vector(p)); return [round(c.x, 4), round(1 - c.y, 4)]


# Zonas de interés sobre la cara visible y silueta (contorno izquierdo + derecho)
data = {
    'cap': proj((0, -0.0148, 0.228)),
    'shoulder': proj((0, -0.029, 0.17)),
    'label': proj((0, -0.0352, 0.093)),
    'labelHi': proj((0, -0.0352, 0.112)),
    'base': proj((0, -0.0345, 0.02)),
}
outline = [(0.0152, 0.2195), (0.0148, 0.2335)] + [(r, z) for r, z in PROFILE if r > 0 and z < 0.215]
outline = [(0.0352, z) if 0.064 <= z <= 0.122 else (r, z) for r, z in outline]
right = [proj((r, 0, z)) for r, z in sorted(set(outline), key=lambda t: -t[1])]
left = [proj((-r, 0, z)) for r, z in sorted(set(outline), key=lambda t: t[1])]
data['_shape'] = right + left
sc.render.filepath = OUT; sc.render.image_settings.file_format = 'PNG'
bpy.ops.render.render(write_still=True)
json.dump(data, open(os.path.splitext(OUT)[0] + '.json', 'w'), indent=1)
print('BOTTLE', json.dumps(data))
