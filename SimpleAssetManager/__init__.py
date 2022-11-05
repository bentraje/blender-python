# -*- coding: utf-8 -*-
import bpy
from bpy.types import WindowManager
import bpy.utils.previews
from bpy.props import BoolProperty, PointerProperty, \
    StringProperty, EnumProperty
import bmesh
import os
import subprocess
from math import pi, cos, sin, radians
from mathutils import Euler

bl_info = {
    "name": "Simple Asset Manager",
    "description": "Manager for objects, materials, particles, "
                   "hdr. Before official.",
    "author": "Dawid Huczyński",
    "version": (0, 9, 6),
    "blender": (2, 80, 0),
    "location": "View 3D > Properties",
    "wiki_url": "https://gitlab.com/tibicen/simple-asset-manager",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Add Mesh"
}

# TODO: append same object instance not new one
# TODO: textures library
# TODO: row and columns in asset grid goes to preferences?
# TODO: add licence info

import platform
import hashlib
h = platform.node() + platform.system() + platform.processor()
h = hashlib.md5(h.encode())
DEBUG = True if h.hexdigest() == '6bd56b92d9a0dbe4d57802b2050e1ac5' else False
DBG_LIB = '/home/tibicen/Dokumenty/blender-library/'

EXRS = ('city.exr', 'courtyard.exr', 'forest.exr', 'interior.exr',
        'night.exr', 'studio.exr', 'sunrise.exr', 'sunset.exr')
FORMATS = ('.blend', '.obj', '.fbx', '.hdr', '.exr')


def find_layer(coll, lay_coll=None):
    if lay_coll is None:
        lay_coll = bpy.context.view_layer.layer_collection
    if lay_coll.collection == coll:
        return lay_coll
    else:
        for child in lay_coll.children:
            a = find_layer(coll, child)
            if a:
                return a
        return None


def import_scenes_depricated(blendFile, link):
    scenes = []
    with bpy.data.libraries.load(blendFile) as (data_from, data_to):
        for name in data_from.scenes:
            scenes.append({'name': name})
    action = bpy.ops.wm.link if link else bpy.ops.wm.append
    action(directory=blendFile + "/Scene/", files=scenes)
    scenes = bpy.data.scenes[-len(scenes):]


def append_element(blendFile, link=False):
    scenes = []
    asset_coll = bpy.data.collections['Assets']
    coll_name = os.path.splitext(
        os.path.basename(blendFile))[0].title()
    # if coll_name in bpy.data.collections.keys():
    #     bpy.ops.object.collection_instance_add(collection=coll_name)
    # else:
    # TODO instance on first import and hide assets
    obj_coll = bpy.data.collections.new(coll_name)
    asset_coll.children.link(obj_coll)
    obj_lay_coll = find_layer(obj_coll)
    bpy.context.view_layer.active_layer_collection = obj_lay_coll
    objects = []
    if blendFile.endswith('.obj'):
        bpy.ops.import_scene.obj(filepath=blendFile)
    elif blendFile.endswith('.fbx'):
        bpy.ops.import_scene.fbx(filepath=blendFile)
    elif blendFile.endswith('.blend'):
        with bpy.data.libraries.load(blendFile) as (data_from, data_to):
            for name in data_from.scenes:
                scenes.append({'name': name})
        action = bpy.ops.wm.link if link else bpy.ops.wm.append
        action(directory=blendFile + "/Scene/", files=scenes)
        scenes = bpy.data.scenes[-len(scenes):]
        for scene in scenes:
            objs = 0
            for object in scene.collection.objects:
                # TODO: if there is any object in master collection
                obj_coll.objects.link(object)
                objs += 1
                objects.append(object)
            for coll in scene.collection.children:
                if coll.name.startswith('Collection'):
                    for object in coll.objects:
                        obj_coll.objects.link(object)
                        objects.append(object)
                    for sub_coll in coll.children:
                        obj_coll.children.link(sub_coll)
                else:
                    obj_coll.children.link(coll)
            bpy.data.scenes.remove(scene)
        for obj in objects:
            obj.select_set(True)


