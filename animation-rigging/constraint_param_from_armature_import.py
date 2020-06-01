"""
Name: Constraint Parameter from Armature (Import)
Author: Ben Traje
Notes:
  1) To be used with the import/export equivalent
"""

import json
import bpy

new_armature = bpy.data.objects['metarig_new']

with open("D:/constraint_param.json", "r") as read_file:
    data = json.load(read_file)

    for bone_name, constraint_list in data.items():

        for param_name, constraint_param in constraint_list.items():
            new_bone = new_armature.pose.bones[bone_name]

            new_constraint  = new_bone.constraints.new(param_name)
            target          = bpy.data.objects[constraint_param['target']]                           
            new_constraint.target       = target
            new_constraint.subtarget    = constraint_param['subtarget']
            new_constraint.target_space = constraint_param['target_space']
            new_constraint.owner_space  = constraint_param['owner_space']
            new_constraint.invert_x = constraint_param['invert_x']
            new_constraint.invert_y = constraint_param['invert_y']
            new_constraint.invert_z = constraint_param['invert_z']       


