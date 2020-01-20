# General

- There are three main ways to access and modify nodes. There’s no exclusivity. You can use all of them in the same script.
  - bpy.data : a somewhat low-level code (i.e. powerful but verbose)
  - bpy.context: a somewhat mid-level code
  - bpy.ops: a somewhat high-level code (i.e. easy to write but limited)
- Info panel that records commands performed in real-time. Unlike Maya where it returns MEL, or 3ds Max where it returns MaxScript, Blender returns python lines. As such, you can just copy and paste lines and stack them together

## Generic Commands

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
