# Copy Loc Constraint Delete

import bpy

obj_list = bpy.context.selected_objects

driver = obj_list[0]
driven = obj_list[1]

loc_constraint = driven.constraints.new('COPY_LOCATION')
rot_constraint = driven.constraints.new('COPY_ROTATION')

loc_constraint.target = driver
rot_constraint.target = driver

#apply transform
bpy.ops.object.visual_transform_apply()

driven.constraints.remove(loc_constraint)
driven.constraints.remove(rot_constraint)

