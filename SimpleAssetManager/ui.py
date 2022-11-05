import bpy 
from bpy.props import BoolProperty, PointerProperty, \
    StringProperty, EnumProperty
import os

from . import DEBUG, DBG_LIB, EXRS, FORMATS, __name__


def SAM_UI(self, context):
    layout = self.layout
    wm = context.window_manager
    manager = context.scene.asset_manager
    # Categories Drop Down Menu
    col = layout.column()
    if manager.cat not in ('empty', ''):
        col.prop(manager, "cat")
    if manager.subcat not in ('empty', ''):
        col.prop(manager, "subcat")
    # search bar
    row = layout.row()
    col.prop(manager, 'search')
    # Previews
    # row = layout.row()
    if wm.asset_manager_prevs not in ('', 'empty'):
        row = layout.row()
        if wm.asset_manager_prevs != 'empty':
            row.template_icon_view(wm, "asset_manager_prevs",
                                   show_labels=True)
        # Materials
        row = layout.row()
        material = 'material' in manager.cat.lower() or \
                   'material' in manager.subcat.lower()
        particle = 'particle' in manager.cat.lower() or \
                   'particle' in manager.subcat.lower()
        hdr = wm.asset_manager_prevs.endswith(('.hdr', '.hdri', '.exr'))
        if material:
            row.operator("asset_manager.append_material")
            row = layout.row()
            row.operator("asset_manager.add_material")
            row = layout.row()
            row.operator("asset_manager.replace_material")
        elif particle:
            row.operator("asset_manager.append_object")
            row = layout.row()
            row.operator("asset_manager.add_particles")
        elif hdr:
            row = layout.row()
            row.operator("asset_manager.append_object")
        else:
            # Objects, HDR, Particles
            origin_btn_name = 'At Origin'
            if manager.origin:
                origin_btn_name = 'At Cursor'
            row.prop(manager, "origin", text=origin_btn_name, toggle=True)
            if manager.origin:
                row.prop(manager, "incl_cursor_rot")
            row = layout.row()
            row.operator("asset_manager.append_object")
        if wm.asset_manager_prevs.endswith('.blend'):
            row = layout.row()
            row.operator("asset_manager.open_file")
            row.operator("asset_manager.link_object")


# Panel
class SAM_PT_Panel(bpy.types.Panel):
    # Create a Panel in the Tool Shelf
    bl_label = "Simple Asset Manager"
    bl_idname = "IMPORT_PT_Asset_Manager"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_options = {"DEFAULT_CLOSED"}

    # Draw
    def draw(self, context):
        SAM_UI(self, context)


class SAM_PT_Popup(bpy.types.Operator):
    """Acces to your Objects Library"""
    bl_idname = "view3d.add_asset"
    bl_label = "Simple Asset Manager"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        SAM_UI(self, context)

    def execute(self, context):
        return {'FINISHED'}


class SAM_PT_PrefPanel(bpy.types.AddonPreferences):
    bl_idname = __name__
    lib_path: StringProperty(
        name="Library Path",
        default= DBG_LIB if DEBUG else os.path.splitdrive(__file__)[0],
        description="Show only hotkeys that have this text in their name",
        subtype="DIR_PATH")

    rerender: BoolProperty(default=False)

    opensame: BoolProperty()

    incl_cursor_rot: BoolProperty(
        name='Rotation',
        description='Include rotation when appending to cursor.')

    exrs = [(exr, exr.replace('.exr', '').title(),
             '', nr) for nr, exr in enumerate(EXRS)]
    render_env: EnumProperty(
        items=exrs,
        name="Render Scene",
        description="With what light the previews.",
        default='interior.exr'
    )

    def draw(self, context):
        manager = context.scene.asset_manager
        layout = self.layout
        col = layout.column()
        col.prop(self, "lib_path", text='Master Library path')
        row = layout.row()
        col.prop(manager, "local_library", text='Local Library path')
        row = layout.row()
        row.operator("asset_manager.render_previews",
                     text="Render missing previews")
        row.prop(self, 'rerender',
                 text='Re-render ALL previews')
        row = layout.row()
        row.prop(self, 'opensame',
                 text='Open file on the same instance')
        row = layout.row()
        row.prop(self, 'render_env', text='Previews render light')


def SAM_MT_button(self, context):
    self.layout.operator(SAM_PT_Popup.bl_idname,
                         text="Simple Asset Manager")


def SAM_MT_Library_Path(self, context):
    asset = context.scene.asset_manager
    layout = self.layout
    layout.label(text="Simple Asset Manager:")
    layout.prop(asset, "local_library")


