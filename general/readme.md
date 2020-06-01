# General

- There are three main ways to access and modify nodes. There’s no exclusivity. You can use all of them in the same script.
  - bpy.data : a somewhat low-level code (i.e. powerful but verbose)
  - bpy.context: a somewhat mid-level code
  - bpy.ops: a somewhat high-level code (i.e. easy to write but limited)
- Info panel that records commands performed in real-time. Unlike Maya where it returns MEL, or 3ds Max where it returns MaxScript, Blender returns python lines. As such, you can just copy and paste lines and stack them together

### Generic Commands

```python
# All objects
bpy.data.scenes
bpy.data.materials
bpy.data.objects # all objects in a scenes
bpy.context.scene.objects # specific to the active/selected scene
bpy.data.collections[0].objects # all objects in a collection
bpy.data.collections[0].all_objects # all objects (including grandchildren) in the collection of a collection  

# Hierarchy 
children = obj.children #list of all immediate child objects
sibling = 

# By name
bpy.data.objects['objectName']

# By selection
bpy.context.selected_objects
bpy.context.active_object # last selected object
'''
With the Preferences>Interface>Python Tooltips turned on,
you can hover a UI parameter and see its corresponding API equivalent.
'''

# Create Object
obj = bpy.data.objects.new("Empty", None)
context.scene.objects.link(obj)

# Create Collection
col = bpy.data.collections.new('new_collection')
bpy.context.scene.collection.children.link(col)
col.objects.link(obj) # Link obj to to the collection

# Query Parameters
bpy.data.object['objectName'].location
bpy.data.object['objectName'].name

# Modify Parameters
bpy.data.object['objectName'].location = (1,2,3)
bpy.data.object['objectName'].name = "newObjectName"
```

### Others
```python
# For the Blender Modelling
import bpy

objects = bpy.context.scene.objects

for obj in objects:
    obj.select = obj.type == "MESH"

for ob in bpy.context.selected_objects:
    ob.data.use_auto_smooth = False

mats = bpy.data.materials

for obj in bpy.data.objects:
    for slt in obj.material_slots:
        part = slt.name.rpartition('.')
        if part[2].isnumeric() and part[0] in mats:
            slt.material = mats.get(part[0])

for object in bpy.context.scene.objects:
    object.name = object.name.replace('_', '.')
```
```python
# Snippets
for ob in bpy.data.objects: print (ob.name)
for ob in bpy.context.selected_objects: ob.scale = [2,2,2]


arm.data.edit_bones[‘yourBone’].parent = arm.data.edit_bones[‘parentBone’]

bpy.data.objects[objectName].data.splines[0].use_cyclic you can also use bpy.data.curves[curveName].splines[0].use_cyclic but note that generally objectName != curveName

bpy.context.collection.objects.link(ob) bpy.data.collections[“Collection Name”].objects.link(ob)

General

Scripting
Ctrl+Spacebar to Autocomplete in the console
bpy.context = C
bpy.data = D

list(bpy.data.objects)
bpy.data.objects['Cube']
bpy.data.objects[0]

create new material. bpy.data.materials.new("MyMaterial")
but you also need to create material slot.

>>> bpy.data.scenes[0].render.resolution_percentage100
>>> bpy.data.scenes[0].objects["Torus"].data.vertices[0].co.x1.0


Data is added and removed via methods on the collections in bpy.data, eg:
create objects

>>> mesh = bpy.data.meshes.new(name="MyMesh")

>>> bpy.data.meshes.remove(mesh)

Preferences>Interface>Python Tooltip

C.object lists the active objects
for ob in C.scene.objects: print(ob.name)
C is like bpy.context
D is like bpy.data
import bpy
for 
press ctrl + spacebar to show pseduo auto completion. 
bpy context is agnostic. much like procedural programming
bpy data is  i guess for object oriented. 

bpy.data.objects['Suzanne']

bpy.context.select_objects

handler. its a trigger when something happens. it is executed. 
bpy.data.scenes['Scene'].render.resolution_percentage
bpy.data.objects[0].name
bpy.data.scenes[0].objects["Torus"].data.vertices[0].co.x
bpy.data.objects['Suzanne'] = bpy.data.scenes[0].objects['Suzanne']
mesh = bpy.data.meshes.new(name="MyMesh") but its not on the scene?
bpy.data.meshes.remove(mesh)
bpy.context readily operates on the selected object
Operators are tools generally accessed by the user from buttons, menu items or key shortcuts. 
>>> bpy.ops.mesh.flip_normals(){'FINISHED'}>>> 
bpy.ops.mesh.hide(unselected=False){'FINISHED'}>>> 
bpy.ops.object.scale_apply(){'FINISHED'}

Example of a matrix, vector multiplication:
bpy.context.object.matrix_world * bpy.context.object.data.verts[0].co

import mathutils
import math
plane.scale = mathutils.Vector((4, 4, 4))
plane.rotation_euler.rotate_axis('Y', math.radians(40))
```

```python
# Miscellaneous
# Executing a script within a script

script = bpy.data.texts["script_name.py"]
exec(script.as_string())

# Executing a script within a script

filename = "/full/path/to/myscript.py"
exec(compile(open(filename).read(), filename, 'exec'))

# Sequence Editor
https://blender.stackexchange.com/questions/71826/adding-keyboard-shortcut-to-a-blender-script

# Matrices
'''
As mentioned in the comments, the matrices need to be up to date, which can be done with bpy.context.scene.update()
'''

def ClearParent(child):    
    # Save the transform matrix before de-parenting
    matrixcopy = child.matrix_world.copy()
    
    # Clear the parent
    child.parent = None
        
    # Restore childs location / rotation / scale
    child.matrix_world = matrixcopy

# Matrix
relative_location = bpy.context.object.location
relative_location = bpy.context.object.matrix_local.to_translation()

world_location = bpy.context.object.matrix_world.to_translation()
world_loc, world_rot, world_scale = bpy.context.object.matrix_world.decompose()

from bpy import context
context.scene.cursor_location = context.object.matrix_world.to_translation()

# Retrieve Matrix of an object affected by Armature
https://blender.stackexchange.com/questions/49965/get-visual-transform-of-object-through-python

https://blender.stackexchange.com/questions/44637/how-can-i-manually-calculate-bpy-types-posebone-matrix-using-blenders-python-ap/44975#44975
```

