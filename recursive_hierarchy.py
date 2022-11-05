# https://blender.stackexchange.com/questions/145620/looping-over-hierarchies-of-objects-with-python
# Does not include recursion of the bones of the armature

import bpy
scene = bpy.context.scene

def print_heir(ob, levels=10):
    def recurse(ob, parent, depth):
        if depth > levels: 
            return
        print("  " * depth, ob.name)

        for child in ob.children:
            recurse(child, ob,  depth + 1)
    recurse(ob, ob.parent, 0)

root_obs = (o for o in scene.objects if not o.parent)

for o in root_obs:
    print_heir(o)