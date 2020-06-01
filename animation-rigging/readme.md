# General

* Like in the viewport, you need to access armature/bones in Python in three separate methods: vanilla bones, edit bones and pose bones. In addition, when you execute a method, you need to be in the proper mode in the viewport otherwise you'll get a None. You'll get more details in the bones section of the API documentation. 
    * Blender Python API Documentation: Strictly speaking PoseBone’s are not bones, they are just the state of the armature, stored in the bpy.types.Object rather than the bpy.types.Armature, the real bones are however accessible from the pose bones - bpy.types.PoseBone.bone
* In other words, accessing edit bones in pose mode is not okay. It should be accessing edit bones in edit mode.  If it makes you feel better, the bone modes annoy me too. I sincerely hope Blender gets rid of it and just have one mode (i.e. no modes at all)
* Creating object and bone constraints have the same workflow. The obj below variable refers to both objects and bones. Be it noted that you can add constraint only in Pose Mode
* https://blenderartists.org/t/bone-manipulation-with-python-in-2-5/456531/6 

```python
# ACCESS CONSTRAINTS
constraint_list = obj.constraints
only_copy_constraint_list = [ c for c in obj.constraints if c.type == 'COPY_LOCATION']

# CREATE CONSTRAINTS
loc_cons = obj.constraints.new("COPY LOCATION")

# MODIFY PARAMETERS
loc_cons.target_space = 'WORLD'
loc_cons.owner_space = 'WORLD'
loc_constraint.target = obj # If the target is an object
loc_constraint.target = obj_armature # If the target is an armature/bone 
loc_constraint.subtarget = obj_bone # If the target is an armature/bone. Can accept a string as a parameter rather than just a bpy.data.object
loc_constraint.target = None # Removing the existing target

# REMOVING CONSTRAINTS
loc_cons = obj.constraints.remove(loc_cons)

# REMOVING ALL CONSTRAINTS
for constraint in constraint_list: # See access constraints above
    obj.constraints.remove(constraint)
```

```python
# ACCESS BONES
armature = bpy.data.objects['Armature']
active_bone = bpy.context.active_bone # Type return differs depending on the mode you are in.
active_pose_bone = bpy.context.active_pose_bone
 
selected_bones_list01 = bpy.context.selected_pose_bones

selected_bones_list02 = bpy.context.editable_bones
selected_bones_list02 = bpy.context.selected_editable_bones # alternative

specific_bone01 = armature.pose.bones['BoneName'] # returns PoseBone type
specific_bone02 = armature.data.bones['BoneName'] # returns Bone Type

# CREATE BONES
bpy.data.objects['metarig'].data.edit_bones.new("new_bone") #Must have access to the armature

# DELETE BONES

# MODIFY BONE PARAMETERS

bones.use_connect = True # works only on Edit Bones/Mode 
bones.use_deform = True # works only on Edit Bones/Mode

bpy.context.object.data.bones["thigh.L"].use_deform # Works on either modes/types where an armature is selected. 
```

```python 
Random
# Remove Animation
obj.animation_data_clear()

#apply transform
bpy.ops.object.visual_transform_apply()

#If the child object moves after setting the parent, use the following to move it back:

# After both parent and child have been link()ed to the scene:
childObject.parent = parentObject
childObject.matrix_parent_inverse = parentObject.matrix_world.inverted()


#To unparent and keep the child object location (without using operators):
parented_wm = childObject.matrix_world.copy()
childObject.parent = None
childObject.matrix_world = parented_wm

# Change objects rotation to euler 

# https://blender.stackexchange.com/questions/93197/make-all-bones-euler-rotation

import bpy
order = 'XYZ'
context = bpy.context
rig_object = context.active_object
for pb in rig_object.pose.bones:
    pb.rotation_mode = order
```

```python
# Snippets
# Change Bone Names

import bpy
context = bpy.context
obj = context.object

namelist = [("Bone", "Head")]

for name, newname in namelist:
    # get the pose bone with name
    pb = obj.pose.bones.get(name)
    # continue if no bone of that name
    if pb is None:
        continue
    # rename
    pb.name = newname

# Get global matrix
mat_local_to_parent = (
    bone.matrix_local if bone.parent is None else
    bone.parent.matrix_local.inverted() * bone.matrix_local
)

pos = mat_local_to_parent.to_translation()
quat = mat_local_to_parent.to_quaternion().inverted()
```
