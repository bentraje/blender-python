import bpy
from bpy.props import BoolProperty, PointerProperty, \
    StringProperty, EnumProperty
import bmesh
import os
import subprocess
from math import pi, cos, sin, radians
from mathutils import Euler

from . import DEBUG, EXRS, FORMATS, __name__
from . import find_layer, append_element, append_material, append_hdr, append_particles
from . import preview_collections


def purge(data):
    # RENDER PREVIEW SCENE PREPARATION METHODS
    for el in data:
        if el.users == 0:
            data.remove(el)


def prepare_scene(blendFile):
    # RENDER PREVIEW SET SCENE
    for ob in bpy.data.objects:
        ob.hide_select = False
        ob.hide_render = False
        ob.hide_viewport = False
        ob.hide_set(False)
    for coll in bpy.data.collections:
        coll.hide_select = False
        coll.hide_render = False
        coll.hide_viewport = False
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)
    purge(bpy.data.collections)
    purge(bpy.data.objects)
    purge(bpy.data.cameras)
    purge(bpy.data.lights)
    purge(bpy.data.meshes)
    purge(bpy.data.particles)
    purge(bpy.data.materials)
    purge(bpy.data.textures)
    purge(bpy.data.images)
    purge(bpy.data.collections)
    # set output
    eevee = bpy.context.scene.eevee
    render = bpy.context.scene.render
    eevee.use_ssr_refraction = True
    eevee.use_ssr = True
    eevee.use_gtao = True
    eevee.gtao_distance = 1
    render.filepath = os.path.splitext(blendFile)[0]
    render.stamp_note_text = os.path.splitext(blendFile)[1][1:].upper()
    render.film_transparent = True
    render.resolution_x = 200
    render.resolution_y = 200
    render.use_stamp_date = False
    render.use_stamp_render_time = False
    render.use_stamp_camera = False
    render.use_stamp_scene = False
    render.use_stamp_filename = False
    render.use_stamp_frame = False
    render.use_stamp_time = False
    render.use_stamp = True
    render.use_stamp_note = True
    render.stamp_font_size = 20
    render.image_settings.file_format = 'PNG'
    render.image_settings.color_mode = 'RGBA'


def add_camera():
    cam = bpy.data.cameras.new('SAM_cam')
    cam_ob = bpy.data.objects.new('SAM_cam_ob', cam)
    bpy.context.collection.objects.link(cam_ob)
    cam_ob.rotation_euler = (pi / 2, 0, -pi / 6)
    cam.shift_y = -.3
    cam.lens = 71
    bpy.data.scenes[0].camera = cam_ob
    bpy.ops.view3d.camera_to_view_selected()
    return cam_ob


def rot_point(point, angle):
    angle = radians(angle)
    x, y = point
    rx = x * cos(angle) - y * sin(angle)
    ry = x * sin(angle) + y * cos(angle)
    return (rx, ry)


def rotate_uv(ob, angle):
    UV = ob.data.uv_layers[0]
    for v in ob.data.loops:
        UV.data[v.index].uv = rot_point(UV.data[v.index].uv, angle)


def set_scene_material(blendFile, cam):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,
                                         ring_count=32,
                                         location=(0, 0, 0))
    ob = bpy.context.active_object
    bpy.ops.object.editmode_toggle()
    bpy.ops.uv.sphere_project(direction='ALIGN_TO_OBJECT')
    mesh = bmesh.from_edit_mesh(ob.data)
    for v in mesh.verts:
        v.select = True if v.co[1] < 0 else False
    bmesh.update_edit_mesh(ob.data)
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.uv.unwrap(method='CONFORMAL', margin=0)
    # bpy.ops.uv.pack_islands()
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.uv.unwrap(method='CONFORMAL', margin=0)
    # bpy.ops.uv.pack_islands()
    bpy.ops.object.editmode_toggle()
    rotate_uv(ob, 46.5)
    bpy.ops.object.shade_smooth()
    bpy.ops.object.material_slot_add()
    # append material
    files = append_material(blendFile)
    name = files[0]['name']
    mat = bpy.data.materials[name]
    ob.material_slots[0].material = mat
    # modify camera settings
    cam.rotation_euler = Euler((pi / 2, 0, 0), 'XYZ')
    cam.data.shift_y = 0
    cam.data.lens = 41


