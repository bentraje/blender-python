import bpy
bpy.context.object


#This is used to  create initial offset controls to match the controls to join orientation

obj_anim = []

for obj in bpy.context.selected_objects:
    
    try:
        if obj.animation_data.action != None:
            obj_anim.append(obj)
    except:
        pass    

for obj in obj_anim:
    col = obj.users_collection[0]
    child = obj.copy()
    
    col.objects.link(child)
    child.parent = obj
    
    child.animation_data_clear()
    
    if '.' in obj.name:
        base_name = obj.name.split(".")[0]
        new_name = base_name + '_offset'
        child.name = new_name
    else:
        child.name = obj.name + '_offset'

# EXECUTE SEPARATELY

for obj in bpy.context.selected_objects:
    
    
    if '_offset' in obj.name:
        loc_constraint = obj.constraints.new('COPY_LOCATION')
        rot_constraint = obj.constraints.new('COPY_ROTATION')
        
        loc_constraint.target = bpy.data.objects['Joints']
        rot_constraint.target = bpy.data.objects['Joints']
