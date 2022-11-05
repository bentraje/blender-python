# ##### BEGIN LICENSE BLOCK #####
#
#  Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) 
#
#  This work is licensed under the Creative Commons
#  Attribution-NonCommercial-NoDerivatives 4.0 International License. 
#
#  To view a copy of this license,
#  visit http://creativecommons.org/licenses/by-nc-nd/4.0/.
#
# ##### END LICENSE BLOCK #####

bl_info = {
    "name": "Text Tool",
    "author": "Darkfall",
    "version": (1, 3),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Text Tool Tab",
    "description": "Adds a new Text Object with user defined properties, Typewriter / Scrolling Text Animation, Radial Curve tool",
    "warning": "",
    "wiki_url": "",
    "category": "Add Text",
}

import bpy
from bpy.types import (Panel, Operator)


class OBJECT_PT_TextTool(Panel):
    bl_label = " "
    bl_idname = "OBJECT_PT_texttool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Text Tool"
    
    def draw_header(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Text Tool", icon= 'EVENT_T')
    

    def draw(self, context):
        layout = self.layout

        row = layout.split(factor= 0.45)
        row.label(text= "")
        row.operator("wm.textopbasic", text= "Text Tool", icon= 'OUTLINER_OB_FONT')
        
          
class WM_OT_textOpBasic(Operator):
    """Open the Text Tool Dialog Box"""
    bl_idname = "wm.textopbasic"
    bl_label = "                            Text Tool Operator"
    

    
    text : bpy.props.StringProperty(name="", default="")
    scale : bpy.props.FloatProperty(name= "", default= 1)
    rotation : bpy.props.BoolProperty(name= "Orientation", default= False)
    center : bpy.props.BoolProperty(name= "Alignment", default= False)
    extrude : bpy.props.BoolProperty(name= "Extrude", default= False)
    extrude_amount : bpy.props.FloatProperty(name= "Extrude Amount", default= 0.06)
    italic : bpy.props.BoolProperty(name= "Auto Italic", default = False)
    options : bpy.props.BoolProperty(name= "Options", default = False)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
        
    def draw(self, context):
        layout = self.layout
        layout.separator(factor= 1)
        
        row = layout.row()
        row.label(text= "Enter Text:", icon = 'FILE_TEXT')
        row.prop(self, "text")
        
        row = layout.row()
        row.label(text= "Scale:", icon = 'EMPTY_ARROWS')
        row.prop(self, "scale")
        
        layout.separator(factor= 1)
        
        box = layout.box()
        
        row = box.row()
        row.prop(self, "options")
        if self.options == True:
        
            row = box.row()
            row = box.row()
            row.prop(self, "italic")
            if self.italic == True:
                row.label(text= "Italic: Enabled", icon = 'ITALIC')
            else: 
                row.label(text= "Italic: Not Enabled", icon = 'DRIVER_DISTANCE')
                    
            row = box.row()
            row.prop(self, "rotation")
            if self.rotation == True:
                row.label(text= "Orientation: Z UP", icon= 'EMPTY_SINGLE_ARROW')
            else:
                row.label(text= "Orientation: Default", icon= 'ARROW_LEFTRIGHT')
                    
            
            
            row = box.row()
            row.prop(self, "center")
            if self.center == True:
                row.label(text= "Alignment: Center", icon= 'ALIGN_CENTER')
            else:
                row.label(text= "Alignment: Default", icon= 'ALIGN_LEFT')
            
            
            
            row = box.row()
            row.prop(self, "extrude")
            if self.extrude == True:
                row.prop(self, "extrude_amount")
            
        layout.separator(factor= 1)    
            
        

    def execute(self, context):
        
        t = self.text
        s = self.scale
        c = self.center
        e = self.extrude
        ea = self.extrude_amount
        r = self.rotation
        
        bpy.ops.object.text_add(enter_editmode=True)
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        bpy.ops.font.text_insert(text= t)
        bpy.ops.object.editmode_toggle()
        bpy.context.object.data.size = s
        if r == True:
            bpy.context.object.rotation_euler[0] = 1.5708    
        if e == True:
            bpy.context.object.data.extrude = ea
        if c == True:
            bpy.context.object.data.align_x = 'CENTER'
            bpy.context.object.data.align_y = 'CENTER'
            
        if self.italic == True:
            bpy.context.object.data.shear = 0.38
        
        bpy.context.object.name = self.text + " : (font)"    
    
        return {'FINISHED'}



classes = [OBJECT_PT_TextTool, WM_OT_textOpBasic]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)



if __name__ == "__main__":
    register()
