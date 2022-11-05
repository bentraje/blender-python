import bpy

# Constraint ret joint to tgt joint

# TypeError: 'NoneType' object is not iterable
# Means you are not in the pose mode

src = bpy.data.objects['Deformation.001']

for bone in bpy.context.selected_pose_bones:
    loc_cons = bone.constraints.new('COPY_LOCATION')
    rot_cons = bone.constraints.new('COPY_ROTATION')
    loc_cons.target = src
    rot_cons.target = src
    sub_target = bone.name[:-4]
    loc_cons.subtarget = sub_target    
    rot_cons.subtarget = sub_target
            
    #bpy.ops.object.visual_transform_apply()
    bpy.ops.pose.visual_transform_apply()
    bpy.ops.pose.armature_apply(selected=False)
    
    bone.constraints.remove(loc_cons)
    bone.constraints.remove(rot_cons)