def set_scene_hdr(blendFile, cam):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,
                                         ring_count=32,
                                         location=(0, 0, 0))
    bpy.ops.object.shade_smooth()
    bpy.ops.object.material_slot_add()
    bpy.ops.material.new()
    ob = bpy.context.active_object
    mat = bpy.data.materials[-1]
    ob.material_slots[0].material = mat
    shader = mat.node_tree.nodes['Principled BSDF']
    shader.inputs['Metallic'].default_value = 1
    shader.inputs['Roughness'].default_value = 0
    append_hdr(blendFile)
    cam.rotation_euler = Euler((pi / 2, 0, 0), 'XYZ')
    cam.data.shift_y = 0
    cam.data.lens = 41


def set_scene_particle_settings(blendFile):
    lay_coll = find_layer(bpy.context.scene.collection)
    bpy.context.view_layer.active_layer_collection = lay_coll
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64,
                                         ring_count=32,
                                         enter_editmode=True,
                                         location=(0, 0, 0))
    bpy.ops.uv.sphere_project()
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.shade_smooth()
    sphere = bpy.context.active_object
    files = append_particles(blendFile)
    for f in files:
        name = f['name']
        bpy.ops.object.particle_system_add()
        settings = bpy.data.particles[name]
        sphere.particle_systems[-1].settings = settings
        # for render preview
        settings.child_nbr = settings.rendered_child_count
    bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.data.objects:
        if ob.type == 'CAMERA' or ob == sphere:
            pass
        else:
            ob.select_set(True)
    bpy.context.view_layer.objects.active = sphere
    bpy.data.collections['Assets'].hide_viewport = True
    sphere.select_set(True)
    sphere.particle_systems[-1].seed = 1


class SAM_OT_render_previews(bpy.types.Operator):
    bl_idname = "asset_manager.render_previews"
    bl_label = "(re)Render all previews"

    sub_process: BoolProperty()
    rerender: StringProperty()
    render_env: StringProperty()

    def execute(self, context):
        pref = context.preferences.addons[__name__].preferences
        if self.rerender == '':
            rerender = pref.rerender
        else:
            rerender = True if self.rerender == 'True' else False
        if 'Assets' not in bpy.context.scene.collection.children.keys():
            asset_coll = bpy.data.collections.new('Assets')
            context.scene.collection.children.link(asset_coll)
        else:
            asset_coll = bpy.data.collections['Assets']
        # IF is for rendering in separate blender instance
        if not self.sub_process:
            local_lib = context.scene.asset_manager.local_library
            lib_path = pref.lib_path if local_lib == '' else local_lib 
            lib_path = bpy.path.abspath(lib_path)
            command = [bpy.app.binary_path,
                       "--python-expr",
                       'import bpy;'
                       f'bpy.context.scene.asset_manager.local_library="{lib_path}";'
                       'bpy.ops.asset_manager.render_previews('
                       f'sub_process=True, rerender="{str(rerender)}", '
                       f'render_env="{str(pref.render_env)}");'
                       'bpy.context.preferences.view.use_save_prompt=False;'
                       'bpy.ops.wm.quit_blender();']
            subprocess.Popen(command)
            bpy.context.scene['asset_manager']['cat'] = 0
            pcoll = preview_collections["main"]
            pcoll.clear()
        else:
            lib_path = context.scene.asset_manager.local_library
            for r, d, fs in os.walk(lib_path):
                for f in fs:
                    render_type = 'RENDERED' if f.endswith(
                        ('.hdr', '.exr')) else 'MATERIAL'
                    if f.endswith(FORMATS):
                        blendFile = os.path.join(r, f)
                        png = os.path.splitext(blendFile)[0] + '.png'
                        if not rerender and os.path.exists(png):
                            continue
                        prepare_scene(blendFile)
                        cam = add_camera()
                        if f.endswith(('.hdr', '.exr')):
                            continue
                            # TODO: render previews like texture haven
                            # set_scene_hdr(blendFile, cam)
                        elif 'material' in r.lower():
                            set_scene_material(blendFile, cam)
                        elif 'particle' in r.lower():
                            set_scene_particle_settings(blendFile)
                        elif 'node' in r.lower():
                            pass
                        else:
                            append_element(blendFile)
                        bpy.ops.object.select_all(action='SELECT')
                        bpy.ops.view3d.camera_to_view_selected()
                        cam.data.lens = 40 if 'material' in r.lower() else 70
                        for area in bpy.context.screen.areas:
                            area.type = 'VIEW_3D'
                            space = area.spaces[0]
                            space.region_3d.view_perspective = 'CAMERA'
                            space.shading.type = render_type
                            space.overlay.show_overlays = False
                            if render_type == 'MATERIAL':
                                space.shading.studio_light = self.render_env
                        bpy.ops.render.opengl(write_still=True)
        return{'FINISHED'}
