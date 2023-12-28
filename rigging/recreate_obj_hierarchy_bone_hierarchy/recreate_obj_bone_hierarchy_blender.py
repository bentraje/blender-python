import bpy


def crawl_hierarchy(obj, indent=0):
    # Print the name of the current object with indentation
    print("  " * indent + obj.name)

    # Recursively process the children of the current object
    for child in obj.children:
        crawl_hierarchy(child, indent + 1)

# Replace "YourObjectName" with the name of the object you want to start from
root_object_name = "obj_hierarchy"

# Get the root object by name
root_object = bpy.data.objects.get(root_object_name)

# Check if the root object exists
if root_object:
    print(f"Hierarchy of object '{root_object_name}':")
    crawl_hierarchy(root_object)
else:
    print(f"The object '{root_object_name}' does not exist.")


def duplicate_object_recursive(original_object, parent=None):
    # Duplicate the object and link it to the parent
    
    
    duplicate_object = original_object.copy()
    # print ("B")
    # print (original_object)
    # print (original_object.data)
    # duplicate_object.data = original_object.data.copy()
    # print ("C")    
    bpy.context.collection.objects.link(duplicate_object)
    # print ("D")    
    
    # Set the parent of the duplicate object
    if parent:
        duplicate_object.parent = parent

    print ("E")    

    # Duplicate the child hierarchy recursively
    for child in original_object.children:
        duplicate_object_recursive(child, parent=duplicate_object)

    print ("D")    
        

    return duplicate_object


#selected_object = bpy.data.objects['heart_full_rig']
#duplicate_object_recursive(root_object)


armature_obj = bpy.data.objects.get('arm_hierarchy')


def bone_to_joint_hierarchy(original_object, parent=None):
    
    # Create New Bone
    
    print ("A")
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='EDIT')
    duplicate_obj = armature_obj.data.edit_bones.new(original_object.name)

    print ("B")
    if parent:
        bone_parent = armature.data.edit_bones.get(parent)
        duplicate_obj.parent = bone_parent

    print ("C")
    for child in original_object.children:
        duplicate_object_recursive(child, parent=duplicate_obj)

    print ("D")    
    return duplicate_obj

    #bones = obj.data.edit_bones


bone_to_joint_hierarchy(root_object)	


'''

    # Get the armature edit_bone by name
    edit_bone_a = armature_obj.data.edit_bones.get(bone_a_name)
    edit_bone_b = armature_obj.data.edit_bones.get(bone_b_name)

    # Check if both bones exist
    if edit_bone_a and edit_bone_b:
        # Set bone_b as the parent of bone_a
        edit_bone_a.parent = edit_bone_b

        # Switch back to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
'''