# Duplicate selected controls and append "_match" in their name

import bpy
obj_list = bpy.context.selected_objects


for obj in obj_list:
    col = obj.users_collection[0]
    duplicate = obj.copy()
    col.objects.link(duplicate)
    duplicate.name = obj.name + '_match'


#######################
# For all selected objects with "_match" in their name, add LOC and ROT constraints with an armature as a target

import bpy
obj_list = bpy.context.selected_objects

armature = 'Joints.001'

for obj in bpy.context.selected_objects:
    
    
    if '_match' in obj.name:
        loc_constraint = obj.constraints.new('COPY_LOCATION')
        rot_constraint = obj.constraints.new('COPY_ROTATION')
        
        loc_constraint.target = bpy.data.objects[armature]
        rot_constraint.target = bpy.data.objects[armature]

########################
# Ideally there should be also a line for adding subtarget but since control and joints have different naming convention. 
# Have to perform this manually
