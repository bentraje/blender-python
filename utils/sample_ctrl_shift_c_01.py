import bpy


class SimpleCustomMenu(bpy.types.Menu):
    bl_label = "Simple Custom Menu"
    bl_idname = "OBJECT_MT_simple_custom_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.textopbasic", text= "Text Tool", icon= 'OUTLINER_OB_FONT')

class WM_OT_textOpBasic(bpy.types.Operator):
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


classes = [SimpleCustomMenu, WM_OT_textOpBasic]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:     
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

    # The menu can also be called from scripts
    bpy.ops.wm.call_menu(name=SimpleCustomMenu.bl_idname)
