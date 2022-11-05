# Add an offset child to an object with animation

import bpy
bpy.context.object


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
