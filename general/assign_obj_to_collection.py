import bpy 
import json

# NoneExist': 'Col_C'
# sample json structure
# data = {'Sphere': 'Col_A', 'Plane': 'Col_B', 'Cube': 'Col_C', }

with open("D:\layer_list.json", "r") as read_file:
    data = json.load(read_file)
    
for key, value in data.items():
    
    print (key, value)
    
    try:
        obj = bpy.data.objects[key]
    except:
        print (key +  " does not exist")
        continue

    bpy.context.scene.collection.objects.link(obj)    

    
    # Create a new collection if it doesn't exist
    if value not in bpy.data.collections:
        col = bpy.data.collections.new(value)
        bpy.context.scene.collection.children.link(col)
    else:
        col = bpy.data.collections[value]    
        
    for col in obj.users_collection:
        if col == bpy.data.collections[value]:
            pass
        else:
            col.objects.link(obj)
    
    # Unlink Unnecessary Collections
    for col in obj.users_collection:
        if col != bpy.data.collections[value]:
            col.objects.unlink(obj)
