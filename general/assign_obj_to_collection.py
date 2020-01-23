import bpy 
import json

# NoneExist': 'Col_C'
# sample json structure
# data = {'Sphere': 'Col_A', 'Plane': 'Col_B', 'Cube': 'Col_C', }

with open("D:\layer_list.json", "r") as read_file:
    data = json.load(read_file)
    
for key, value in data.items():
    
    try:
        obj = bpy.data.objects[key]
    except:
        print (key +  " does not exist")
        continue   

    
    # Create a new collection if it doesn't exist
    if value not in bpy.data.collections:
        col = bpy.data.collections.new(value)
        bpy.context.scene.collection.children.link(col)
    else:
        col = bpy.data.collections[value]    
    
    # Assign the object to the collection if it still not yet assigned
    for col in obj.users_collection:
        if col == bpy.data.collections[value]:
            pass
        else:
            col = bpy.data.collections[value]
            try:
                col.objects.link(obj)
            except:
                print (obj + ' already in collection ')
                continue
    
    # Unlink Unnecessary Collections
    for col in obj.users_collection:
        if col != bpy.data.collections[value]:
            col.objects.unlink(obj)

    # Remove parent on object to prevent that greyout object in the outline
    bpy.data.objects[key].parent = None
    