def append_hdr(blendFile):
    file = os.path.basename(blendFile)
    # check if already loaded
    if file in bpy.data.worlds.keys():
        world = bpy.data.worlds[file]
    else:
        bpy.ops.image.open(filepath=blendFile)
        im = bpy.data.images[file]
        world = bpy.data.worlds.new(file)
        world.use_nodes = True
        nodes = world.node_tree.nodes
        tex = nodes.new('ShaderNodeTexEnvironment')
        tex.image = im
        background = nodes['Background']
        world.node_tree.links.new(background.inputs['Color'],
                                  tex.outputs['Color'])
    bpy.context.scene.world = world


def append_material(blendFile, link=False):
    files = []
    with bpy.data.libraries.load(blendFile) as (data_from, data_to):
        for name in data_from.materials:
            files.append({'name': name})
    action = bpy.ops.wm.link if link else bpy.ops.wm.append
    for file in files:
        if file['name'] not in bpy.data.materials.keys():
            action(directory=blendFile + "/Material/", files=[file, ])
    return files


def append_particles(blendFile, link=False):
    particles = []
    asset_coll = bpy.data.collections['Assets']
    if "Particles" not in bpy.data.collections.keys():
        particles_coll = bpy.data.collections.new('Particles')
        asset_coll.children.link(particles_coll)
    else:
        particles_coll = bpy.data.collections['Particles']
    with bpy.data.libraries.load(blendFile) as (data_from, data_to):
        for name in data_from.particles:
            particles.append({'name': name})
    exists = True
    for name in [x['name'] for x in particles]:
        if name not in bpy.data.particles.keys():
            exists = False
    if exists:
        return particles
    coll_name = os.path.splitext(
        os.path.basename(blendFile))[0].title()
    obj_coll = bpy.data.collections.new(coll_name)
    particles_coll.children.link(obj_coll)
    obj_lay_coll = find_layer(obj_coll)
    bpy.context.view_layer.active_layer_collection = obj_lay_coll
    action = bpy.ops.wm.link if link else bpy.ops.wm.append
    colls = bpy.data.collections[:]
    action(directory=blendFile + "/ParticleSettings/", files=particles)
    # # doublecheck if collections are imported properly
    # for coll in bpy.data.collections:
    #     if coll not in colls:
    #         obj_coll.children.link(coll) # TODO
    #     for obj in coll.objects:
    #         if obj in obj_coll.objects.values():
    #             obj_coll.objects.unlink(obj)
    return particles


def execute_insert(context, link):
    active_layer = context.view_layer.active_layer_collection
    for ob in bpy.context.scene.objects:
        ob.select_set(False)
    bpy.ops.object.select_all(action='DESELECT')
    selected_preview = bpy.data.window_managers["WinMan"].asset_manager_prevs
    folder = os.path.split(os.path.split(selected_preview)[0])[1]
    if 'Assets' not in bpy.context.scene.collection.children.keys():
        asset_coll = bpy.data.collections.new('Assets')
        context.scene.collection.children.link(asset_coll)
    else:
        asset_coll = bpy.data.collections['Assets']
    # Append objects
    if 'material' in folder.lower():
        return append_material(selected_preview, link)
    elif 'particle' in folder.lower():
        files = append_particles(selected_preview, link)
        context.view_layer.active_layer_collection = active_layer
        return files
    elif selected_preview.endswith(('.hdr', '.exr')):
        append_hdr(selected_preview)
    else:
        append_element(selected_preview, link)
        if context.scene.asset_manager.origin:
            if context.scene.asset_manager.incl_cursor_rot:
                temp = context.scene.tool_settings.transform_pivot_point
                context.scene.tool_settings.transform_pivot_point = 'CURSOR'
                cur = context.scene.cursor
                cur_loc = cur.location.copy()
                cur_rot = cur.rotation_euler.copy()
                cur.location = (0, 0, 0)
                cur.rotation_euler = (0, 0, 0)
                for x, y in list(zip(cur_rot, 'XYZ')):
                    bpy.ops.transform.rotate(value=-x, orient_axis=y)
                bpy.ops.transform.translate(value=cur_loc)
                cur.location = cur_loc
                cur.rotation_euler = cur_rot
                context.scene.tool_settings.transform_pivot_point = temp
                # bpy.ops.wm.tool_set_by_id(name="builtin.rotate")
            else:
                cur_loc = context.scene.cursor.location
                bpy.ops.transform.translate(value=cur_loc)
        context.view_layer.active_layer_collection = active_layer


