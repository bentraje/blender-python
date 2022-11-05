import bpy
from math import pi

# Frame 1
bpy.data.objects['Cube'].keyframe_insert(data_path='location',frame=1)

bpy.context.object.rotation_euler[0] = 0
bpy.data.objects['Cube'].keyframe_insert(data_path='rotation_euler',frame=1)

bpy.context.object.scale[0] = 1
bpy.context.object.scale[1] = 1
bpy.context.object.scale[2] = 1
bpy.data.objects['Cube'].keyframe_insert(data_path='scale',frame=1)

# Frame 1254
bpy.ops.transform.translate(value = (0, 0, 5))
bpy.data.objects['Cube'].keyframe_insert(data_path='location',frame=125)

bpy.context.object.rotation_euler[0] = pi
bpy.data.objects['Cube'].keyframe_insert(data_path='rotation_euler',frame=125)


bpy.data.objects['Cube'].keyframe_insert(data_path='scale',frame=1)
bpy.context.object.scale[0] = 2
bpy.context.object.scale[1] = 2
bpy.context.object.scale[2] = 2
bpy.data.objects['Cube'].keyframe_insert(data_path='scale',frame=125)

# Frame 250
bpy.ops.transform.translate(value = (0, 0, -5))                         
bpy.data.objects['Cube'].keyframe_insert(data_path='location',frame=250)

bpy.context.object.rotation_euler[0] = 2 * pi
bpy.data.objects['Cube'].keyframe_insert(data_path='rotation_euler',frame=125)


bpy.context.object.scale[0] = 1
bpy.context.object.scale[1] = 1
bpy.context.object.scale[2] = 1
bpy.data.objects['Cube'].keyframe_insert(data_path='scale',frame=250)