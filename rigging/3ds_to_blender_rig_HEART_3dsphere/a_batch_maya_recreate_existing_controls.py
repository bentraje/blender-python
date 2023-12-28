import bpy
import os
import json

def main():
    base = r"C:\Users\BT\Documents\GitHub\maya-python\rigging\3ds_to_maya_rig_HEART_3dsphere"
    file_name = r'_3dmedisphere_FULL_heart_anim.json'
    file_path = os.path.join(base, file_name)
    
    all_obj = bpy.data.objects
    arm_obj = bpy.data.objects['Point028']
    deformed_bones = arm_obj.data.bones

    with open(file_path, 'r') as f:
        data = json.load(f)
        
        # COMPLETENESS CHECK
        for d in data:
            if d in all_obj:
                print (d, " exists in the scene as a regular OBJ")
            else: 
                if d in deformed_bones:
                    print (d, " exists in the scene as a BONE")                    
                else:
                    print (d, " DO NOT exists in the scene *****************")  
                    

        # DUPLICATE OBJECT FOR ANIM OBJECTS
        
        arm_dup = arm_obj.copy()
        arm_dup.data = arm_obj.data.copy()
        bpy.context.collection.objects.link(arm_dup)
        
        arm_dup.name = arm_obj.name + "_anim"
        
        
        
import bpy

def duplicate_object_recursive(original_object, parent=None):
    # Duplicate the object and link it to the parent
    
    print ("A")
    duplicate_object = original_object.copy()
    print ("B")
    print (original_object)
    print (original_object.data)
    duplicate_object.data = original_object.data.copy()
    print ("C")    
    bpy.context.collection.objects.link(duplicate_object)
    print ("D")    
    
    # Set the parent of the duplicate object
    if parent:
        duplicate_object.parent = parent

    print ("E")    

    # Duplicate the child hierarchy recursively
    for child in original_object.children:
        duplicate_object_recursive(child, parent=duplicate_object)

    print ("D")    
        

    return duplicate_object


selected_object = bpy.data.objects['heart_full_rig']
duplicate_object_recursive(selected_object)
            
# main()  


'''
        

# Duplicate Object.

>>> arm_dup = arm.copy()
>>> arm_dup.data = arm.data.copy()
>>> arm_dup

bpy.context.collection.objects.link(arm_dup)

# Delete Data                      

action = armature_obj.animation_data.action

        if action:
            bpy.data.actions.remove(action)
'''