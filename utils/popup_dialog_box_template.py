import bpy


class WM_OT_myOp(bpy.types.Operator):
    """Open the Add Cube Dialog Box"""
    bl_label = " Add Cube Dialog Box"
    bl_idname = "wm.myop"
    
    text = bpy.props.StringProperty(name = "Enter Text", default ="")
    scale = bpy.props.FloatVectorProperty(name = "scale Z Axis", default = (1,1,1))
    
    def execute(self, context):
                
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.object # Automatically selects the cube above? 
        obj.name = self.text
        obj.scale[0] = self.scale[0]
        obj.scale[1] = self.scale[1]
        obj.scale[2] = self.scale[2]        
        
        return {'FINISHED'}
    
    def invoke(self, context, event): 
        
        return context.window_manager.invoke_props_dialog(self)
    

def register():
    bpy.utils.register_class(WM_OT_myOp)
    

def unregister():
    bpy.utils.unregister_class(WM_OT_myOp)
    

if __name__ == "__main__":
    register()
    
    bpy.ops.wm.myop('INVOKE_DEFAULT')