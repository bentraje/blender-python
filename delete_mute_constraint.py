import bpy





bone_list = ["Equipment.L", "Equipment.R", "Band.Tweak.R", "Band.Tweak.L", "Equipment.L.offset", "torso", "hips", "chest", "spine_fk", "tweak_spine", "toe.L", "toe.R", "thigh_parent.L", "thigh_ik.L", "thigh_parent.R", "thigh_ik.R", "spine_fk.001", "tweak_spine.001", "spine_fk.002", "tweak_spine.002", "spine_fk.003", "tweak_spine.003",
    "thumb.01_master.L", "thumb.01.L", "thumb.02.L", "thumb.03.L", "thumb.01.L.001",
    "upper_arm_parent.L", "upper_arm_fk.L", "forearm_fk.L", "hand_fk.L", "upper_arm_ik.L",
    "f_index.01_master.L", "f_index.01.L", "f_index.02.L", "f_index.03.L", "f_index.01.L.001",
    "f_middle.01_master.L", "f_middle.01.L", "f_middle.02.L", "f_middle.03.L", "f_middle.01.L.001",
    "f_ring.01_master.L", "f_ring.01.L", "f_ring.02.L", "f_ring.03.L", "f_ring.01.L.001",
    "f_pinky.01_master.L", "f_pinky.01.L", "f_pinky.02.L", "f_pinky.03.L", "f_pinky.01.L.001",
    "palm.L",
    "thumb.01_master.R", "thumb.01.R", "thumb.02.R", "thumb.03.R", "thumb.01.R.001", 
    "upper_arm_parent.R", "upper_arm_ik.R",
    "f_index.01_master.R", "f_index.01.R", "f_index.02.R", "f_index.03.R", "f_index.01.R.001",
    "f_middle.01_master.R", "f_middle.01.R", "f_middle.02.R", "f_middle.03.R", "f_middle.01.R.001", 
    "f_ring.01_master.R", "f_ring.01.R", "f_ring.02.R", "f_ring.03.R", "f_ring.01.R.001",
    "f_pinky.01_master.R", "f_pinky.01.R", "f_pinky.02.R", "f_pinky.03.R", "f_pinky.01.R.001"
    "palm.R",
    "neck", "head", "tweak_Neck", "shoulder.L", "shoulder.R", "tweak_spine.004", "hand_ik.L", "upper_arm_ik_target.L", "hand_ik.R", "upper_arm_ik_target.R", "foot_ik.L", "foot_spin_ik.L",
    "foot_heel_ik.L", "thigh_ik_target.L", "foot_ik.R", "foot_spin_ik.R", "foot_heel_ik.R", "thigh_ik_target.R"]

for obj in bpy.data.objects:
    obj.select_set(False)

for bone in bone_list:
    bpy.data.objects["Control Rig"].data.bones[bone].select = True

for bone in bpy.context.selected_pose_bones:
    for c in bone.constraints:
        bone.constraints.remove(c)  # Remove constraint
        c.mute = True

        



# bpy.data.objects["Control Rig"].data.bones["f_pinky.01.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_pinky.02.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_pinky.03.L"].select = True

# bpy.data.objects["Control Rig"].data.bones["f_ring.01.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_ring.02.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_ring.03.L"].select = True

# bpy.data.objects["Control Rig"].data.bones["f_middle.01.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_middle.02.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_middle.03.L"].select = True

# bpy.data.objects["Control Rig"].data.bones["f_index.01.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_index.02.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_index.03.L"].select = True

# bpy.data.objects["Control Rig"].data.bones["thumb.01.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["thumb.02.L"].select = True
# bpy.data.objects["Control Rig"].data.bones["thumb.03.L"].select = True

# bpy.data.objects["Control Rig"].data.bones["f_pinky.01.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_pinky.02.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_pinky.03.R"].select = True

# bpy.data.objects["Control Rig"].data.bones["f_ring.01.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_ring.02.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_ring.03.R"].select = True

# bpy.data.objects["Control Rig"].data.bones["f_middle.01.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_middle.02.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_middle.03.R"].select = True

# bpy.data.objects["Control Rig"].data.bones["f_index.01.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_index.02.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["f_index.03.R"].select = True

# bpy.data.objects["Control Rig"].data.bones["thumb.01.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["thumb.02.R"].select = True
# bpy.data.objects["Control Rig"].data.bones["thumb.03.R"].select = True