class SAM_OT_LinkButton(bpy.types.Operator):
    bl_idname = "asset_manager.link_object"
    bl_label = "Link"
    bl_description = 'Links object to scene'

    def execute(self, context):
        execute_insert(context, link=True)
        return{'FINISHED'}


class SAM_OT_AppendButton(bpy.types.Operator):
    bl_idname = "asset_manager.append_object"
    bl_label = "Append"
    bl_description = 'Appends object to scene'

    def execute(self, context):
        execute_insert(context, link=False)
        return{'FINISHED'}


class SAM_OT_AppendMaterialButton(bpy.types.Operator):
    bl_idname = "asset_manager.append_material"
    bl_label = "Append"
    bl_description = 'Adds material to blendfile'

    def execute(self, context):
        execute_insert(context, link=False)
        return{'FINISHED'}


class SAM_OT_AddMaterialButton(bpy.types.Operator):
    bl_idname = "asset_manager.add_material"
    bl_label = "Add"
    bl_description = 'Adds material to object'

    def execute(self, context):
        active_ob = context.active_object
        wm = bpy.data.window_managers["WinMan"]
        for ob in bpy.context.scene.objects:
            ob.select_set(False)
        bpy.ops.object.select_all(action='DESELECT')
        selected_preview = wm.asset_manager_prevs
        files = append_material(selected_preview)
        for file in files:
            mat = bpy.data.materials[file['name']]
            active_ob.data.materials.append(mat)
        active_ob.select_set(True)
        return{'FINISHED'}


class SAM_OT_ReplaceMaterialButton(bpy.types.Operator):
    bl_idname = "asset_manager.replace_material"
    bl_label = "Replace"
    bl_description = 'Replace objects material'

    def execute(self, context):
        active_ob = context.active_object
        wm = bpy.data.window_managers["WinMan"]
        for ob in bpy.context.scene.objects:
            ob.select_set(False)
        bpy.ops.object.select_all(action='DESELECT')
        selected_preview = wm.asset_manager_prevs
        files = append_material(selected_preview)
        for file in files:
            mat = bpy.data.materials[file['name']]
            active_ob.data.materials[active_ob.active_material_index] = mat
        active_ob.select_set(True)
        return{'FINISHED'}


class SAM_OT_AddParticlesButton(bpy.types.Operator):
    bl_idname = "asset_manager.add_particles"
    bl_label = "Add to object"
    bl_description = 'Adds particles to object'

    def execute(self, context):
        active_ob = context.active_object
        bpy.ops.object.select_all(action='DESELECT')
        files = execute_insert(context, link=False)
        active_ob.select_set(True)
        for file in files:
            bpy.ops.object.particle_system_add()
            par_sys = active_ob.particle_systems[-1]
            par_sys.settings = bpy.data.particles[file['name']]
            par_sys.name = file['name']
        return{'FINISHED'}


class SAM_OT_OpenButton(bpy.types.Operator):
    bl_idname = "asset_manager.open_file"
    bl_label = "Open File"

    def execute(self, context):
        addon_prefs = context.preferences.addons[__name__].preferences
        wm = bpy.data.window_managers["WinMan"]
        if addon_prefs.opensame:
            selected_preview = wm.asset_manager_prevs
            bpy.ops.wm.open_mainfile(filepath=selected_preview)
        else:
            selected_preview = wm.asset_manager_prevs
            command = [bpy.app.binary_path, selected_preview]
            subprocess.Popen(command)
        return{'FINISHED'}


# Update
def update_category(self, context):
    enum_previews_from_directory_items(self, context)


