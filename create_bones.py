import bpy, bmesh

arm_obj = bpy.data.objects['Armature']
# must be in edit mode to add bones
bpy.context.scene.objects.active = arm_obj
bpy.ops.object.mode_set(mode='EDIT', toggle=False)
edit_bones = arm_obj.data.edit_bones

b = edit_bones.new('bone1')
# a new bone will have zero length and not be kept
# move the head/tail to keep the bone
b.head = (1.0, 1.0, 0.0)
b.tail = (1.0, 1.0, 1.0)

b = edit_bones.new('bone2')
b.head = (1.0, 2.0, 0.0)
b.tail = (1.0, 2.0, 1.0)

# exit edit mode to save bones so they can be used in pose mode
bpy.ops.object.mode_set(mode='OBJECT')

# make the custom bone shape
bm = bmesh.new()
bmesh.ops.create_circle(bm, cap_ends=False, diameter=0.2, segments=8)
me = bpy.data.meshes.new("Mesh")
bm.to_mesh(me)
bm.free()
b2_shape = bpy.data.objects.new("bone2_shape", me)
bpy.context.scene.objects.link(b2_shape)
b2_shape.layers = [False]*19+[True]

# use pose.bones for custom shape
arm_obj.pose.bones['bone2'].custom_shape = b2_shape
# use data.bones for show_wire
arm_obj.data.bones['bone2'].show_wire = True