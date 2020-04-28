"""
Name: Constraint Parameter from Armature (Export)
Author: Ben Traje
Notes:
  1) To be used with the import/export equivalent
"""

import bpy
import json

old_armature = bpy.data.objects['Armature_proxy']
old_bone_list = old_armature.pose.bones

param_dict = {}


for old_bone in old_bone_list:
    
    if old_bone.constraints:
        
        constraint_dict = {}
        
        for old_constraint in old_bone.constraints: 
                    
            if old_constraint.target.type == 'ARMATURE':
                
                constraint_dict.update(
                    {old_constraint.type:
                        {
                        'target': old_constraint.target.name,
                        'subtarget': old_constraint.subtarget,
                        'target_space': old_constraint.target_space,
                        'owner_space': old_constraint.owner_space,
                        'invert_x': old_constraint.invert_x,
                        'invert_y': old_constraint.invert_y,
                        'invert_z': old_constraint.invert_z,
                        }
                    }
                )               
            
                
            else:
                pass
    
        param_dict.update(
            {old_bone.name: constraint_dict}
    
        )
            
    else:
        pass

with open("D:/constraint_param.json", "w") as write_file:
    json.dump(param_dict, write_file, indent=4)