def search_library(self, context):
    pref = context.preferences.addons[__name__].preferences
    local_lib = context.scene.asset_manager.local_library
    lib_path = pref.lib_path if local_lib == '' else local_lib 
    lib_path = bpy.path.abspath(lib_path)
    empty_path = os.path.join(os.path.dirname(__file__), 'empty.png')
    pcoll = preview_collections["main"]
    keyword = context.scene.asset_manager.search.lower()
    items = []
    enum_items = []
    for r, dirs, files in os.walk(lib_path):
        if keyword in ''.join(files).lower():
            for file in files:
                if keyword in file.lower():
                    prev = scan_for_elements(os.path.join(r, file))
                    if prev:
                        items.append(prev)
    enum_items = gen_thumbnails(items, enum_items, pcoll, empty_path)
    if len(enum_items) == 0:
        if 'empty' in pcoll:
            enum_items.append(('empty', '', "", pcoll['empty'].icon_id, 0))
        else:
            empty = pcoll.load('empty', empty_path, 'IMAGE')
            enum_items.append(('empty', '', '', empty.icon_id, 0))
    pcoll.asset_manager_prevs = enum_items
    bpy.data.window_managers[0]['asset_manager_prevs'] = 0


def subcategory_callout(self, context):
    global subcategories
    pref = context.preferences.addons[__name__].preferences
    local_lib = context.scene.asset_manager.local_library
    lib_path = pref.lib_path if local_lib == '' else local_lib 
    lib_path = bpy.path.abspath(lib_path)
    path = os.path.join(lib_path, self.cat)
    if self.cat in ('.', 'empty'):
        return [('empty', '', '', 0)]
    for r, d, f in os.walk(path):
        subcategories = sorted([(x, x, '', nr + 1) for nr, x in enumerate(d)])
        subcategories.insert(0, ('.', '.', '', 0))
        if len(subcategories) > 1:
            return subcategories
        else:
            context.scene['asset_manager']['subcat'] = 0
            return [('empty', '', '', 0), ]


def categories(self, context):
    global categories
    categories = []
    nr = 0
    pref = context.preferences.addons[__name__].preferences
    local_lib = context.scene.asset_manager.local_library
    lib_path = pref.lib_path if local_lib == '' else local_lib 
    lib_path = bpy.path.abspath(lib_path)
    for el in sorted(os.listdir(lib_path)):
        p = os.path.join(lib_path, el)
        if os.path.isdir(p) and not el.startswith('.'):
            nr += 1
            categories.append((el, el, '', nr))
    categories.insert(0, ('.', '.', '', 0))
    if len(categories) > 1:
        return categories
    else:
        context.scene['asset_manager']['cat'] = 0
        return [('empty', '', '', 0), ]


# Drop Down Menu
class SimpleAssetManager(bpy.types.PropertyGroup):
    cat: EnumProperty(
        items=categories,
        name="Category",
        description="Select a Category",
        update=update_category)

    subcat: EnumProperty(
        items=subcategory_callout,
        name="Subcategory",
        description="Select subcategory",
        update=update_category)

    origin: BoolProperty(
        name='Origin',
        description='Placement location')

    incl_cursor_rot: BoolProperty(
        name='Rotation',
        description='fIncludes cursor rotation on import.')

    search: StringProperty(
        name='Search',
        description='Search through whole library',
        update=search_library)
    
    local_library: StringProperty(
        name="Local/Project Library Path",
        default= '',
        description="SAM uses this path if not empty, otherwise uses master library from preferences.",
        subtype="DIR_PATH")


def scan_for_elements(path):
    if path.lower().endswith(FORMATS):
        png = os.path.splitext(path)[0] + '.png'
        if path.lower().endswith(('.hdr', '.exr')):
            return (path, True)
        elif os.path.exists(png):
            return (path, True)
        else:
            return (path, False)
    else:
        return None


