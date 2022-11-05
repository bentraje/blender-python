# https://blender.stackexchange.com/questions/135597/how-to-duplicate-an-object-in-2-8-via-the-python-api-without-using-bpy-ops-obje?newreg=19f5e730223c444eb0b870abfa4e9c8d

template_object = bpy.data.objects.get('TemplateObjectName')
if template_object:
    # Create the new object by linking to the template's mesh data
    new_object = bpy.data.objects.new('NewObjectName', template_object.data)
    # Create a new animation for the newly created object
    animation = new_object.animation_data_create()

    # Option 1: Linking action
    #-------------------------
    #Assign the template object's action to the new animation
    animation.action = template_object.animation_data.action

    # Option2: NOT Linking action
    #----------------------------
    # Assign a copy of the template object's action to the new animation
    animation.action = template_object.animation_data.action.copy()
    # Rename it if desired
    animation.action.name = 'NewAction'

    # Link the new object to the appropriate collection
    collection.objects.link(new_object)