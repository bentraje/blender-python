import bpy

def create_light():
    """
    Add a mesh light for cycles
    """

    # Add new plane
    bpy.ops.mesh.primitive_plane_add(location=(15, -5, 5))
    plane = bpy.context.active_object
    plane.name = 'Light Plane'
    plane.scale = mathutils.Vector((4, 4, 4))
    # tilt
    plane.rotation_euler.rotate_axis('Y', radians(40))

    # Create a new material
    material = bpy.data.materials.new(name="Plane Light Emission Shader")
    material.use_nodes = True

    # Remove default
    material.node_tree.nodes.remove(material.node_tree.nodes.get('Diffuse BSDF'))
    material_output = material.node_tree.nodes.get('Material Output')
    emission = material.node_tree.nodes.new('ShaderNodeEmission')
    emission.inputs['Strength'].default_value = 5.0

    # link emission shader to material
    material.node_tree.links.new(material_output.inputs[0], emission.outputs[0])

    # set activer material to your new material
    plane.active_material = material

create_light()