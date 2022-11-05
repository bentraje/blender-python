import bpy

# Parenting the duplicate joint_ret to the joint

for bone in bpy.context.selected_editable_bones:
    sub_target = bone.name[:-4]
    print (bone.name)
    print (sub_target)
    # target = bpy.data.objects['Deformation'].data.bones[sub_target]
    # EditBone.parent expected a EditBone type, not Bone
    target = bpy.data.objects['Deformation'].data.edit_bones[sub_target]
    bone.parent = target
