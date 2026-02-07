# Terrain utility functions
# Functions for terrain mesh creation and manipulation

import bpy
import bmesh
from mathutils import Vector
import random


def create_terrain_plane(size=100, subdivisions=50, name="Terrain"):
    """
    Create a subdivided plane to serve as terrain.
    
    Args:
        size: Size of the terrain plane
        subdivisions: Number of subdivisions for detail
        name: Name of the terrain object
    
    Returns:
        Blender mesh object
    """
    # Create mesh and object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    
    # Link to scene
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Create bmesh
    bm = bmesh.new()
    
    # Create grid
    bmesh.ops.create_grid(
        bm,
        x_segments=subdivisions,
        y_segments=subdivisions,
        size=size/2
    )
    
    # Update mesh
    bm.to_mesh(mesh)
    bm.free()
    
    return obj


def add_terrain_noise(terrain_obj, strength=2.0, scale=5.0):
    """
    Add noise displacement to terrain for natural variation.
    
    Args:
        terrain_obj: Terrain mesh object
        strength: Strength of the displacement
        scale: Scale of the noise pattern
    """
    # Add displacement modifier
    displace_mod = terrain_obj.modifiers.new(name="Terrain_Displace", type='DISPLACE')
    
    # Create texture for displacement
    texture = bpy.data.textures.new(name="Terrain_Noise", type='CLOUDS')
    texture.noise_scale = scale
    
    displace_mod.texture = texture
    displace_mod.strength = strength
    displace_mod.mid_level = 0.5


def get_terrain_height_at_position(terrain_obj, x, y):
    """
    Get the terrain height (Z coordinate) at a given X, Y position.
    Uses raycasting to find the surface.
    
    Args:
        terrain_obj: Terrain mesh object
        x: X coordinate
        y: Y coordinate
    
    Returns:
        Z coordinate (height) or None if no intersection
    """
    # Create ray from above the terrain
    ray_origin = Vector((x, y, 1000))
    ray_direction = Vector((0, 0, -1))
    
    # Perform raycast
    depsgraph = bpy.context.evaluated_depsgraph_get()
    result, location, normal, index = terrain_obj.ray_cast(
        ray_origin,
        ray_direction,
        depsgraph=depsgraph
    )
    
    if result:
        return location.z, normal
    return None, None


def get_terrain_normal_at_position(terrain_obj, x, y):
    """
    Get the surface normal at a given X, Y position on the terrain.
    
    Args:
        terrain_obj: Terrain mesh object
        x: X coordinate
        y: Y coordinate
    
    Returns:
        Normal vector or None if no intersection
    """
    _, normal = get_terrain_height_at_position(terrain_obj, x, y)
    return normal


def apply_terrain_material(terrain_obj, material_name="Terrain_Material"):
    """
    Apply a basic material to the terrain.
    
    Args:
        terrain_obj: Terrain mesh object
        material_name: Name for the material
    
    Returns:
        Material object
    """
    # Create material
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True
    
    # Get nodes
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Create shader nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set base color (grass green)
    principled.inputs['Base Color'].default_value = (0.1, 0.4, 0.1, 1.0)
    principled.inputs['Roughness'].default_value = 0.8
    
    # Link nodes
    mat.node_tree.links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    # Assign material to object
    if terrain_obj.data.materials:
        terrain_obj.data.materials[0] = mat
    else:
        terrain_obj.data.materials.append(mat)
    
    return mat
