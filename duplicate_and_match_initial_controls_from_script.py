'''
Used for matching orientation of the initial controls (from the script) to the static, reorient joints
'''

import bpy
obj_list = bpy.context.selected_objects


'''
for obj in obj_list:
    col = obj.users_collection[0]
    duplicate = obj.copy()
    col.objects.link(duplicate)
    duplicate.name = obj.name + '_match'



'''

for obj in bpy.context.selected_objects:
    
    
    if '_match' in obj.name:
        loc_constraint = obj.constraints.new('COPY_LOCATION')
        rot_constraint = obj.constraints.new('COPY_ROTATION')
        
        loc_constraint.target = bpy.data.objects['Joints.001']
        rot_constraint.target = bpy.data.objects['Joints.001']