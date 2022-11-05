import bpy

obj_list = bpy.context.selected_objects

driver = obj_list[0]
driven = obj_list[1]

# Create Offset Object 

offset = bpy.data.objects.new( "empty", None )
#bpy.context.scene.collection.objects.link(offset)
# bpy.data.collections["Collection1"].children.link(bpy.data.collections["Collection2"])
bpy.data.collections["Collection"].objects.link(offset)

offset.select_set(True)

offset.empty_display_size = 2
offset.empty_display_type = 'PLAIN_AXES'   

loc_constraint = offset.constraints.new('COPY_LOCATION')
rot_constraint = offset.constraints.new('COPY_ROTATION')

loc_constraint.target = driven
rot_constraint.target = driven

bpy.ops.object.visual_transform_apply()

offset.constraints.remove(loc_constraint)
offset.constraints.remove(rot_constraint)

offset.parent = driver
offset.matrix_parent_inverse = driver.matrix_world.inverted()

# Constraint Offset to Driver

driver_loc_constraint = driven.constraints.new('COPY_LOCATION')
driver_rot_constraint = driven.constraints.new('COPY_ROTATION')

driver_loc_constraint.target = offset
driver_rot_constraint.target = offset

bpy.ops.object.visual_transform_apply()
