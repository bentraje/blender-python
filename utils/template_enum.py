import bpy

class ADDONNAME_PT_TemplatePanel(bpy.types.Panel):
    bl_label = "Name of the Panel"
    bl_idname = "ADDONNAME_PT_Template_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Template Tab"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.template_operator")


class ADDONNAME_OT_TemplateOperator(bpy.types.Operator):
    bl_label = "Template Operator"
    bl_idname = "wm.template_operator"

    preset_enum : bpy.props.EnumProperty(
        name = "",
        description = "Select an option",
        items = [
            ('OP1', "Cube", "Add a Cube to the scene"),
            ('OP2', "Sphere", ""),
            ('OP3', "Suzanne", "Add a Suzanne to the scene"), 
        ]
    )
    
    another_enum : bpy.props.EnumProperty(
        name = "",
        description = "Select an option",
        items = [
            ('OP1', "Cube", "Add a Cube to the scene"),
            ('OP2', "Sphere", ""),
            ('OP3', "Suzanne", "Add a Suzanne to the scene"), 
        ]
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preset_enum")
        #layout.prop(self, "another_enum")

    def execute (self, context):
        
        if self.preset_enum == 'OP1':
            bpy.ops.mesh.primitive_cube_add()

        if self.preset_enum == 'OP2':
            bpy.ops.mesh.primitive_uv_sphere_add()

        if self.preset_enum == 'OP3':
            bpy.ops.mesh.primitive_monkey_add()


        return {'FINISHED'}

classes = [ADDONNAME_PT_TemplatePanel, ADDONNAME_OT_TemplateOperator]


#def register():
#    for cls in classes:
#        bpy.utils.register_class(cls)
# 
#def unregister():
#    for cls in classes:
#        bpy.utils.unregister_class(cls)
#        

register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
