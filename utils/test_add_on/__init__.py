bl_info = {
    "name": "Test_addon",
    "author": "jayanam",
    "description": "Simple Test Addon",
    "blender": (2,80,0),
    "location": "View3D",
    "warning": "",
    "category": "Generic"
}


import bpy

from . test_op import Test_OT_Operator
from . test_panel import Test_PT_Panel

classes = (Test_OT_Operator, Test_PT_Panel)


register, unregister = bpy.utils.register_classes_factory(classes)