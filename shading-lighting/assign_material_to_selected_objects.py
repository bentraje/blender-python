import bpy


# Get the selected objects
selected_objects = bpy.context.selected_objects

for sel in selected_objects:
    children = sel.children
    children.append(sel)
    for obj in children:
        if obj.type == 'MESH':
            if not selected_object.data.materials:
                selected_object.data.materials.append(None)

            obj.data.materials[0] = bpy.data.materials['female_gen_mat']

            print ("assigned_materials for ", obj.name)