def gen_thumbnails(image_paths, enum_items, pcoll, empty_path):
    # For each image in the directory, load the thumb
    # unless it has already been loaded
    for i, im in enumerate(sorted(image_paths)):
        filepath, prev = im
        name = os.path.splitext(os.path.basename(filepath))[0]
        name = name.replace('.', ' ').replace('_', ' ').lower().capitalize()
        if filepath in pcoll:
            enum_items.append((filepath, name,
                               "", pcoll[filepath].icon_id, i))
        else:
            if prev:
                imgpath = filepath.rsplit('.', 1)[0] + '.png'
                if filepath.endswith(('.hdr', '.exr')):
                    imgpath = filepath
                thumb = pcoll.load(filepath, imgpath, 'IMAGE')
            else:
                thumb = pcoll.load(filepath, empty_path, 'IMAGE')
            enum_items.append((filepath, name,
                               "", thumb.icon_id, i))
    return enum_items


def enum_previews_from_directory_items(self, context):
    # Get the Preview Collection (defined in register func)
    pcoll = preview_collections["main"]
    pref = context.preferences.addons[__name__].preferences
    category = context.scene.asset_manager.cat
    subcategory = context.scene.asset_manager.subcat
    local_lib = context.scene.asset_manager.local_library
    lib_path = pref.lib_path if local_lib == '' else local_lib 
    lib_path = bpy.path.abspath(lib_path)
    empty_path = os.path.join(os.path.dirname(__file__), 'empty.png')
    enum_items = []
    if category in ('empty', '.'):
        directory = lib_path
    elif subcategory in ('empty', '.'):
        directory = os.path.join(lib_path, category)
    else:
        directory = os.path.join(lib_path, category, subcategory)
    # EnumProperty Callback
    if context is None:
        return enum_items
    # wm = context.window_manager
    if directory == pcoll.asset_manager_prev_dir:
        return pcoll.asset_manager_prevs
    print("Simple Asset Manager - Scanning directory: %s" % directory)
    if directory and os.path.exists(directory):
        image_paths = []
        for fn in os.listdir(directory):
            prev = scan_for_elements(os.path.join(directory, fn))
            if prev:
                image_paths.append(prev)

        enum_items = gen_thumbnails(image_paths, enum_items, pcoll,
                                    empty_path)
    # Return validation
    if len(enum_items) == 0:
        if 'empty' in pcoll:
            enum_items.append(('empty', '',
                               "", pcoll['empty'].icon_id, 0))
        else:
            empty = pcoll.load('empty', empty_path, 'IMAGE')
            enum_items.append(('empty', '', '', empty.icon_id, 0))
    pcoll.asset_manager_prevs = enum_items
    pcoll.asset_manager_prev_dir = directory
    bpy.data.window_managers[0]['asset_manager_prevs'] = 0
    return pcoll.asset_manager_prevs


preview_collections = {}


from .previews import SAM_OT_render_previews
from .ui import SAM_UI, SAM_PT_Panel, SAM_PT_Popup, \
    SAM_PT_PrefPanel, SAM_MT_button, SAM_MT_Library_Path


#####################################################################
# Register

classes = (
    SAM_OT_render_previews,
    SAM_OT_LinkButton,
    SAM_OT_AppendButton,
    SAM_OT_AppendMaterialButton,
    SAM_OT_AddMaterialButton,
    SAM_OT_ReplaceMaterialButton,
    SAM_OT_AddParticlesButton,
    SAM_OT_OpenButton,
    SimpleAssetManager,
    SAM_PT_Panel,
    SAM_PT_Popup,
    SAM_PT_PrefPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    WindowManager.asset_manager_prev_dir = StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default="")

    WindowManager.asset_manager_prevs = EnumProperty(
        items=enum_previews_from_directory_items)

    pcoll = bpy.utils.previews.new()
    pcoll.asset_manager_prev_dir = ""
    pcoll.asset_manager_prevs = ""

    preview_collections["main"] = pcoll
    bpy.types.Scene.asset_manager = PointerProperty(
        type=SimpleAssetManager)

    bpy.types.VIEW3D_MT_add.append(SAM_MT_button)
    bpy.types.SCENE_PT_scene.append(SAM_MT_Library_Path)


# Unregister
def unregister():
    bpy.types.VIEW3D_MT_add.remove(SAM_MT_button)
    bpy.types.SCENE_PT_scene.remove(SAM_MT_Library_Path)
    del WindowManager.asset_manager_prevs

    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.asset_manager


if __name__ == "__main__":
    register()
