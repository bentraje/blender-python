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
