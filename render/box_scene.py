"""Tres versiones de packaging (caja de té ficticia "BRISA") fotografiadas con la misma luz.
Uso: python box_scene.py <ancho> <alto> <samples> <dir_salida>  → box-a.png, box-b.png, box-c.png + boxes.json"""
import bpy, json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

HERE = os.path.dirname(os.path.abspath(__file__))
RW, RH, SAMPLES, OUTD = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
FS = os.environ.get('FONTS_DIR', os.path.join(HERE, 'node_modules', '@fontsource'))
def font(pkg, w, px): return ImageFont.truetype(f'{FS}/{pkg}/files/{pkg}-latin-{w}-normal.woff', int(px))

BW, BH, BD = 0.075, 0.125, 0.06
PPM = 12000
ROT = math.radians(24)
rng = np.random.default_rng(3)

def paper(w, h, rgb, amt=.04):
    n = rng.random((h // 3 + 1, w // 3 + 1)).astype(np.float32)
    n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), np.float32) / 255
    a = np.array(rgb, np.float32)[None, None, :] * (1 - amt / 2 + n[..., None] * amt)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB')

def tex_front(v):
    w, h = int(BW * PPM), int(BH * PPM)
    mm = lambda x: x / 1000 * PPM
    pts = {}
    if v == 'a':
        im = paper(w, h, (27, 30, 34), .06); d = ImageDraw.Draw(im)
        d.text((w / 2, mm(30)), 'BRISA', font=font('space-grotesk', 700, mm(15)), fill=(236, 234, 228), anchor='mm')
        d.line([(mm(14), mm(42)), (w - mm(14), mm(42))], fill=(110, 114, 120), width=6)
        d.text((w / 2, mm(50)), 'INFUSIÓN PREMIUM', font=font('ibm-plex-mono', 500, mm(2.6)), fill=(150, 154, 160), anchor='mm')
        d.text((w / 2, mm(112)), 'TÉ VERDE · 20 SOBRES', font=font('ibm-plex-mono', 500, mm(3)), fill=(150, 154, 160), anchor='mm')
        pts = {'logo': (.5, 30 / 125), 'name': (.5, 112 / 125), 'mid': (.3, .55)}
    elif v == 'b':
        im = paper(w, h, (236, 233, 225)); d = ImageDraw.Draw(im)
        cx, cy, r = w / 2, mm(50), mm(25)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 245, 66))
        leaf = []
        for i in range(81):
            t = i / 80 * 2 * math.pi
            yy = -math.cos(t) * mm(19); xx = math.sin(t) * mm(11) * (math.sin(math.acos(max(-1, min(1, -math.cos(t))))) ** 1.3)
            leaf.append((cx + xx, cy + yy))
        d.polygon(leaf, fill=(24, 26, 28)); d.line([(cx, cy - mm(17)), (cx, cy + mm(17))], fill=(200, 245, 66), width=8)
        d.text((w / 2, mm(92)), 'BRISA', font=font('space-grotesk', 700, mm(12.5)), fill=(20, 22, 26), anchor='mm')
        d.text((w / 2, mm(104)), 'TÉ VERDE · 20 SOBRES', font=font('ibm-plex-mono', 500, mm(3)), fill=(70, 74, 80), anchor='mm')
        pts = {'logo': (.5, 50 / 125), 'brand': (.5, 92 / 125), 'name': (.5, 104 / 125), 'leaf': (.46, 42 / 125)}
    else:
        im = paper(w, h, (246, 245, 241)); d = ImageDraw.Draw(im)
        txt = Image.new('RGBA', (int(mm(100)), int(mm(22))), (0, 0, 0, 0))
        ImageDraw.Draw(txt).text((0, 0), 'BRISA', font=font('space-grotesk', 300, mm(19)), fill=(20, 22, 26, 255))
        txt = txt.rotate(90, expand=True); im.paste(txt, (int(mm(10)), int(mm(18))), txt)
        d.rectangle([mm(40), mm(14), mm(64), mm(15.4)], fill=(20, 22, 26))
        d.text((mm(40), mm(22)), 'TÉ VERDE', font=font('ibm-plex-mono', 500, mm(2.8)), fill=(70, 74, 80))
        d.text((mm(40), mm(27)), '20 SOBRES', font=font('ibm-plex-mono', 500, mm(2.8)), fill=(70, 74, 80))
        pts = {'logo': (.25, .55), 'name': (.65, .19), 'low': (.5, .85)}
    return im, pts

def tex_side(v):
    w, h = int(BD * PPM), int(BH * PPM)
    base = {'a': (27, 30, 34), 'b': (236, 233, 225), 'c': (246, 245, 241)}[v]
    ink = (150, 154, 160) if v == 'a' else (90, 94, 100)
    im = paper(w, h, base, .05); d = ImageDraw.Draw(im); mm = lambda x: x / 1000 * PPM
    for i, line in enumerate(['INGREDIENTES: TÉ VERDE', 'SENCHA 100 %', '', '20 SOBRES × 2 g', 'INFUSIONAR 3 MIN · 80 °C']):
        d.text((mm(6), mm(70) + i * mm(5)), line, font=font('ibm-plex-mono', 500, mm(2.4)), fill=ink)
    return im

