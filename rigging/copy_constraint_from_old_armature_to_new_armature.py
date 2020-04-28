"""
Name: Copy Constraints From Old Armature to New Armature
Author: Ben Traje
Notes:
  1) Written for COPY_LOCATION and COPY_ROTATION Constraint with Armature as the Target Object
"""


import bpy

old_armature = bpy.data.objects['metarig_old']
new_armature = bpy.data.objects['metarig_new']
old_bone_list = old_armature.pose.bones

for old_bone in old_bone_list:
    
    if old_bone.constraints:
        
        for old_constraint in old_bone.constraints: 
            
            if old_constraint.target.type == 'ARMATURE':                
            
                new_bone = new_armature.pose.bones[old_bone.name]
                new_constraint = new_bone.constraints.new(old_constraint.type)
                                
                new_constraint.target = old_constraint.target
                new_constraint.subtarget = old_constraint.subtarget
                new_constraint.target_space = old_constraint.target_space
                new_constraint.owner_space = old_constraint.owner_space
                
                new_constraint.invert_x = old_constraint.invert_x
                new_constraint.invert_x = old_constraint.invert_y
                new_constraint.invert_x = old_constraint.invert_z
                
            else:
                pass
            
    else:
        pass
