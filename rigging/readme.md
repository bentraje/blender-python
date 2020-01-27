# Constraints

Creating object and bone constraints have the same workflow. The obj below variable refers to both objects and bones. Be it noted that you can add constraint only in Pose Mode

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
# Create Constraint on Selected Bones
import bpy


# TypeError: 'NoneType' object is not iterable
# Means you are not in the pose mode

src = bpy.data.objects['Deformation']

for bone in bpy.context.selected_pose_bones:
    
    # Create Constraint
    loc_cons = bone.constraints.new('COPY_LOCATION')
    rot_cons = bone.constraints.new('COPY_ROTATION')
    
    # Modify Space Parameters
    
    loc_cons.target_space = 'LOCAL'
    loc_cons.owner_space = 'LOCAL'
    rot_cons.target_space = 'LOCAL'
    rot_cons.owner_space = 'LOCAL'
    
    
    # Modify Target Parameters
    
    loc_cons.target = src
    rot_cons.target = src
    
    sub_target = bone.name + '_ret'
    loc_cons.subtarget = sub_target    
    rot_cons.subtarget = sub_target
     
```

```python
#
import bpy
context = bpy.context
# the rig object
rig = context.object

# all copy location constraints on all pose bones
constraints = [c for pb in rig.pose.bones 
                 for c in pb.constraints
                 if c.type == 'COPY_LOCATION'
               # and "XY" in c.name
              ]

# set the desired properties
for c in constraints:
    c.use_y = True

# similarly for Transformation
# type from mousing over add constraint in UI
constraints = [c for pb in rig.pose.bones 
                 for c in pb.constraints
                 if c.type == 'TRANSFORM'
              ]

for tc in constraints:
    tc.to_max_y = 0.02 # given 1 blender unit is 1m


# all constraints from preselected pose bones
constraints = [c for pb in context.selected_pose_bones 
                 for c in pb.constraints
              ]
```
