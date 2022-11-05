#Quads

verts = [
    (1.0, 1.0, -1.0),
    (1.0, -1.0, -1.0),
    (-1.0, -1.0, -1.0),
    (-1.0, 1.0, -1.0),
    (1.0, 1.0, 1.0),
    (1.0, -1.0, 1.0),
    (-1.0, -1.0, 1.0),
    (-1.0, 1.0, 1.0)
]

faces = [
    (0, 1, 2, 3),
    (4, 7, 6, 5),
    (0, 4, 5, 1),
    (1, 5, 6, 2),
    (2, 6, 7, 3),
    (4, 0, 3, 7)
]

# Tris 


verts = [
    (-0.285437,-0.744976,-0.471429),
    (-0.285437,-0.744976,-2.471429),
    (1.714563,-0.744976,-2.471429),
    (1.714563,-0.744976,-0.471429),
    (-0.285437,1.255024,-0.471429),
    (-0.285437,1.255024,-2.471429),
    (1.714563,1.255024,-2.471429),
    (1.714563,1.255024,-0.471429)
]

faces =  [
    (4,5,1), (5,6,2), (6,7,3), (4,0,7),
    (0,1,2), (7,6,5), (0,4,1), (1,5,2),
    (2,6,3), (7,0,3), (3,0,2), (4,7,5)
]

import bpy  

# verts = 
# faces =   

mesh_data = bpy.data.meshes.new("cube_mesh_data")
mesh_data.from_pydata(verts, [], faces) 
mesh_data.update()

obj = bpy.data.objects.new("My_Object", mesh_data)

col = bpy.context.collection
col.objects.link(obj)
#obj.select = True
# scene.objects.active = obj  # make the selection effective