def make_scene(v):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, BH / 2)); box = bpy.context.active_object
    box.scale = (BW, BD, BH); bpy.ops.object.transform_apply(scale=True)
    bv = box.modifiers.new('b', 'BEVEL'); bv.width = 0.0012; bv.segments = 4
    front, pts = tex_front(v); side = tex_side(v)
    fp = os.path.join(OUTD, f'_front_{v}.png'); sp_ = os.path.join(OUTD, f'_side_{v}.png'); front.save(fp); side.save(sp_)
    def mat(name, img_path, rough):
        m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
        t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(img_path)
        nt.links.new(t.outputs['Color'], b.inputs['Base Color']); b.inputs['Roughness'].default_value = rough
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1500
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = .12; bp.inputs['Distance'].default_value = .0003
        nt.links.new(nz.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
        return m
    body = mat('body', sp_, .62); box.data.materials.append(body)
    # planos impresos (frente y lateral izquierdo)
    def plane(img, mat_, loc, rot, sx, sy):
        bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot); p = bpy.context.active_object
        p.scale = (sx, sy, 1); bpy.ops.object.transform_apply(scale=True); p.data.materials.append(mat_); return p
    fplane = plane(fp, mat('front', fp, .5), (0, -BD / 2 - 0.0002, BH / 2), (math.pi / 2, 0, 0), BW - 0.0016, BH - 0.0016)
    splane = plane(sp_, mat('side', sp_, .55), (-BW / 2 - 0.0002, 0, BH / 2), (math.pi / 2, 0, -math.pi / 2), BD - 0.0016, BH - 0.0016)
    for o in (box, fplane, splane):
        o.rotation_euler.z += ROT; o.location = Vector(o.location);
    # rotar alrededor del origen
    import mathutils
    R = mathutils.Matrix.Rotation(ROT, 4, 'Z')
    for o in (fplane, splane):
        o.location = (R @ Vector((*o.location[:2], o.location[2], 1)).to_3d()) if False else R.to_3x3() @ Vector(o.location)
    # suelo y fondo
    bpy.ops.mesh.primitive_plane_add(size=4); fl = bpy.context.active_object
    mf = bpy.data.materials.new('slate'); mf.use_nodes = True; nt = mf.node_tree; b = nt.nodes['Principled BSDF']
    n1 = nt.nodes.new('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 60; n1.inputs['Detail'].default_value = 10
    c1 = nt.nodes.new('ShaderNodeValToRGB'); c1.color_ramp.elements[0].color = (0.006, 0.006, 0.007, 1); c1.color_ramp.elements[1].color = (0.022, 0.022, 0.024, 1)
    nt.links.new(n1.outputs['Fac'], c1.inputs['Fac']); nt.links.new(c1.outputs['Color'], b.inputs['Base Color'])
    b.inputs['Roughness'].default_value = 0.62; b.inputs['Specular IOR Level'].default_value = 0.25
    fl.data.materials.append(mf)
    def area(loc, target, size, power, color, size_y=None, spread=180):
        l = bpy.data.lights.new('a', 'AREA'); l.energy = power; l.color = color; l.size = size; l.spread = math.radians(spread)
        if size_y: l.shape = 'RECTANGLE'; l.size_y = size_y
        o = bpy.data.objects.new('a', l); sc.collection.objects.link(o); o.location = loc
        o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    area((-0.32, -0.55, 0.42), (0, 0, 0.07), 0.45, 22, (1.0, 0.94, 0.86))
    area((0.22, 0.2, 0.09), (0, -0.02, 0.12), 0.05, 12, (0.78, 1.0, 0.0), size_y=0.3, spread=30)
    area((0.5, -0.55, 0.15), (0, 0, 0.06), 0.7, 1.6, (0.9, 0.95, 1.0))
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs['Color'].default_value = (0, 0, 0, 1)
    cd = bpy.data.cameras.new('c'); cd.lens = 75; cd.sensor_fit = 'VERTICAL'; cd.sensor_height = 24
    cam = bpy.data.objects.new('c', cd); sc.collection.objects.link(cam); sc.camera = cam
    cam.location = (0.0, -0.62, 0.14); look = Vector((0, 0, 0.066))
    cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Y').to_euler()
    fo = bpy.data.objects.new('f', None); sc.collection.objects.link(fo); fo.location = R.to_3x3() @ Vector((0, -BD / 2, BH * .55))
    cd.dof.use_dof = True; cd.dof.focus_object = fo; cd.dof.aperture_fstop = 4
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
    sc.render.resolution_x = RW; sc.render.resolution_y = RH
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.exposure = -0.1
    try: sc.view_settings.look = 'AgX - Punchy'
    except Exception: pass
    bpy.context.view_layer.update()
    def proj(u, vv):
        p = R.to_3x3() @ Vector(((u - .5) * BW, -BD / 2, BH * (1 - vv)))
        c = world_to_camera_view(sc, cam, p); return [round(c.x, 4), round(1 - c.y, 4)]
    out = {k: proj(*uv) for k, uv in pts.items()}
    out['_box'] = [proj(0, 0), proj(1, 0), proj(1, 1), proj(0, 1)]
    sc.render.filepath = os.path.join(OUTD, f'box-{v}.png'); sc.render.image_settings.file_format = 'PNG'
    bpy.ops.render.render(write_still=True)
    return out

res = {v: make_scene(v) for v in ('a', 'b', 'c')}
json.dump(res, open(os.path.join(OUTD, 'boxes.json'), 'w'), indent=1)
print('BOXES', json.dumps(res))
