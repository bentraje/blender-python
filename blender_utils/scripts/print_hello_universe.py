import bpy

def main():
    print ("Hello Universe")
    bpy.ops.mesh.primitive_cube_add()   
    bpy.ops.mesh.primitive_plane_add()
    bpy.ops.mesh.primitive_monkey_add()  
    print ("Add Cube")

if __name__=='__main__':
    main()