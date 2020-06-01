# Constraints

### Creating object and bone constraints have the same workflow. The obj below variable refers to both objects and bones. Be it noted that you can add constraint only in Pose Mode

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
